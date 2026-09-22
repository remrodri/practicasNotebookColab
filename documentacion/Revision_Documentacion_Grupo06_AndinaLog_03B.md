# Revisión de documentación oficial

## Grupo 06 — AndinaLog — Subcaso 03B

Fecha de revisión: 2026-09-22

## 1. Mandato del subcaso

El trabajo debe apoyar a Operaciones y Planificación de Datos para proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.

La decisión de negocio tiene tres partes conectadas:

1. Detectar y comparar excursiones térmicas por viaje, producto, camión y categoría logística.
2. Priorizar lotes con riesgo de vencimiento o merma.
3. Alertar sobre una posible desviación térmica durante los próximos 60 minutos.

## 2. Fuentes que corresponden al rol 03B

La documentación asigna nueve fuentes al subcaso 03B:

| Fuente | Granularidad esperada | Uso principal |
|---|---|---|
| `andinalog_wms_orders.csv` | Una orden despachada | Orden, viaje, producto, camión y atributos operativos del pedido |
| `andinalog_iot_telemetry.csv` | Una lectura temporal de un viaje | Temperatura, humedad y etiquetas térmicas |
| `andinalog_productos.csv` | Un producto | Categoría, temperatura objetivo y tolerancia |
| `andinalog_inventory_tracking.csv` | Un movimiento de lote | Permanencia, vencimiento y merma |
| `andinalog_flota.csv` | Un camión | Tipo, capacidad y centro base |
| `andinalog_warehouse_costs.csv` | Un centro y periodo | Rotación, costos y pérdidas por merma |
| `andinalog_hr_drivers.csv` | Un registro de chofer y centro | Carga, ausentismo y variables operativas de choferes |
| `andinalog_flota_eventos.json` | Un evento por camión | Configuración y alertas anteriores al instante de predicción |
| `andinalog_bitacora_choferes.txt` | Una observación de turno | Contexto semiestructurado de transporte |

`client_satisfaction`, `commercial_margins` y `clientes` pertenecen al rol 03A y no son necesarios para el mandato 03B.

## 3. Evidencias obligatorias

### Evidencia 1 — Excursiones térmicas

La unidad final es el viaje. Primero se debe agregar la telemetría por `viaje_id`, `order_id`, `camion_id` y `producto_id`. Después se incorporan Productos y Flota mediante uniones N a 1.

Resultados mínimos:

- temperatura promedio de cabina por viaje;
- número de lecturas con desviación por viaje;
- indicador de si el viaje tuvo al menos una desviación;
- porcentaje de viajes con desviación por categoría logística y tipo de camión.

No se debe calcular el porcentaje contando lecturas como si fueran viajes.

### Evidencia 2 — Vencimiento y merma

La unidad es el lote. `fecha_salida` vacía significa que el lote sigue en almacén y no constituye un error.

Resultados mínimos:

- días en almacén y días para vencer por lote;
- lotes aún en almacén;
- merma total por categoría logística;
- resumen del riesgo de vencimiento por categoría y, cuando corresponda, por centro.

Productos se une por `producto_id`. Warehouse Costs amplía la evidencia a rotación y pérdidas por centro.

### Evidencia 3 — Alerta térmica a 60 minutos

La unidad es una lectura de telemetría. Antes de crear rezagos o ventanas se debe ordenar por `viaje_id` y `timestamp`, y agrupar siempre por `viaje_id`.

Variables mínimas:

- desvío respecto al umbral térmico del producto;
- temperatura rezagada;
- pendiente entre lecturas;
- objetivo de desviación durante los próximos 60 minutos.

Se deben comprobar secuencia, cobertura y separación temporal para impedir que una variable use datos futuros.

## 4. Contratos predictivos oficiales

### Regresión

- **Decisión:** anticipar la magnitud de la posible desviación para decidir si interceptar el camión.
- **Unidad:** lectura de telemetría.
- **Horizonte:** próximos 60 minutos.
- **Objetivo:** máximo futuro de `abs(temperatura_cabina - temperatura_requerida) - tolerancia` dentro de la ventana del viaje.
- **Predictoras:** información disponible hasta el instante de predicción: lecturas actuales y anteriores, parámetros del producto, eventos anteriores de flota y atributos del pedido.

