# Matriz de transformaciones B6 — Productos v2

| Variable | Entrada | Regla / acción | Salida + bandera | Prueba | Responsable | Versión | Fecha |
|---|---|---|---|---|---|---|---|
| `producto_id` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `nombre_producto` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `categoria_logistica` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `temperatura_conservacion_requerida_c` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `tolerancia_temperatura_c` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `precio_unitario_bob` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `costo_unitario_bob` | Bronze | ID PROD-### único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| Fila | Diagnóstico completo | Tratamiento: Normalizar ID sin conflicto. Inferir categoría únicamente con objetivo, tolerancia y vida útil observada concordantes; inferir objetivo faltante solo con categoría, tolerancia y vida útil concordantes. Marcar categoria_imputada y temperatura_imputada. Excluir duplicados posteriores y conflictos. | Silver o cuarentena final; `decision_tratamiento`, `motivo_cuarentena_final` | Silver + cuarentena final = 63 | Grupo 06 | v2 | 2026-09-22 |

Esta matriz resume las decisiones. Los motivos concretos por fila se encuentran en los CSV y la lógica ejecutable en los notebooks. Los patrones térmicos y de vida útil provienen de este dataset; no son límites universales. Los umbrales inferidos no son aptos para el KPI térmico observado.
