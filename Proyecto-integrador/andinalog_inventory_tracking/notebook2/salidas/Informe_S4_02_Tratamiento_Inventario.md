# Informe de tratamiento de seguimiento de inventario

**Fuente Bronze SHA-256:** `6b10604538376dda79b3ebe4cc77015321c31ae17ac092e29edf3c66a5cf2c0c`
**Referencia de productos SHA-256:** `428412504cad67f8ea0a5c6d5bb957faafd6f87337d022d70c7682e777c400cd`
**Versión:** `GIAD-M3-S4-INV-tratamiento-v1`

## Resultado del lote

Se conservaron las 6,040 filas. La cuarentena pasó de 104 a 69 filas; 35 salieron tras resolver completamente sus problemas. Se registraron 36 problemas resueltos, 29 pendientes y 40 copias excluidas de la vista analítica.

## Tratamientos aplicados

- Se convirtieron 25 fechas de ingreso con formato DD/MM/YYYY a convención ISO YYYY-MM-DD.
- Se convirtieron 10 registros con cantidad de ingreso expresada como 'cien' a valor entero 100.
- No se imputaron fechas de salida imposibles (2026-02-31), mermas negativas ni fechas de vencimiento ausentes por falta de evidencia externa.

## Duplicados y selección canónica

Se auditaron 40 pares de registros con clave duplicada: 39 pares idénticos y 1 par con mayor estándar en formato de fecha.
Se asignó condición canónica a 40 registros y se conservaron 40 copias duplicadas en cuarentena.

## Motivos que permanecen en cuarentena

| Columna | Código | Motivos finales |
|---|---|---:|
| cantidad_merma | FUERA_RANGO | 6 |
| fecha_salida | FECHA_INVALIDA | 5 |
| fecha_vencimiento | FALTANTE | 18 |
| movimiento_id | DUPLICADO | 40 |

## Reglas aplicadas

- `DUPLICADO_IDENTICO`: **APROBADA**. Tratamiento: Conservar primera aparicion y marcar copia como excluida. Acuerdo: Acuerdo de equipo S4: duplicados exactos auditados
- `DUPLICADO_COMPLEMENTARIO`: **APROBADA**. Tratamiento: Elegir fila con fecha_ingreso ISO canonica y excluir copia. Acuerdo: Acuerdo de equipo S4: fila con formato ISO prevalece
- `FECHA_INGRESO_FORMATO`: **APROBADA**. Tratamiento: Convertir DD/MM/YYYY a YYYY-MM-DD conservando original. Acuerdo: Acuerdo de equipo S4: estandarizacion de convencion de fecha
- `CANTIDAD_INGRESO_TEXTO`: **APROBADA**. Tratamiento: Convertir 'cien' a 100 en cantidad_ingreso_preparada. Acuerdo: Acuerdo de equipo S4: conversion de palabra numerica evidente
- `MERMA_SIGNO_NEGATIVO`: **PENDIENTE**. Tratamiento: Corregir signo invirtiendo valor absoluto si ingreso > salida. Acuerdo: pendiente.
- `FECHA_SALIDA_IMPOSIBLE`: **PENDIENTE**. Tratamiento: Imputar fecha correcta para 2026-02-31. Acuerdo: pendiente.
- `VENCIMIENTO_FALTANTE`: **PENDIENTE**. Tratamiento: Imputar fecha de vencimiento segun categoria de producto. Acuerdo: pendiente.