### Clasificación

- **Decisión:** alertar si el camión superará el umbral durante la próxima hora.
- **Unidad:** lectura de telemetría.
- **Horizonte:** próximos 60 minutos.
- **Objetivo:** `desviacion_proximos_60min_flag`.
- **Predictoras:** las mismas familias anteriores, limitadas al instante de predicción.

La variable objetivo nunca puede entrar como predictora. `desviacion_termica_flag` solo puede utilizarse si realmente está disponible en el instante de inferencia.

## 5. Reglas de integración

- Declarar la unidad de observación antes de cada unión.
- Normalizar claves y medir la cobertura de correspondencia.
- Usar `left` cuando se deba conservar la población principal y explicar los registros sin contraparte.
- Agregar cada tabla de hechos antes de unirla con otra tabla de hechos.
- Ordenar y agrupar las series temporales antes de `shift`, `rolling` o de construir el objetivo futuro.
- Separar hechos observados, imputaciones, inferencias, recomendaciones y afirmaciones causales.
- Conservar Bronze sin modificaciones y registrar regla, acción y cantidad de filas afectadas.

## 6. Estado actual del proyecto

Ya están diagnosticadas y tratadas cuatro de las nueve fuentes:

- IoT Telemetry;
- Productos;
- Inventory Tracking;
- Flota.

El EDA integrado actual cubre las tres evidencias básicas con esas cuatro fuentes. Los conteos Silver verificados son 28 677 lecturas IoT, 60 productos, 5 980 lotes y 30 camiones.

Para completar el alcance documental faltan cinco fuentes:

1. WMS Orders.
2. Warehouse Costs.
3. Flota Eventos JSON.
4. Bitácora de Choferes TXT.
5. HR Drivers.

La prioridad inmediata debe ser WMS Orders y Flota Eventos, porque aparecen directamente entre las predictoras del contrato a 60 minutos. Warehouse Costs es necesario para completar la evidencia de rotación y pérdidas por centro. Bitácora y HR Drivers deben diagnosticarse, tratarse y documentarse; su incorporación al modelo dependerá de su disponibilidad temporal y de si aportan información sin fuga ni datos personales innecesarios.

## 7. Entregables finales exigidos

El expediente final debe contener:

1. Un notebook ejecutado por tabla, con carga, preparación, EDA, modelo o aporte al dataset integrado y una celda de reproducibilidad.
2. Un único Excel con inventario de fuentes, diccionario multitabla en formato largo y muestra del dataset final integrado.
3. Informe técnico final en PDF, máximo seis páginas, incluida la declaración de uso de IA.
4. Presentación de máximo ocho diapositivas para diez minutos.
5. Matriz de trazabilidad desde el problema hasta la recomendación.
6. Plan de correcciones de la preentrega, si corresponde.

La defensa dura 30 minutos: 10 de exposición, 15 de preguntas individuales y 5 de cierre. Todos deben comprender el proyecto completo.

## 8. Secuencia recomendada

1. Completar diagnóstico y tratamiento de las cinco fuentes pendientes.
2. Crear el inventario y diccionario multitabla de las nueve fuentes.
3. Actualizar el EDA y las tres evidencias con los nuevos Silver.
4. Construir el dataset predictivo respetando el corte temporal.
5. Desarrollar y comparar baseline, regresión y clasificación.
6. Validar por tiempo o por viajes completos, evitando que lecturas del mismo viaje aparezcan en entrenamiento y prueba.
7. Analizar errores, estabilidad, incertidumbre y limitaciones.
8. Preparar matriz de trazabilidad, informe, presentación y declaración de IA.

## 9. Decisión práctica

El trabajo realizado hasta ahora es válido como base de preparación y EDA, pero todavía no representa el expediente completo solicitado. El siguiente bloque correcto es diagnosticar y tratar las cinco fuentes pendientes, comenzando por WMS Orders y Warehouse Costs, y luego Eventos, Bitácora y HR Drivers. Después debe actualizarse el EDA integrado y construirse formalmente los dos contratos predictivos.
