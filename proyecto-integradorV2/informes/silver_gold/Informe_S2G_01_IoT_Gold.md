# Informe S2G 01 - AndinaLog IoT Gold

## Objetivo del producto Gold
Construir la tabla base del modelo predictivo de 03B: una fila por lectura de telemetria que
permita predecir si ocurrira una desviacion termica durante los proximos 60 minutos
(`desviacion_proximos_60min_flag`).

## Fuente utilizada
- Entrada unica: `datos/silver/andinalog_iot_telemetry_silver.csv`.
- No se realizo ningun join: IoT Silver contiene todas las variables minimas.
- Fuentes contextuales o excluidas: ninguna. El producto no necesita WMS Orders, flota, inventario,
  HR Drivers ni Bitacora.

## Compuerta previa y evidencia de la fuente
La skill de Gold exige como entrada minima IoT Silver con evidencia de conciliacion y de auditoria.
El notebook verifica esta compuerta con los archivos actuales, antes de construir Gold, y falla si
no se cumple.
- Bronze de origen: `datos/bronze/andinalog_iot_telemetry.csv` (28920 filas leidas en esta ejecucion).
- Silver derivado: `datos/silver/andinalog_iot_telemetry_silver.csv` (28448 filas leidas en esta ejecucion).
- Cuarentena de la etapa Bronze-Silver: `datos/quarantine/andinalog_iot_telemetry_quarantine.csv` (472 filas leidas en esta ejecucion).
- Informe de la etapa Bronze-Silver: `informes/bronze_silver/Informe_B2S_04_IoT_Telemetry.md`.
- Notebook de la etapa Bronze-Silver: `notebooks/bronze_silver/04_iot_telemetry/B2S_04_AndinaLog_IoT_Telemetry.ipynb`.
- Conciliacion verificada en esta ejecucion: Bronze 28920 = Silver 28448 + cuarentena 472.
- Conciliacion declarada en el informe de la etapa Bronze-Silver: Conciliacion: Bronze 28920 = Silver 28448 + cuarentena 472.
- Silver sin errores bloqueantes: 0. Silver sin lecturas imputadas: 0.
- Clave de lectura de Silver unica: True.
- La etapa Bronze-Silver de esta fuente tiene su propia auditoria; la evidencia citada arriba es la
  que sustenta el uso de Silver como base de este producto, y no se modifica ninguna decision de esa etapa.

## Unidad de observacion
Una lectura de telemetria. Una fila Gold por cada fila Silver, sin agregar ni muestreo.

## Esquema real encontrado en IoT Silver
- Filas: 28448. Columnas: 78.
- Viajes distintos: 1200.
- Ordenes distintos: 1200; camiones distintos: 30.
- Timestamp con sufijo `+00:00` en todas las filas, es decir UTC; rango de
  2026-08-01 04:10:00+00:00 a
  2026-08-31 15:11:00+00:00.
- Identificador de lectura disponible: `_fila_bronze`, unico en las 28448 filas.
- Frecuencia observada dentro de cada viaje: intervalo mediano
  30 minutos, con intervalos de 30, 60 y 90 minutos; ninguna lectura con
  intervalo no multiple de la cadencia. La cadencia no es completamente regular, por lo que las
  ventanas se resuelven con tiempo y no con desplazamiento fijo de filas.
- Vacios heredados: humedad ausente en 98 lecturas;
  temperatura ausente en 0 lecturas.
- Silver no trae errores bloqueantes ni lecturas imputadas.

## Clave de agrupacion
`viaje_id` (`viaje_id` con patron `^VIA-\d{5}$`).
Clave de lectura: `viaje_id` mas `timestamp`. Ninguna ventana cruza viajes,
ordenes o camiones.

## Definicion de cada predictor
| Predictor | Definicion |
|---|---|
| `temperatura_cabina_c` | Temperatura de la cabina en la lectura actual, tal como entrega Silver. |
| `humedad_cabina_pct` | Humedad relativa de la cabina en la lectura actual; nula si Silver la trae vacia, sin imputar. |
| `desviacion_termica_flag` | Indicador de desviacion termica observada en el instante t, tal como entrega Silver. |
| `temperatura_anterior` | Ultima lectura con timestamp estrictamente anterior a t dentro del mismo viaje, sin tolerancia de distancia; la primera lectura de cada viaje queda nula. |
| `variacion_temperatura_30min` | Busqueda temporal dentro del mismo viaje de la lectura mas reciente con timestamp en [t-45, t-30] minutos; variacion = temperatura actual menos temperatura de esa lectura. Sin lectura en ese rango la variacion queda nula. |

