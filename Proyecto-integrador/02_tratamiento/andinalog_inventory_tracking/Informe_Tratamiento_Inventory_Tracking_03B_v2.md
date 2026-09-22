# Informe de tratamiento — Inventory Tracking v2

Grupo 06, AndinaLog 03B. Fecha: 2026-09-22.

## Decisiones

Normalizar formatos de fecha y producto; inferir vencimiento faltante solo si el producto tiene al menos 20 lotes válidos y una única vida útil observada. Registrar vencimiento_imputado y excluirlo del KPI de vencimiento observado. Excluir duplicados, conflictos y valores imposibles.

## Resultado verificado

| Medida | Filas |
|---|---:|
| Entrada diagnosticada | 6040 |
| Silver | 5980 |
| Cuarentena final | 60 |
| Recuperadas de cuarentena diagnóstica | 49 |

Silver y cuarentena final suman exactamente la entrada. Silver conserva los valores Bronze junto a los tratados y las marcas de imputación, normalización o revisión; los motivos y acciones explican cada decisión. `en_cuarentena_diagnostico` es histórico y `en_cuarentena_final` indica la decisión de esta etapa. El reporte de calidad resume estas cifras.

Las cantidades son unidades del producto, sin equivalencia supuesta a kg o cajas. Las fechas son fechas de calendario sin conversión horaria. Un vencimiento estimado no confirma el vencimiento físico del lote.
