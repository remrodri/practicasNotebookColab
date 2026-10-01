---
name: andinalog-auditoria-inicial
description: Audita en solo lectura un notebook o etapa de AndinaLog 03B antes de corregirla y produce hallazgos accionables con evidencia.
---

# Auditoría inicial

No edites notebooks, datos ni informes. Lee `AGENTS.md`, la memoria relevante y la skill del notebook.

## Verificaciones

- Entradas y rutas reproducibles.
- Notebook ejecutado sin errores y en orden.
- Unidad, claves, filas, faltantes y duplicados.
- Conciliación entre entrada, salida y cuarentena.
- Reglas temporales, joins e imputaciones justificadas.
- Ausencia de fuga entre entrenamiento y prueba.
- Coherencia entre código, salidas, interpretaciones e informe.
- Lenguaje comprensible y afirmaciones sin causalidad indebida.
- Dependencias externas o contratos faltantes.

## Hallazgos

Clasifica cada hallazgo como crítico, alto, medio o bajo. Incluye identificador, archivo, evidencia, impacto, corrección esperada y criterio para cerrarlo. Separa hechos de recomendaciones.

## Salida

Guarda `.opencode/audits/AAAA-MM-DD-inicial-<alcance>.md`. No marques el producto como aprobado; esa decisión corresponde a la auditoría final.