Columnas de control de ventana: `ts_temperatura_anterior` y `ts_base_variacion` guardan el instante
exacto de la lectura usada como antecedente, para demostrar que ningun predictor usa el futuro.

## Definicion exacta del objetivo
1 si existe al menos una desviacion_termica_flag igual a 1 en (t, t+60] dentro del mismo viaje; 0 solo con cobertura suficiente y sin desviacion; nulo sin cobertura suficiente.

La desviacion del instante t no se incluye como evento futuro: el intervalo evaluado es
`(t, t+60]` de forma estricta.

## Metodo para la variacion de 30 minutos
Busqueda temporal dentro del mismo viaje de la lectura mas reciente con timestamp en [t-45, t-30] minutos; variacion = temperatura actual menos temperatura de esa lectura. Sin lectura en ese rango la variacion queda nula.

La tolerancia de 15 minutos es la mitad de la cadencia observada de
30 minutos, de modo que la busqueda nunca alcanza una lectura mas antigua que t-30
y nunca puede tomar informacion posterior a t. Cuando el intervalo previo real es de 60 o 90
minutos, no existe lectura en el rango y la variacion queda nula, con el motivo registrado en
`motivo_variacion_30min`. No se usa `shift` fijo por filas ni `merge_asof` sin verificar la frecuencia.

## Criterio de cobertura futura
La ventana objetivo es evaluable si la ultima lectura futura dentro de (t, t+60] alcanza al menos t+45 minutos. Sin esa cobertura el objetivo queda nulo y la bandera en False.

Es decir, la ventana es evaluable cuando existe una lectura con instante entre `t+45` y `t+60`
minutos dentro del mismo viaje. Con cadencia de 30 minutos esto equivale a exigir la lectura de
`t+60`. Las lecturas finales de cada viaje quedan con objetivo nulo y
`ventana_objetivo_evaluable=False`; nunca se rellenan con cero.

## Conteos de filas y grupos
- Filas Silver: 28448. Filas Gold: 28448. Diferencia: 0.
- Viajes: 1200, iguales a los viajes de Silver.
- Columnas Silver: 78. Columnas Gold: 20.

## Distribucion del objetivo
- Ventanas evaluables: 25777.
- Ventanas no evaluables: 2671.
- Objetivo 1: 1300. Objetivo 0: 24477. Objetivo nulo: 2671.
- Prevalencia entre ventanas evaluables: 0.050433.
- Lecturas con desviacion actual: 940 de 28448.

## Cobertura de predictores derivados
- `temperatura_anterior` disponible en 27248 de 28448 lecturas.
- `variacion_temperatura_30min` disponible en 26933 de 28448 lecturas.
- `humedad_cabina_pct` ausente en 98 lecturas; se conserva nula, sin imputar.
- No se imputo ningun predictor ni identificador.

## Motivos de los nulos de predictores derivados
Todo nulo de un predictor derivado lleva su motivo en una columna propia; el motivo aparece solo
cuando el derivado falta, y el control final lo verifica.
| Columna de motivo | Motivo | Lecturas |
|---|---|---|
| `motivo_temperatura_anterior` | primera_lectura_del_viaje | 1200 |
| `motivo_variacion_30min` | primera_lectura_del_viaje | 1200 |
| `motivo_variacion_30min` | sin_lectura_en_[t-45,t-30]_minutos | 315 |
- `temperatura_anterior` nula en 1200 lecturas, todas con motivo.
- `variacion_temperatura_30min` nula en 1515 lecturas, todas con motivo.
- El motivo de cobertura del objetivo se conserva aparte en `calidad_estado` y `calidad_motivo`; no se
  mezcla con el motivo de los antecedentes.

## Uso posterior de la tabla: variables admitidas y prohibidas
- Predictores que el EDA y el modelo deben usar: temperatura_cabina_c, humedad_cabina_pct, desviacion_termica_flag, temperatura_anterior, variacion_temperatura_30min.
- Variable objetivo: desviacion_proximos_60min_flag.
- Columnas que NO deben usarse como variable de entrada, por ser de objetivo, control o auditoria:
  desviacion_proximos_60min_flag, ts_temperatura_anterior, ts_base_variacion, ventana_objetivo_evaluable, motivo_temperatura_anterior, motivo_variacion_30min, objetivo_coincide_con_silver, calidad_estado, calidad_motivo.
- No se debe usar "todas las columnas salvo el objetivo": las 9 columnas de objetivo,
  control y auditoria incorporarian informacion derivada del objetivo y producirian fuga temporal; el
  notebook verifica que el conjunto de predictores y el conjunto de columnas no admisibles son disjuntos.

