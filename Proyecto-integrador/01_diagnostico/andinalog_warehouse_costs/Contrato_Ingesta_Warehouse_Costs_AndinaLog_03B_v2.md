# Contrato de ingesta — Warehouse Costs — AndinaLog 03B v2

| Elemento | Acuerdo |
|---|---|
| Fuente | `andinalog_warehouse_costs.csv` |
| Granularidad | Un centro y periodo mensual |
| Clave natural | `centro_distribucion + periodo_mes` |
| Centros | Cochabamba, La Paz, Santa Cruz, Oruro y Tarija |
| Periodo | `AAAA-MM`; fecha de calendario mensual sin zona horaria |
| Rotación | Días, valor numérico mayor que cero |
| Montos | BOB, valores no negativos |
| Duplicidad | Conservar la primera fila completa y excluir copias incompletas posteriores |
| Imputación | No completar una copia que será excluida |

Los importes contables se conservan. Los cálculos derivados de Inventario sirven para comprobar coherencia, no para sustituirlos.
