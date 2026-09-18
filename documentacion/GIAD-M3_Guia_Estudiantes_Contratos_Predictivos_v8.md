**GIAD · Módulo 3 · Proyecto Integrador — guía para estudiantes**

**Cómo definir un contrato predictivo**

_Método y doce ejemplos resueltos sobre los datos sintéticos v8_

**Fecha:** 17 de septiembre de 2026

**Para:** los seis equipos del Proyecto Integrador (01A/01B AITSA, 02A/02B RedNexo, 03A/03B AndinaLog)

**Datos:** sintéticos v8 — verificado directamente sobre los archivos Silver reales, no solo sobre el diccionario de datos

# **Cómo usar esta guía**

Esta guía no reemplaza el trabajo de tu equipo. Cada uno de los seis subcasos del Proyecto Integrador ya trae, en el dossier del docente, dos contratos por definir: uno de regresión y uno de clasificación. Lo que sigue muestra, con los doce contratos oficiales ya resueltos y verificados sobre los datos sintéticos v8, **cómo se razona** cada uno de los cinco elementos que todo contrato predictivo necesita: **Decisión, Unidad de observación, Horizonte, Objetivo Y y Predictoras X**.

Úsala como modelo de razonamiento, no como una plantilla para copiar y pegar: si tu equipo decide acotar el problema de otra forma, está bien, siempre que puedas defender tus cinco elementos con la misma precisión que se exige aquí. La sección final trae una plantilla en blanco para que definas los tuyos.

# **El método: las 5 preguntas que definen un contrato predictivo**

Antes de escribir una sola línea de código, todo contrato predictivo —el tuyo o cualquiera de estos doce— se puede y se debe responder con cinco preguntas. Si no puedes responder alguna con precisión y contra los datos reales, tu contrato todavía no está listo.

**1\. Decisión**

¿Qué decisión de negocio cambia según el resultado de la predicción? Una predicción sin una decisión asociada no es un contrato, es un ejercicio académico.

**_Error común:_** _describir una métrica ("predecir el MTTR") sin decir para qué decisión concreta se usa esa cifra._

**2\. Unidad de observación**

¿Sobre qué entidad se hace UNA predicción? ¿A qué grano corresponde exactamente una fila de tu tabla de entrenamiento (un proyecto, un ticket, un abonado, una zona-tecnología-mes, una lectura de telemetría)?

**_Error común:_** _declarar una unidad de observación más fina de lo que los datos realmente permiten (p. ej. "zona-tecnología-período" cuando la tabla real no tiene columna de período)._

**3\. Horizonte**

¿En qué instante se hace la predicción, y qué cuenta como "antes" de ese instante? ¿Hasta cuándo se extiende el resultado que quieres anticipar?

**_Error común:_** _usar como predictora (X) un dato que en la práctica solo se conoce después del instante de predicción — eso no es una X, es una fuga de datos._

**4\. Objetivo Y**

¿Existe como campo literal o hay que construirlo con una fórmula? Si hay que construirlo, ¿la fórmula está verificada contra los datos reales? ¿Qué cobertura tiene, y esa cobertura es aleatoria o sesgada?

**_Error común:_** _confiar en la documentación del diccionario de datos sin correr el código sobre el archivo real (en v8, churn_risk está documentado como "Decimal" pero en los datos reales es un entero 0/1)._

**5\. Predictoras X**

¿Cada X existe, en qué tabla vive, y se puede filtrar para que sea estrictamente anterior al horizonte? ¿Alguna X vive en la misma fuente que tu propio Y y ocurre después del hecho que quieres predecir (circularidad)?

**_Error común:_** _arrastrar sin darse cuenta una columna que en el fondo es una versión disfrazada del propio Y (p. ej. usar la satisfacción del cliente para predecir el costo de una devolución registrada en la misma evaluación)._

# **Qué cambió de los datos v7 a los v8**

Los datos sintéticos se ampliaron de la versión 7 a la versión 8 específicamente para resolver vacíos que en su momento obligaban a recortar o replantear varios de los doce contratos. Esto es lo que cambió, verificado directamente sobre los archivos Silver reales:

