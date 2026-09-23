# Informe de Auditoría, Integración y EDA — AndinaLog 03B

**Grupo:** 06  
**Fecha:** 2026-09-23  
**Alcance:** seis fuentes Silver: IoT, Productos, Flota, WMS Orders, Inventory Tracking y Warehouse Costs.

## 1. Objetivo

Verificar que los seis Silver sean aptos para integración, medir la cobertura de los joins y construir las tres evidencias del subcaso 03B antes de iniciar el modelado.

## 2. Auditoría de entrada

| Fuente | Filas Silver | Clave única | Cuarentena final dentro de Silver | Apta para integrar |
|---|---:|---:|---:|---:|
| iot | 28,677 | Sí | 0 | Sí |
| productos | 60 | Sí | 0 | Sí |
| flota | 30 | Sí | 0 | Sí |
| inventario | 5,980 | Sí | 0 | Sí |
| wms | 7,468 | Sí | 0 | Sí |
| warehouse | 5 | Sí | 0 | Sí |


Los seis Silver superaron los controles de claves, nulos críticos y cuarentena final. Las fechas IoT se conservaron como hora de Bolivia.

## 3. Cobertura de joins

| Join | Cardinalidad | Filas antes | Filas después | Cobertura | Multiplicó filas |
|---|---|---:|---:|---:|---:|
| IoT → Productos | muchos a uno | 28,677 | 28,677 | 100.00% | No |
| IoT → Flota | muchos a uno | 28,677 | 28,677 | 100.00% | No |
| IoT → WMS Orders | muchos a uno | 28,677 | 28,677 | 99.67% | No |
| Inventario → Productos | muchos a uno | 5,980 | 5,980 | 100.00% | No |


Productos, Flota e Inventario alcanzaron cobertura completa. WMS Orders cubrió **99.67%** de las lecturas IoT; quedaron **95 lecturas** sin una orden Silver asociada. Estas filas se conservan mediante `left join` y deberán excluirse únicamente de modelos que requieran variables WMS completas, o tratarse con un indicador explícito de ausencia.

Ningún join multiplicó las filas de la población principal.

### Explicación de las 95 lecturas sin correspondencia en WMS Silver

Las 95 lecturas corresponden a cuatro viajes cuyas órdenes existen en WMS, pero quedaron en la cuarentena final del tratamiento y, por tanto, no forman parte de WMS Silver.

| Viaje | Orden | Lecturas IoT | Motivo de cuarentena en WMS |
|---|---|---:|---|
| `VIA-00558` | `ORD-2026-00813` | 24 | Tiempo real de entrega negativo (`-16,6` horas) |
| `VIA-00504` | `ORD-2026-02446` | 24 | Tiempo real de entrega negativo (`-54,9` horas) |
| `VIA-00698` | `ORD-2026-04343` | 23 | Cantidad entregada mayor que la solicitada (`299 > 50`) |
| `VIA-00368` | `ORD-2026-04539` | 24 | Cantidad entregada mayor que la solicitada (`70 > 50`) |

Las lecturas IoT no presentan este problema y permanecen válidas para el análisis térmico. La ausencia de correspondencia se debe exclusivamente a que el join utiliza WMS Silver, donde las cuatro órdenes fueron excluidas por inconsistencias en resultados posteriores a la entrega.

No se imputaron los tiempos reales ni las cantidades entregadas porque no existe una fuente independiente que permita conocer sus valores correctos. Usar el valor absoluto, la mediana, el tiempo prometido o igualar la cantidad entregada con la solicitada inventaría resultados y podría modificar artificialmente los indicadores OTIF.

La decisión actual es:

- mantener las cuatro órdenes en la cuarentena final de WMS;
- excluirlas de OTIF, tiempo real y análisis de cantidad entregada;
- conservar las 95 lecturas IoT en las evidencias térmicas;
- mantener visibles los valores WMS ausentes después del `left join`;
- no realizar imputaciones adicionales.

Esta diferencia de cobertura representa **4 de 1.200 viajes** y **95 de 28.677 lecturas IoT**. No invalida el EDA térmico, pero debe considerarse al seleccionar variables WMS para el dataset predictivo.

## 4. Evidencia 1 — excursiones térmicas

- Viajes totales: **1,200**.
- Viajes con al menos una lectura y un umbral observados: **1,100**.
- Viajes observados con una o más desviaciones: **311**.
- Porcentaje global observado: **28.27%**.

El porcentaje se calcula con viajes como denominador. Las temperaturas o umbrales imputados permanecen en la tabla para análisis, pero no forman parte del KPI térmico observado.

## 5. Evidencia 2 — vencimiento, merma, rotación y costos

- Lotes/movimientos Silver: **5,980**.
- Lotes todavía en almacén al corte: **0**.
- Lotes con salida posterior al vencimiento: **468**.
- Merma registrada: **53,308 unidades**.
- Centros-periodo de Warehouse Costs: **5**.
- Centros con información de inventario para el mismo periodo: **5**.

La pérdida contable `perdida_mermas_bob_tratado` y el valor estimado de merma calculado desde inventario se conservan como medidas distintas. No se reemplaza una por otra.

## 6. Evidencia 3 — alerta térmica a 60 minutos

- Lecturas conservadas: **28,677**.
- Viajes: **1,200**.
- Lecturas aptas para clasificación: **28,557**.
- Casos positivos de desviación futura: **1,322**.
- Prevalencia positiva: **4.63%**.
- Lecturas con objetivo continuo futuro calculable: **27,477**.

Las variables temporales se calcularon después de ordenar por viaje y hora. Los rezagos, pendientes y objetivos futuros nunca mezclan viajes.

## 7. Variables construidas

- Temperatura rezagada uno y dos pasos.
- Cambio de temperatura y pendiente por minuto.
- Media y máximo históricos de tres lecturas.
- Minutos desde el inicio del viaje.
- Desvío respecto al umbral del producto.
- Objetivo binario de desviación en los próximos 60 minutos.
- Máximo desvío térmico durante los próximos 60 minutos.
- Número de lecturas futuras disponibles en la ventana.
- Banderas de aptitud para clasificación y regresión.

## 8. Limitaciones

1. WMS no tiene correspondencia para 95 lecturas IoT.
2. El periodo disponible es corto y sintético; no demuestra estabilidad futura.
3. La clase positiva es minoritaria, por lo que accuracy no será una métrica suficiente.
4. JSON de eventos, bitácora TXT y HR Drivers quedaron fuera del alcance actual.
5. Las asociaciones entre categoría, camión y desviación no demuestran causalidad.
6. Los últimos instantes de cada viaje no siempre disponen de lecturas futuras suficientes para el objetivo continuo.

## 9. Validaciones superadas

- Los seis Silver son aptos para integrar.
- Las claves maestras son únicas.
- Ningún join multiplicó filas.
- Las tres evidencias conservan su granularidad.
- La Evidencia 3 mantiene una fila por lectura IoT.
- Los objetivos de regresión y clasificación están separados de los predictores.
- El notebook fue ejecutado de principio a fin sin errores.

## 10. Siguiente paso

Revisar la lista de predictores, congelar las reglas de exclusión por fuga y generar los datasets definitivos de regresión y clasificación. Después se aplicarán los contratos de S6, S7–S9 y S10 con separación temporal por viajes completos.
