# Informe de diagnóstico — WMS Orders v2

Se diagnosticaron 7.550 filas sin modificar Bronze. La salida completa conserva los 14 campos originales y añade una bandera y un motivo por campo.

| Resultado | Filas |
|---|---:|
| Diagnosticadas | 7.550 |
| Con observaciones | 272 |
| Cuarentena diagnóstica | 194 |

Problemas principales: 50 copias exactas posteriores, claves recuperables con espacios o minúsculas, 20 fechas locales convertibles, 4 fechas imposibles, 15 cantidades solicitadas textuales, 80 cantidades entregadas ausentes y 15 tiempos reales negativos. Productos, camiones, centros y choferes tienen cobertura completa tras normalizar identificadores.

La cantidad entregada ausente se explica, pero no se imputa. La fila puede servir para atributos anteriores al despacho, aunque no para un KPI OTIF que necesite la cantidad observada.
