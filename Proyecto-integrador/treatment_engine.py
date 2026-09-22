"""Motor reusable para aplicar decisiones de tratamiento a incidencias diagnosticadas.

No contiene reglas de negocio de un CSV específico. El catálogo decide qué
incidencias bloquean una fila y el adaptador del dataset registra resoluciones.
"""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

import pandas as pd


ESTADOS = {"RESUELTO", "PENDIENTE", "ADVERTENCIA", "EXCLUIDO"}


def sha256(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def validar_entrada(principal, problemas, reporte, catalogo, bronze, version):
    if not principal["fila_bronze"].is_unique:
        raise ValueError("fila_bronze duplicada")
    if not problemas["fila_bronze"].isin(principal["fila_bronze"]).all():
        raise ValueError("Incidencia sin fila Bronze")
    if not catalogo["regla_id"].is_unique:
        raise ValueError("regla_id duplicada en catálogo de tratamiento")
    metricas = reporte.set_index("metrica")["valor"]
    if metricas["version_diagnostico"] != version:
        raise ValueError("Versión de diagnóstico incompatible")
    if metricas["sha256_bronze"] != sha256(bronze):
        raise ValueError("Bronze y diagnóstico no corresponden")
    if len(principal) != int(metricas["filas_bronze"]):
        raise ValueError("Cantidad de filas distinta al diagnóstico")


def iniciar_acciones(problemas, catalogo):
    """Crea una decisión auditable por incidencia; ninguna se omite."""
    acciones = problemas.copy(deep=True)
    politica = catalogo.set_index("regla_id")
    faltantes = set(acciones["rule_id"]) - set(politica.index)
    if faltantes:
        raise ValueError(f"Faltan decisiones para reglas: {sorted(faltantes)}")
    acciones["estado_tratamiento"] = acciones["rule_id"].map(politica["estado_inicial"])
    acciones["bloquea_silver"] = acciones["rule_id"].map(politica["bloquea_silver"]).str.lower().eq("true")
    acciones["tratamiento_aplicado"] = "NINGUNO"
    acciones["detalle_resultado"] = acciones["rule_id"].map(politica["justificacion"])
    if not acciones["estado_tratamiento"].isin(ESTADOS).all():
        raise ValueError("Estado de tratamiento inválido")
    return acciones


def resolver(acciones, mascara, tratamiento, detalle):
    acciones.loc[mascara, "estado_tratamiento"] = "RESUELTO"
    acciones.loc[mascara, "bloquea_silver"] = False
    acciones.loc[mascara, "tratamiento_aplicado"] = tratamiento
    acciones.loc[mascara, "detalle_resultado"] = detalle


def excluir(acciones, mascara, tratamiento, detalle):
    acciones.loc[mascara, "estado_tratamiento"] = "EXCLUIDO"
    acciones.loc[mascara, "bloquea_silver"] = True
    acciones.loc[mascara, "tratamiento_aplicado"] = tratamiento
    acciones.loc[mascara, "detalle_resultado"] = detalle


def estado_final(principal, acciones):
    salida = principal.copy(deep=True)
    bloqueadas = acciones.loc[acciones["bloquea_silver"], "fila_bronze"].drop_duplicates()
    salida["en_cuarentena_final"] = salida["fila_bronze"].isin(bloqueadas)
    pendientes = acciones.loc[acciones["estado_tratamiento"].isin(["PENDIENTE", "EXCLUIDO"])].copy()
    pendientes["motivo"] = pendientes["rule_id"] + ":" + pendientes["codigo_error"]
    motivos = pendientes.groupby("fila_bronze")["motivo"].agg(lambda s: "|".join(dict.fromkeys(s)))
    salida["motivos_finales"] = salida["fila_bronze"].map(motivos).fillna("")
    return salida, pendientes


def exportar(directorio, tablas, fuentes):
    """Escribe versiones nuevas y comprueba que las fuentes no cambiaron."""
    for ruta, huella in fuentes.items():
        if sha256(ruta) != huella:
            raise RuntimeError(f"La fuente cambió durante el tratamiento: {ruta}")
    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    temporales = {}
    try:
        for nombre, tabla in tablas.items():
            destino = directorio / nombre
            if destino.exists():
                raise FileExistsError(f"La salida ya existe: {destino}")
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", prefix=".tmp_trat_", dir=directorio,
                                             encoding="utf-8-sig", newline="", delete=False) as tmp:
                tabla.to_csv(tmp, index=False)
                temporales[destino] = Path(tmp.name)
        for destino, temporal in temporales.items():
            os.replace(temporal, destino)
    finally:
        for temporal in temporales.values():
            temporal.unlink(missing_ok=True)
    return list(temporales)
