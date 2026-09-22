# Informe de tratamiento — Productos v2

Grupo 06, AndinaLog 03B. Fecha: 2026-09-22.

## Decisiones

Normalizar ID sin conflicto. Inferir categoría únicamente con objetivo, tolerancia y vida útil observada concordantes; inferir objetivo faltante solo con categoría, tolerancia y vida útil concordantes. Marcar categoria_imputada y temperatura_imputada. Excluir duplicados posteriores y conflictos.

## Resultado verificado

| Medida | Filas |
|---|---:|
| Entrada diagnosticada | 63 |
| Silver | 60 |
| Cuarentena final | 3 |
| Recuperadas de cuarentena diagnóstica | 10 |

Silver y cuarentena final suman exactamente la entrada. Silver conserva los valores Bronze junto a los tratados y las marcas de imputación, normalización o revisión; los motivos y acciones explican cada decisión. `en_cuarentena_diagnostico` es histórico y `en_cuarentena_final` indica la decisión de esta etapa. El reporte de calidad resume estas cifras.

Los patrones térmicos y de vida útil provienen de este dataset; no son límites universales. Los umbrales inferidos no son aptos para el KPI térmico observado.
