# Informe de diagnóstico — Warehouse Costs v2

Se conservaron las seis filas Bronze. La clave Tarija y `2026-08` aparece dos veces. La segunda fila repite pérdidas y costo, pero carece de rotación, por lo que se clasifica como copia incompleta posterior.

| Resultado | Filas |
|---|---:|
| Diagnosticadas | 6 |
| Cuarentena diagnóstica | 1 |
| Claves centro-periodo repetidas | 2 filas |

Los cinco centros y el periodo son válidos. Rotación y montos son positivos. Los valores de rotación coinciden, con diferencias de redondeo, con el promedio observado en Inventario Silver.
