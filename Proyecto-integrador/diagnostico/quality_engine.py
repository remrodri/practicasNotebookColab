"""Motor reutilizable de diagnóstico; nunca modifica las columnas Bronze."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ISSUE_COLUMNS = ["fila_bronze", "rule_id", "dimension_calidad", "severidad", "accion",
                 "tipo_problema", "columna_afectada", "codigo_error", "valor_original", "detalle"]


def cargar_catalogo(ruta):
    catalogo = json.loads(Path(ruta).read_text(encoding="utf-8"))
    reglas = catalogo["reglas"]
    ids = [r["rule_id"] for r in reglas]
    if len(ids) != len(set(ids)):
        raise ValueError("rule_id duplicado en el catálogo")
    tipos = {"not_null", "regex", "datetime", "numeric", "sentinel", "range",
             "allowed_values", "flag", "unit_warning", "duplicate_key", "foreign_key",
             "positive", "normalized_collision"}
    for regla in reglas:
        if regla["tipo_regla"] not in tipos:
            raise ValueError(f"Tipo de regla desconocido: {regla['tipo_regla']}")
        if regla["severidad"] not in {"CRITICAL", "WARNING"}:
            raise ValueError(f"Severidad inválida: {regla['rule_id']}")
        if regla["accion"] not in {"CUARENTENA", "REVISAR"}:
            raise ValueError(f"Acción inválida: {regla['rule_id']}")
    return catalogo


def _texto(serie):
    return serie.astype("string").str.strip()


def _evaluar(df, regla, referencias):
    tipo = regla["tipo_regla"]
    columna = regla["columna"]
    p = regla.get("parametros", {})
    if tipo == "duplicate_key":
        clave_cols = p["clave"]
        clave = df[clave_cols].astype("string").apply(lambda s: s.str.strip())
        firma = pd.util.hash_pandas_object(df[p["columnas_bronze"]].astype("string"), index=False)
        grupos = pd.MultiIndex.from_frame(clave)
        variantes = firma.groupby(grupos).transform("nunique")
        repetida = clave.duplicated(keep=False)
        mascara = (repetida & variantes.gt(1)) if p["clase"] == "conflicto" else (df[p["columnas_bronze"]].duplicated(keep="first") & ~variantes.gt(1))
        evidencia = clave.astype("string").agg(" + ".join, axis=1)
        return mascara, evidencia, None
    if tipo == "normalized_collision":
        original = df[columna].astype("string")
        normalizado = original.str.strip().str.upper()
        # Colisión solo cuando el ID normalizado coincide y el texto original difiere.
        variantes = original.groupby(normalizado, dropna=False).transform("nunique")
        mascara = normalizado.duplicated(keep="first") & variantes.gt(1)
        return mascara.fillna(False).astype(bool), original, None
    if columna not in df:
        raise ValueError(f"Columna requerida ausente: {columna}")
    valor = _texto(df[columna])
    presente = valor.notna() & valor.ne("")
    if tipo == "not_null":
        mascara = ~presente
    elif tipo == "regex":
        valor_formato = df[columna].astype("string") if p.get("exact_raw", False) else valor
        mascara = presente & ~valor_formato.str.fullmatch(p["patron"]).fillna(False)
    elif tipo == "datetime":
        formato = valor.str.fullmatch(p["patron"]).fillna(False)
        fecha = pd.to_datetime(valor, format=p["formato"], errors="coerce")
        mascara = presente & (~formato | fecha.isna())
    elif tipo in {"numeric", "sentinel", "range", "positive"}:
        numero = pd.to_numeric(valor, errors="coerce")
        if tipo == "numeric":
            mascara = presente & numero.isna()
        elif tipo == "sentinel":
            mascara = numero.isin(p["valores"])
        elif tipo == "positive":
            mascara = numero.notna() & numero.le(0)
        else:
            mascara = numero.notna() & ~numero.between(p["min"], p["max"])
    elif tipo == "allowed_values":
        mascara = presente & ~valor.str.upper().isin(p["valores"])
    elif tipo == "flag":
        mascara = presente & ~valor.isin(["0", "1"])
    elif tipo == "unit_warning":
        mascara = valor.str.upper().eq(p["valor"])
    elif tipo == "foreign_key":
        nombre = p["dataset"]
        if nombre not in referencias:
            return None, None, "SIN_FUENTE_REFERENCIA"
        ref = referencias[nombre]
        if p["columna_referencia"] not in ref.columns:
            return None, None, "SIN_COLUMNA_REFERENCIA"
        ids = set(_texto(ref[p["columna_referencia"]]).dropna()) - {""}
        mascara = presente & ~valor.isin(ids)
    else:
        raise ValueError(tipo)
    return mascara.fillna(False).astype(bool), df[columna], None


def diagnosticar(df_bronze, catalogo, referencias=None):
    referencias = referencias or {}
    columnas = catalogo["columnas_bronze"]
    if list(df_bronze.columns) != columnas or not df_bronze.columns.is_unique:
        raise ValueError(f"Esquema Bronze inesperado: {list(df_bronze.columns)}")
    principal = df_bronze.copy(deep=True)
    principal.insert(0, "fila_bronze", range(1, len(principal) + 1))
    hallazgos, estado = [], []
    for regla in catalogo["reglas"]:
        mascara, evidencia, motivo = _evaluar(principal, regla, referencias)
        if motivo:
            estado.append({"rule_id": regla["rule_id"], "estado": "NO_EJECUTADA", "motivo": motivo, "incidencias": 0})
            continue
        filas = principal.loc[mascara, ["fila_bronze"]].copy()
        for campo in ISSUE_COLUMNS[1:]:
            if campo == "valor_original":
                filas[campo] = evidencia.loc[mascara].astype("string").to_numpy()
            else:
                filas[campo] = regla.get(campo, "")
        hallazgos.append(filas[ISSUE_COLUMNS])
        estado.append({"rule_id": regla["rule_id"], "estado": "EJECUTADA", "motivo": "", "incidencias": len(filas)})
    problemas = pd.concat(hallazgos, ignore_index=True) if hallazgos else pd.DataFrame(columns=ISSUE_COLUMNS)
    problemas = problemas.sort_values(["fila_bronze", "rule_id"], kind="stable").reset_index(drop=True)
    problemas["version_catalogo"] = catalogo["version_catalogo"]
    agrupado = problemas.groupby("fila_bronze")
    principal["columnas_con_problemas"] = principal["fila_bronze"].map(
        agrupado["columna_afectada"].agg(lambda s: "|".join(dict.fromkeys(s)))).fillna("")
    principal["cantidad_problemas"] = principal["fila_bronze"].map(agrupado.size()).fillna(0).astype(int)
    for sev, nombre in [("CRITICAL", "cantidad_critical"), ("WARNING", "cantidad_warning")]:
        conteo = problemas.loc[problemas["severidad"].eq(sev)].groupby("fila_bronze").size()
        principal[nombre] = principal["fila_bronze"].map(conteo).fillna(0).astype(int)
    cuarentena = problemas.loc[problemas["accion"].eq("CUARENTENA"), "fila_bronze"]
    principal["en_cuarentena"] = principal["fila_bronze"].isin(cuarentena)
    return principal, problemas, pd.DataFrame(estado)


def reportes(principal, problemas, estado, catalogo, archivo, sha256):
    n = len(principal)
    metricas = pd.DataFrame([
        ("archivo_bronze", archivo), ("sha256_bronze", sha256),
        ("version_catalogo", catalogo["version_catalogo"]),
        ("filas_bronze", n), ("filas_con_problemas", int(principal["cantidad_problemas"].gt(0).sum())),
        ("filas_en_cuarentena", int(principal["en_cuarentena"].sum())),
        ("filas_solo_warning", int((principal["cantidad_warning"].gt(0) & principal["cantidad_critical"].eq(0)).sum())),
        ("incidencias", len(problemas)),
        ("incidencias_critical", int(problemas["severidad"].eq("CRITICAL").sum())),
        ("incidencias_warning", int(problemas["severidad"].eq("WARNING").sum())),
        ("reglas_no_ejecutadas", int(estado["estado"].eq("NO_EJECUTADA").sum())),
    ], columns=["metrica", "valor"])
    def resumen(columnas):
        base = problemas.groupby(columnas, dropna=False).agg(incidencias=("fila_bronze", "size"), filas_afectadas=("fila_bronze", "nunique")).reset_index()
        base["porcentaje_filas"] = (base["filas_afectadas"] / n * 100).round(2) if n else 0.0
        return base
    return {
        "metricas": metricas,
        "por_regla": resumen(["rule_id", "dimension_calidad", "severidad", "accion", "tipo_problema", "columna_afectada", "codigo_error"]),
        "por_columna": resumen(["columna_afectada"]),
        "por_dimension": resumen(["dimension_calidad"]),
        "estado_reglas": estado,
    }
