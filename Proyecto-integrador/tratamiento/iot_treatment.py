"""Reglas específicas de tratamiento IoT de AndinaLog 03B."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from treatment_engine import cargar_catalogo, iniciar_acciones, resolver, excluir, estado_final, sha256, validar_entrada, exportar

VERSION_DIAGNOSTICO = "GIAD-M3-S4-IOT-diagnostico-v7"
VERSION_TRATAMIENTO = "GIAD-M3-S4-IOT-tratamiento-v6"
BRONZE = ["timestamp", "viaje_id", "order_id", "camion_id", "producto_id",
          "temperatura_cabina_c", "temp_unit", "humedad_cabina_pct",
          "desviacion_termica_flag", "desviacion_proximos_60min_flag"]


def leer(ruta):
    return pd.read_csv(ruta, dtype="string", encoding="utf-8-sig", keep_default_na=False)


def rutas(raiz):
    raiz = Path(raiz)
    d = raiz / "proyecto-integrador/diagnostico/andinalog_iot_telemetry/salidas"
    t = raiz / "proyecto-integrador/tratamiento"
    return {
        "bronze": raiz / "datasets/AndinaLog_03B_Bronce/andinalog_iot_telemetry.csv",
        "principal": d / "andinalog_iot_telemetry_v7_diagnosticado.csv",
        "productos": raiz / "proyecto-integrador/andinalog_productos/notebook2/salidas/andinalog_productos_silver.csv",
        "flota": raiz / "proyecto-integrador/andinalog_flota/notebook2/salidas/andinalog_flota_silver.csv",
        "catalogo": t / "catalogo_reglas_tratamiento.json",
        "salidas": t / "salidas",
    }


def _incidencias_integradas(principal):
    import json
    requeridas = {"incidencias_json", "cantidad_problemas", "version_diagnostico", "sha256_bronze"}
    if not requeridas.issubset(principal.columns):
        raise ValueError("El diagnosticado no contiene el contrato integrado v7")
    registros = []
    for fila, detalle, conteo in principal[["fila_bronze", "incidencias_json", "cantidad_problemas"]].itertuples(index=False, name=None):
        incidencias = json.loads(detalle)
        if len(incidencias) != int(conteo):
            raise ValueError(f"Incidencias y contador no coinciden en fila {fila}")
        registros.extend({"fila_bronze":fila, **incidencia} for incidencia in incidencias)
    return pd.DataFrame(registros)


def _reporte_integrado(principal):
    valores = {}
    for campo in ("version_diagnostico", "sha256_bronze"):
        if principal[campo].nunique() != 1:
            raise ValueError(f"Metadato inconsistente: {campo}")
        valores[campo] = principal[campo].iloc[0]
    valores["filas_bronze"] = str(len(principal))
    return pd.DataFrame(valores.items(), columns=["metrica", "valor"])


def _duplicados(df, flota_ids):
    decisiones = []
    claves = df["viaje_id"].str.strip() + "|" + df["timestamp"].str.strip()
    for clave, grupo in df.groupby(claves, sort=False):
        if len(grupo) < 2:
            continue
        grupo = grupo.sort_values("fila_bronze", key=lambda s: s.astype(int))
        tipo, canonica = "CONFLICTO", None
        if len(grupo) == 2:
            a, b = grupo.iloc[0], grupo.iloc[1]
            if all(a[c] == b[c] for c in BRONZE):
                tipo, canonica = "IDENTICO", a["fila_bronze"]
            else:
                ca, cb = a["camion_id"].strip().upper(), b["camion_id"].strip().upper()
                solo_camion = all(a[c] == b[c] for c in BRONZE if c != "camion_id")
                if solo_camion and ca == cb and ca in flota_ids:
                    tipo, canonica = "CAMION_EQUIVALENTE", a["fila_bronze"]
                else:
                    def comparable(x,c):
                        v=x[c].strip()
                        return v.upper() if c=="camion_id" and v.upper() in flota_ids else v
                    compatibles = all(not (comparable(a,c) and comparable(b,c) and comparable(a,c)!=comparable(b,c)) for c in BRONZE)
                    na=sum(bool(a[c].strip()) for c in BRONZE)
                    nb=sum(bool(b[c].strip()) for c in BRONZE)
                    if compatibles and na != nb:
                        tipo, canonica = "COMPLEMENTARIO", a["fila_bronze"] if na>nb else b["fila_bronze"]
        for _, fila in grupo.iterrows():
            decision = "PENDIENTE" if canonica is None else ("CANONICA" if fila["fila_bronze"]==canonica else "COPIA_EXCLUIDA")
            decisiones.append({"fila_bronze":fila["fila_bronze"],"clave_lectura":clave,
                              "tipo_duplicado":tipo,"decision_duplicado":decision,
                              "fila_canonica":canonica or ""})
    return pd.DataFrame(decisiones, columns=["fila_bronze","clave_lectura","tipo_duplicado","decision_duplicado","fila_canonica"])


def tratar(raiz, guardar=False):
    p = rutas(raiz)
    for nombre in ("bronze","principal","productos","flota","catalogo"):
        if not p[nombre].is_file():
            raise FileNotFoundError(p[nombre])
    principal = leer(p["principal"])
    if "zona_horaria_origen" not in principal or not principal["zona_horaria_origen"].eq("America/La_Paz").all():
        raise ValueError("El diagnóstico no confirma America/La_Paz como zona horaria de origen")
    problemas = _incidencias_integradas(principal)
    reporte = _reporte_integrado(principal)
    productos, flota, catalogo = leer(p["productos"]), leer(p["flota"]), cargar_catalogo(p["catalogo"])
    validar_entrada(principal, problemas, reporte, catalogo, p["bronze"], VERSION_DIAGNOSTICO)
    if productos["producto_id"].duplicated().any() or flota["camion_id"].duplicated().any():
        raise ValueError("Dimensión Silver con clave duplicada")
    acciones = iniciar_acciones(problemas, catalogo)
    df = principal.copy(deep=True)

    # El docente confirmó America/La_Paz para fechas sin zona. Bronze permanece intacto.
    fecha = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    utc = fecha.dt.tz_localize("America/La_Paz", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
    df["timestamp_utc"] = utc.dt.strftime("%Y-%m-%dT%H:%M:%SZ").fillna("")
    df["zona_horaria_origen_asumida"] = "America/La_Paz"

    numero = pd.to_numeric(df["temperatura_cabina_c"], errors="coerce")
    unidad = df["temp_unit"].str.strip().str.upper()
    valida = numero.notna() & numero.ne(-999)
    df["temperatura_c_preparada"] = pd.Series(pd.NA, index=df.index, dtype="Float64")
    c = valida & unidad.eq("C")
    f = valida & unidad.eq("F")
    df.loc[c, "temperatura_c_preparada"] = numero[c]
    df.loc[f, "temperatura_c_preparada"] = (numero[f]-32)*5/9
    df["temperatura_c_preparada"] = df["temperatura_c_preparada"].round(6)
    df["tratamiento_temperatura"] = "SIN_TRATAMIENTO"
    df.loc[c, "tratamiento_temperatura"] = "C_ORIGINAL"
    df.loc[f, "tratamiento_temperatura"] = "F_A_C"
    f_filas = set(df.loc[f,"fila_bronze"])
    mask = acciones["rule_id"].eq("IOT-R015") & acciones["fila_bronze"].isin(f_filas)
    resolver(acciones, mask, "F_A_C", "Fahrenheit convertido a Celsius en columna preparada")

    flota_ids = set(flota["camion_id"])
    formato = df["camion_id"].str.strip().str.upper()
    canonico = formato.isin(flota_ids)
    df["camion_id_preparado"] = df["camion_id"]
    df.loc[canonico, "camion_id_preparado"] = formato[canonico]
    reparadas = set(df.loc[canonico,"fila_bronze"])
    mask = acciones["rule_id"].eq("IOT-R008") & acciones["fila_bronze"].isin(reparadas)
    resolver(acciones, mask, "CAMION_CANONICO", "Formato canónico confirmado en Flota Silver")

    decisiones = _duplicados(df, flota_ids)
    if len(decisiones):
        lookup = decisiones.set_index("fila_bronze")["decision_duplicado"]
        decision = acciones["fila_bronze"].map(lookup)
        dup = acciones["rule_id"].isin(["IOT-R011","IOT-R012"])
        resolver(acciones, dup & decision.eq("CANONICA"), "SELECCION_CANONICA", "Lectura canónica del par")
        excluir(acciones, dup & decision.eq("COPIA_EXCLUIDA"), "COPIA_EXCLUIDA", "Copia conservada fuera de Silver")
        # En duplicados idénticos la primera fila no recibe incidencia; la segunda sí.
        excluidas = set(decisiones.loc[decisiones["decision_duplicado"].eq("COPIA_EXCLUIDA"),"fila_bronze"])
        existentes = set(acciones.loc[dup & decision.eq("COPIA_EXCLUIDA"),"fila_bronze"])
        for fila in sorted(excluidas-existentes,key=int):
            acciones.loc[len(acciones)] = {"fila_bronze":fila,"rule_id":"IOT-R011","codigo_error":"COPIA_EXCLUIDA",
                "estado_tratamiento":"EXCLUIDO","bloquea_silver":True,"tratamiento_aplicado":"COPIA_EXCLUIDA",
                "detalle_resultado":"Copia conservada fuera de Silver"}

    df, pendientes = estado_final(df, acciones)
    df["cobertura_producto"] = df["producto_id"].isin(set(productos["producto_id"]))
    df["cobertura_flota"] = df["camion_id_preparado"].isin(flota_ids)
    df["apto_serie"] = ~df["en_cuarentena_final"] & df["timestamp_utc"].ne("")
    df["apto_termica"] = df["apto_serie"] & df["cobertura_producto"] & df["temperatura_c_preparada"].notna()
    df["version_tratamiento"] = VERSION_TRATAMIENTO
    cuarentena = df.loc[df["en_cuarentena_final"]].copy()
    silver = df.loc[~df["en_cuarentena_final"], BRONZE + ["timestamp_utc","cobertura_producto","cobertura_flota","apto_termica"]].copy()
    idx = silver.index
    silver["camion_id"] = df.loc[idx,"camion_id_preparado"]
    silver["temperatura_cabina_c"] = df.loc[idx,"temperatura_c_preparada"]
    silver["temp_unit"] = "C"
    assert df[BRONZE].equals(principal[BRONZE])
    assert not silver.duplicated(["viaje_id","timestamp"]).any()
    assert silver["temperatura_cabina_c"].notna().all()
    assert set(pendientes.loc[pendientes["bloquea_silver"],"fila_bronze"]) == set(cuarentena["fila_bronze"])
    reporte2 = pd.DataFrame([
        ("version_tratamiento",VERSION_TRATAMIENTO),
        ("version_diagnostico",VERSION_DIAGNOSTICO),
        ("sha256_bronze",sha256(p["bronze"])),
        ("filas_totales",len(df)),
        ("filas_silver",len(silver)),
        ("filas_cuarentena_final",len(cuarentena)),
        ("filas_apto_termica",int(df["apto_termica"].sum())),
        ("filas_sin_producto_silver",int((~df["cobertura_producto"]).sum())),
        ("filas_sin_flota_silver",int((~df["cobertura_flota"]).sum())),
        ("temperaturas_F_a_C",int(f.sum())),
        ("temperaturas_K_a_C",0),
        ("acciones_pendientes",int(acciones["estado_tratamiento"].eq("PENDIENTE").sum())),
        ("copias_excluidas",int(acciones["estado_tratamiento"].eq("EXCLUIDO").sum())),
    ],columns=["metrica","valor"])
    tablas = {"andinalog_iot_telemetry_v6_tratado.csv":df,
              "andinalog_iot_telemetry_v6_silver.csv":silver,
              "andinalog_iot_telemetry_v6_acciones.csv":acciones,
              "andinalog_iot_telemetry_v6_decisiones_duplicados.csv":decisiones,
              "andinalog_iot_telemetry_v6_cuarentena_final.csv":cuarentena,
              "andinalog_iot_telemetry_v6_reporte_tratamiento.csv":reporte2}
    if guardar:
        fuentes={p[k]:sha256(p[k]) for k in ("bronze","principal","productos","flota","catalogo")}
        exportar(p["salidas"],tablas,fuentes)
    return tablas