| **Qué cambió**                                                                                                                                                   | **Contrato(s) que beneficia**           | **Verificado en los datos v8**                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| AITSA ahora tiene fecha por registro: fecha_fin (proyectos), fecha_factura (facturación), fecha_asignacion (asignaciones), fecha_apertura/fecha_cierre (tickets) | 01A y 01B (regresión y clasificación)   | 100 proyectos con fecha_fin ≥ fecha_inicio; 100% de fecha_asignacion y de fecha_apertura caen dentro de la ventana de vida de su proyecto |
| rednexo_opex_costs pasa de una foto de 21 filas a un panel de 378 filas (18 meses × 21 combinaciones zona-tecnología)                                            | 02A-regresión                           | confirmado: 21 combinaciones × 18 períodos = 378 filas exactas                                                                            |
| rednexo_nodos pasa de 15 a 30 nodos, cubriendo las 21 combinaciones zona-tecnología (incluida Sacaba)                                                            | 02A y 02B (las X que dependen de nodos) | confirmado: 21/21 combinaciones cubiertas — cero valores faltantes al unir con opex_costs o crm_billing                                   |
| andinalog_client_satisfaction sube de 20% a 49% de cobertura, con un muestreo sesgado y documentado                                                              | 03A-regresión                           | confirmado: 3.696 de 7.500 pedidos (49,3%); probabilidad de evaluación 87,5% si el pedido incumplió OTIF vs. 39,5% si lo cumplió          |
| Sin cambios: andinalog_iot_telemetry, andinalog_wms_orders, rednexo_support_log, rednexo_network_performance, rednexo_nms_eventos                                | 02B y 03B                               | mismos campos y la misma cobertura que en v7                                                                                              |

**Lo que NO cambió: la naturaleza de las etiquetas**

churn_risk sigue siendo un entero 0/1 generado por una regla del propio simulador, no una baja real observada; el flag de desviación térmica de AndinaLog sigue viniendo precomputado. Verificar el **tipo real** de un campo contra los datos, y no solo contra el diccionario, sigue siendo obligatorio incluso en v8.

# **Doce contratos resueltos sobre los datos v8**

## **01A — AITSA, Gerencia General y Dirección Estratégica**

## **03B — AndinaLog, Operaciones y Planificación de Datos**

**Contrato de regresión**

**Decisión:** Anticipar la magnitud de una posible desviación térmica de la carga, para decidir si interceptar el camión.

**Unidad de observación:** Lectura de telemetría (andinalog_iot_telemetry, 28.800 lecturas, 24 por viaje — sin cambios frente a v7).

**Horizonte:** Próximos 60 minutos, como el máximo (rolling-max) agrupado por viaje_id y ordenado por timestamp.

**Objetivo Y:** máximo en la ventana de desvio_respecto_umbral_c = |temperatura_cabina_c − temperatura_conservacion_requerida_c| − tolerancia_temperatura_c (fórmula verificada, no un campo literal).

**Predictoras X:** lecturas actuales/previas de iot_telemetry; temperatura_conservacion_requerida_c y tolerancia_temperatura_c del producto; eventos de flota previos; atributos del pedido.

**Contrato de clasificación**

**Decisión:** Alertar si un camión va a superar el umbral térmico en la próxima hora, para decidir un desvío o intercepción.

**Unidad de observación:** Lectura de telemetría (mismo archivo).

**Horizonte:** Próximos 60 minutos.

**Objetivo Y:** desviacion_proximos_60min_flag — verificado en v8: campo ya precomputado, con una tasa de 4,6% (antes 3,9% en v7; el desplazamiento es por la nueva secuencia aleatoria del generador, no por un cambio de diseño).

**Predictoras X:** Las mismas de la regresión.

**Exclusión (fuga):** desviacion_proximos_60min_flag (es el propio Y) y desviacion_termica_flag solo si no está disponible en el instante de predicción.

# **Errores comunes al definir un contrato predictivo**

**1\. Confundir "el campo ya existe" con "el campo está disponible en el momento correcto".** En 01B, aunque fecha_asignacion ya existe en v8, solo la mitad de los cruces válidos quedan realmente antes de la apertura del ticket.

**2\. No declarar la dirección del sesgo cuando la cobertura es parcial.** En 03A, el 49,3% de cobertura no es aleatorio: sobre-representa pedidos problemáticos (MNAR), así que un promedio simple sesga el resultado en una dirección conocida.

**3\. Unir tablas de distinta granularidad sin agregar antes.** En 02A, el panel mensual de OPEX (18 filas por zona-tecnología) puede producir fan-out si se une directo contra una tabla de una fila por combinación.

**4\. Circularidad: usar como X un dato que vive en la misma fuente que tu propio Y y ocurre después del hecho.** En 03A, la satisfacción del cliente y el costo de devolución se registran en la misma evaluación posterior al despacho.

**5\. Confiar en el diccionario de datos en vez de verificar el tipo real del campo.** churn_risk está documentado como "Decimal" pero en los datos reales es un entero 0/1.

**6\. Igualar "fecha de cierre formal" con "última fecha de actividad".** En 01A, el 16,8% de las facturas llegan después de fecha_fin.

# **Plantilla para tu propio contrato**

Copia esta tabla y complétala para cada uno de los dos contratos de tu subcaso. Si no puedes llenar un campo con una frase concreta y verificable contra los datos, tu contrato todavía no está listo.

| **Campo**             | **Tu respuesta** |
| --------------------- | ---------------- |
| Decisión              | …                |
| Unidad de observación | …                |
| Horizonte             | …                |
| Objetivo Y            | …                |
| Predictoras X         | …                |
| Exclusión (fuga)      | …                |