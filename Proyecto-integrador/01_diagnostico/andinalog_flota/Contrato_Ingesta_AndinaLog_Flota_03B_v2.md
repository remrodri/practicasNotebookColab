# Contrato de ingesta — AndinaLog 03B — Flota v2

Responsable: Grupo 06, rol 03B. Versión: 2. Fecha: 2026-09-22.

| Elemento | Acuerdo |
|---|---|
| Fuente | `datasets/AndinaLog_03B_Bronce/andinalog_flota.csv` |
| Formato | CSV UTF-8; primera fila con encabezados; se leen los campos como texto para no alterar Bronze |
| Frecuencia | No especificada por la fuente; no se supone una cadencia de actualización |
| Granularidad | Una fila Bronze; `fila_bronze` conserva su posición |
| Campos | camion_id, centro_distribucion_base, capacidad_kg, tipo_camion |
| Calidad | ID CAM-## único; centros Cochabamba, La Paz, Santa Cruz, Oruro o Tarija; tipo Seco o Refrigerado; capacidad numérica positiva en kg. Menos de 750 kg requiere revisión de ficha, sin cuarentena automática. |
| Diagnóstico | `diagnosticado` completo, subconjunto `cuarentena`, `reporte_calidad`; para cada campo, `_en_cuarentena` y `_motivo`. La bandera de fila es OR de las banderas de campo. El motivo puede describir revisión aunque la bandera sea falsa. El original no se modifica. |
| Tratamiento | Normalizar ID sin conflicto; conservar capacidad original y tratada; excluir copias posteriores y conflictos. No imputar tipo, centro ni capacidad. |
| Salida | Silver y cuarentena final particionan diagnosticado; `reporte_calidad` resume la etapa. Silver conserva Bronze, marcas diagnósticas, valores tratados y acciones. `en_cuarentena_diagnostico` identifica la decisión previa. |

750 kg es umbral de revisión, no mínimo normativo. La compatibilidad térmica de una asignación debe analizarse junto con el producto y el viaje.

La cuarentena de diagnóstico es un subconjunto del diagnosticado y no debe concatenarse con él. No hay catálogo externo obligatorio: las reglas están visibles en los notebooks y documentadas aquí.
