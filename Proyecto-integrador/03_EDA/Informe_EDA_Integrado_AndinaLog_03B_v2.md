# Informe EDA integrado — AndinaLog 03B v2

Grupo 06. Fecha: 2026-09-22. El notebook usa los cuatro Silver v2.

| Silver | Filas |
|---|---:|
| IoT | 28 677 |
| Productos | 60 |
| Flota | 30 |
| Inventario | 5 980 |

Las uniones respetan la granularidad por producto, camión, viaje y lote; se agregan datos antes de cruzar hechos que comparten una clave. Hay 26 183 lecturas IoT aptas para KPI térmico observado, 1 100 viajes con al menos una lectura observada y 311 con desviación. Se registran 17 viajes con posible incompatibilidad producto/camión, sin asumir causalidad. En inventario hay 18 vencimientos imputados, excluidos del KPI observado. En el conjunto elegible para alerta temprana hay 24 892 lecturas con rezago de 30 minutos y 664 objetivos positivos entre las 24 070 lecturas aún dentro de tolerancia. Las fechas de inventario son fechas de calendario; los timestamps IoT tratados corresponden a hora de Bolivia.

Las salidas inferidas se identifican por sus banderas y no se mezclan con hechos observados en indicadores que requieren observación.
