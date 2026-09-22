# Matriz de transformaciones B6 — Flota v2

| Variable | Entrada | Regla / acción | Salida + bandera | Prueba | Responsable | Versión | Fecha |
|---|---|---|---|---|---|---|---|
| `camion_id` | Bronze | ID CAM-## único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `centro_distribucion_base` | Bronze | ID CAM-## único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `capacidad_kg` | Bronze | ID CAM-## único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `tipo_camion` | Bronze | ID CAM-## único | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| Fila | Diagnóstico completo | Tratamiento: Normalizar ID sin conflicto; conservar capacidad original y tratada; excluir copias posteriores y conflictos. No imputar tipo, centro ni capacidad. | Silver o cuarentena final; `decision_tratamiento`, `motivo_cuarentena_final` | Silver + cuarentena final = 32 | Grupo 06 | v2 | 2026-09-22 |

Esta matriz resume las decisiones. Los motivos concretos por fila se encuentran en los CSV y la lógica ejecutable en los notebooks. 750 kg es umbral de revisión, no mínimo normativo. La compatibilidad térmica de una asignación debe analizarse junto con el producto y el viaje.
