# Proyecto Integrador V2 AndinaLog 03B

## Alcance

Este proyecto corresponde al Grupo 06, empresa AndinaLog y subcaso 03B. V2 sigue los prompts S11 del docente para construir pipelines Bronze a Silver y productos Silver a Gold. No reutilizar automaticamente codigo, estructuras, salidas, conteos o conclusiones de V1. V3 realizara la comparacion y combinacion posterior.

## Skills del proyecto

- Usa `$andinalog-03b-bronze-silver` para procesar una fuente Bronze CSV, JSON o TXT.
- Usa `$andinalog-03b-silver-gold` para integrar fuentes Silver y producir detalle y agregado Gold.
- Usa `$andinalog-03b-v2-pipeline` para revisar orden, alcance y coherencia general.
- Usa `$andinalog-03b-auditoria` en modo Plan despues de Build para revisar entregables sin modificarlos.
- Usa `$andinalog-03b-iot-gold` para construir desde IoT Silver la tabla Gold con predictores temporales y objetivo futuro.
- Usa `$andinalog-03b-iot-eda` para ejecutar el EDA obligatorio sobre la tabla Gold.
- Usa `$andinalog-03b-iot-regresion-logistica` para dividir por viaje, entrenar y evaluar el modelo requerido.

## Alcance predictivo minimo confirmado

- El modelo obligatorio de 03B es una regresion logistica para predecir `desviacion_proximos_60min_flag`.
- La fuente minima es `andinalog_iot_telemetry.csv`; los cruces con otros datasets no son indispensables para el primer modelo.
- La unidad de observacion es una lectura de telemetria.
- Los predictores minimos son temperatura actual, humedad actual, desviacion termica actual, temperatura anterior y variacion de temperatura de los ultimos 30 minutos.
- La separacion de entrenamiento y prueba se realiza por viaje u orden.
- Ningun predictor puede utilizar lecturas o eventos posteriores al instante de prediccion.
- Despues de IoT Silver, el orden obligatorio es Gold, EDA y regresion logistica. Cada etapa entrega notebook ejecutado e informe MD.
- Usa `$andinalog-03b-iot-gold` para construir desde IoT Silver la tabla Gold con predictores temporales y objetivo futuro.
- Usa `$andinalog-03b-iot-eda` para ejecutar el EDA obligatorio sobre la tabla Gold.
- Usa `$andinalog-03b-iot-regresion-logistica` para dividir por viaje, entrenar y evaluar el modelo requerido.

## Alcance predictivo minimo confirmado

- El modelo obligatorio de 03B es una regresion logistica para predecir `desviacion_proximos_60min_flag`.
- La fuente minima es `andinalog_iot_telemetry.csv`; los cruces con otros datasets no son indispensables para el primer modelo.
- La unidad de observacion es una lectura de telemetria.
- Los predictores minimos son temperatura actual, humedad actual, desviacion termica actual, temperatura anterior y variacion de temperatura de los ultimos 30 minutos.
- La separacion de entrenamiento y prueba se realiza por viaje u orden para impedir que lecturas consecutivas de la misma entidad aparezcan en ambos conjuntos.
- Ningun predictor puede utilizar lecturas o eventos posteriores al instante de prediccion.
- Despues de IoT Silver, el orden obligatorio es Gold, EDA y regresion logistica. Cada etapa entrega notebook ejecutado e informe MD.

## Prompts y perfiles de fuente

- Usa prompts breves y estandarizados para Plan, Build y Auditoria. El usuario solo necesita indicar la fuente o producto, las rutas y los entregables esperados.
- Las reglas particulares de cada fuente Bronze viven en `andinalog-03b-bronze-silver/references/fuentes/` y no deben repetirse manualmente en cada prompt.
- La skill Bronze-Silver selecciona automaticamente el perfil por el nombre de la fuente y lo contrasta con el archivo real antes de proponer o implementar reglas.
- La skill de Auditoria vuelve a leer el mismo perfil para comprobar que Build lo aplico correctamente.
- Un perfil orienta la interpretacion del dominio; nunca sustituye la inspeccion del esquema, los valores ni la documentacion oficial disponible.

## Entregables