## Controles contra fuga temporal
- `ts_temperatura_anterior` y `ts_base_variacion` son menores o iguales que `timestamp` en todas las lecturas.
- Los predictores no incluyen `desviacion_proximos_60min_flag` ni ninguna columna de objetivo, control o
  auditoria; la lista completa de columnas no admisibles esta en la seccion de uso posterior.
- El objetivo se recalculo con una forma independiente basada en `shift` y se comparo fila a fila.
- Toda ventana se resolvio dentro de `viaje_id`: la temperatura anterior y la base de
  variacion se recuperaron uniendo por viaje y por instante, y todas las ventanas se resolvieron contra su propio viaje.
- La tabla de roles y la lista de columnas no admisibles como entrada estan en la seccion de clasificacion.

## Clasificacion de columnas de Gold
```
                       columna                     rol  nulos                                      ejemplo
                  _fila_bronze   identificador_lectura      0                                            2
                     timestamp marca_tiempo_prediccion      0                    2026-08-11 18:11:00+00:00
                      viaje_id   identificador_entidad      0                                    VIA-00001
                      order_id  identificador_contexto      0                               ORD-2026-05710
                     camion_id  identificador_contexto      0                                       CAM-20
                   producto_id  identificador_contexto      0                                     PROD-045
          temperatura_cabina_c               predictor      0                                         2.19
            humedad_cabina_pct               predictor      0                                         72.6
       desviacion_termica_flag               predictor      0                                            0
          temperatura_anterior               predictor   1200                                         2.19
       ts_temperatura_anterior         control_ventana   1200                    2026-08-11 18:11:00+00:00
   variacion_temperatura_30min               predictor   1515                                         2.72
             ts_base_variacion         control_ventana   1515                    2026-08-11 18:11:00+00:00
   motivo_temperatura_anterior               auditoria      0                    primera_lectura_del_viaje
        motivo_variacion_30min               auditoria      0                    primera_lectura_del_viaje
desviacion_proximos_60min_flag                objetivo   2671                                          0.0
    ventana_objetivo_evaluable       control_cobertura      0                                         True
  objetivo_coincide_con_silver               auditoria      0                                         True
                calidad_estado               auditoria      0                           objetivo_evaluable
                calidad_motivo               auditoria      0 ventana_60min_observada_dentro_de_la_entidad
```

## Resultados de conciliacion
- Filas Silver = Filas Gold: 28448 = 28448; diferencia 0.
- Sin eliminacion de filas: no se uso `dropna`; las lecturas sin antecedente o sin cobertura se conservan.
- Sin multiplicacion: una fila Gold por lectura Silver, clave de lectura unica.
- CSV exportado con codificacion UTF-8 y sin indice; relectura verificada con 28448 filas y
  20 columnas, y tipos interpretables.
- Etiqueta de Gold identica a la que traia Silver en 25774 lecturas y
  distinta en 2674. La diferencia proviene de que Silver no expone
  la falta de cobertura como objetivo nulo, mientras que Gold si lo hace.

## Limitaciones
- La cadencia observada es de 30 minutos, por lo que la ventana de 30 minutos se resuelve con una sola
  lectura base y no con un promedio; los intervalos reales de 60 y 90 minutos dejan variacion nula.
- Las ultimas lecturas de cada viaje no tienen ventana de 60 minutos observada y quedan con objetivo nulo.
- La etiqueta describe asociacion temporal con una desviacion posterior; no afirma causalidad ni
  anticipa reglas de negocio, y no se usa para sancionar conductores.
- La evaluacion de cobertura admite una ventana observada de al menos 45 de los 60 minutos; lecturas
  adicionales dentro de la ventana pueden faltar en viajes con huecos.
- La tabla no incluye variables de otras fuentes; el alcance minimo de 03B no las exige.

## Rutas de los entregables
- Notebook: `notebooks/silver_gold/01_iot_gold/S2G_01_AndinaLog_IoT_Gold.ipynb`
- Gold: `datos/gold/andinalog_iot_modelado_gold.csv`
- Informe: `informes/silver_gold/Informe_S2G_01_IoT_Gold.md`

## Reproducibilidad
- Ejecucion UTC: 2026-09-25T17:11:58.718685+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- numpy: 2.5.3.
- El pipeline es determinista y no usa aleatoriedad, por lo que no se declara semilla.
- Ejecutar las celdas en orden desde la raiz del proyecto; `detectar_raiz()` busca la raiz entre el
  directorio actual y sus ancestros, o la variable de entorno `ANDINALOG_ROOT`.
- Los controles finales se aplican sobre el CSV Gold persistido, no solo sobre el dataframe en memoria.
