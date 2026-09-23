# Informe de tratamiento — WMS Orders v2

El tratamiento conserva los valores Bronze y genera columnas tratadas, acciones, motivos y aptitudes analíticas.

| Resultado | Filas |
|---|---:|
| Entrada | 7.550 |
| Silver | 7.468 |
| Cuarentena final | 82 |
| Recuperadas de cuarentena inicial | 112 |
| Aptas para KPI OTIF | 7.388 |
| Aptas para modelo previo al despacho | 7.468 |

Las 15 apariciones de `cincuenta` se convirtieron de forma determinista a 50 y quedaron marcadas. Dos filas se recuperaron completamente; 13 permanecen en cuarentena porque la cantidad entregada observada supera las 50 unidades solicitadas. Las 82 filas finales corresponden a copias exactas, fechas imposibles, contradicciones de cantidad o tiempos reales negativos. Las 80 cantidades entregadas ausentes permanecen vacías y marcadas; no se reconstruyen usando `otif_in_full`.

`apta_kpi_otif` controla indicadores que necesitan resultados completos. `apta_modelo_predespacho` controla la disponibilidad de atributos conocidos al despachar. Las variables posteriores al resultado no deben ingresar al modelo térmico.