Por cada fuente Bronze entrega un notebook ejecutado, un informe MD, un CSV Silver y un CSV de cuarentena. Por cada producto Gold entrega un notebook ejecutado, un informe MD, un detalle Gold y un agregado Gold.

Para el producto predictivo minimo de IoT, Gold puede ser una sola tabla a nivel de lectura; no exige agregado ni join. El EDA y el modelo se entregan en notebooks e informes separados.

Para el producto predictivo minimo de IoT, Gold puede ser una sola tabla a nivel de lectura; no exige agregado ni join. El EDA y el modelo se entregan en notebooks e informes separados.

## Bronze a Silver

- Centraliza reglas en `config`.
- Implementa funciones y encadenalas con `df.pipe()`.
- Conserva valores originales y audita transformaciones e imputaciones.
- No uses `dropna()` para descartar silenciosamente errores.
- Calcula `calidad_estado` despues del tratamiento y la imputacion.
- Envia errores residuales a cuarentena.
- Distingue timestamps con hora, fechas calendario y periodos.
- Interpreta timestamps sin zona en `America/La_Paz` y conviertelos a UTC para Silver.
- Conserva fechas calendario, vencimientos y periodos sin desplazarlos por zona horaria.
- Concilia Bronze, Silver y cuarentena.
- Para JSON o TXT, adapta la conciliacion al cambio documentado de granularidad.

## Imputacion

Imputa solo con una regla reproducible, inequivoca, compatible con el dominio y declarada en `config`. Conserva valor original, valor tratado, bandera, metodo y motivo. No imputes identificadores ni presentes estimaciones como valores confirmados. No uses automaticamente media, mediana, moda, `ffill` o `bfill`. No uses informacion futura. Si una imputacion aprende parametros para modelado, ajustala solamente con entrenamiento.

## Integridad referencial

Distingue error intrinseco, error referencial bloqueante y falta de correspondencia informativa para enriquecimiento. Una observacion valida no pasa automaticamente a cuarentena porque otra fuente no tenga una clave utilizable. Documenta cobertura, no correspondencias y criterio de bloqueo.

## Archivos semiestructurados

- En JSON declara granularidad padre, granularidad hija y reglas de aplanamiento.
- En TXT declara codificacion, separador o patron, lineas fisicas y registros logicos.
- No uses modelos generativos para clasificar texto fila por fila.
- Conserva trazabilidad de objeto, posicion o numero de linea.

## Privacidad

Minimiza identificadores personales de HR Drivers y Bitacora. No muestres nombres, documentos, telefonos o correos en informes o salidas visibles. No uses variables laborales para sancionar conductores ni afirmes causalidad.

## Silver a Gold

- Usa fuentes Silver conciliadas.
- Declara granularidad, claves y cardinalidad.
- Valida joins y conserva no correspondencias.
- Configura agregaciones mediante `metricas_agg`.
- Genera detalle Gold y agregado Gold.
- Agrega antes de unir cuando sea necesario para evitar muchos a muchos.
- Registra cobertura y no correspondencias de cada join.
- Para productos predictivos, usa solamente informacion disponible hasta el instante de prediccion.
- Excluye datos personales sin necesidad analitica demostrada.

## Compuerta previa a Gold

Una fuente necesaria puede entrar a Gold cuando tiene notebook ejecutado, Silver, cuarentena, informe, conciliacion valida y auditoria sin hallazgos criticos o importantes. Documenta las fuentes utilizadas, contextuales y excluidas, junto con el motivo. No es obligatorio utilizar las nueve fuentes en cada producto Gold.

## Dominio

Celsius es la unidad canonica; Fahrenheit es convertible; Kelvin no es esperado operacionalmente. Los centinelas como `-999` no son mediciones. Una fecha sin zona explicita se interpreta como hora de Bolivia antes de convertirse a UTC.

## Calidad de entrega

Los informes deben usar los resultados del notebook entregado. Todos los notebooks deben conservar ejecuciones visibles, controles finales y una seccion de reproducibilidad.

## Auditoria

Audita cada fuente o producto una vez despues de Build. Una segunda auditoria se realiza solo cuando hubo correcciones criticas o importantes. Una entrega queda aprobada cuando no tiene hallazgos criticos ni importantes. La auditoria es de solo lectura; las correcciones se realizan posteriormente en Build.
