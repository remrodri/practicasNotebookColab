# Informe EDA 01 - AndinaLog IoT Gold

## Objetivo del EDA

Analizar de forma exploratoria la tabla Gold construida para el modelo predictivo de 03B,
que busca identificar si una lectura de telemetria tendra una desviacion termica durante
los proximos 60 minutos (`desviacion_proximos_60min_flag`).

Este EDA describe, no construye: no reconstruye el objetivo, no imputa valores, no elimina
registros y no entrena ningun modelo. Las cifras de este informe corresponden a la ejecucion
del notebook entregada en la seccion de reproducibilidad.

## Fuente y ruta de Gold

- Entrada unica: `datos/gold/andinalog_iot_modelado_gold.csv`, leido en modo solo lectura.
- SHA-256 del archivo al inicio y al cierre de la ejecucion:
  `f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479` (identico en ambos
  momentos: el EDA no modifica Gold).
- El Gold fue producido por `notebooks/silver_gold/01_iot_gold/S2G_01_AndinaLog_IoT_Gold.ipynb`
  e informado en `informes/silver_gold/Informe_S2G_01_IoT_Gold.md`. Ese informe se usa solo
  como referencia de conciliacion; ninguna cifra de este informe se copia de el.

## Unidad de observacion

Una lectura de telemetria: cada fila corresponde al instante `timestamp` dentro de un viaje.
No hay agregacion, muestreo ni duplicacion intencional.

- Clave de lectura: `viaje_id` + `timestamp`.
- Filas duplicadas en la clave de lectura: 0.
- `_fila_bronze` unico: True.
- Viajes distintos: 1200. Ordenes distintas: 1200. Camiones distintos: 30. Productos distintos: 60.
- Ordenes por viaje (maximo): 1. Camiones por viaje (maximo): 1.
- Viajes fuera del patron `^VIA-\d{5}$`: 0.

## Fecha de ejecucion

- 2026-09-25T19:28:38.739847+00:00 (celda de configuracion).
- 2026-09-25T19:28:43.693219+00:00 (celda de reproducibilidad).

## Forma de la tabla

- Filas: 28448. Columnas: 20.
- Inventario con rol, tipo, nulos, valores unicos y ejemplo de cada columna: 0 columnas con
  rol sin definir.
- Tipos presentes: `bool` (2 columnas), `float64` (5), `int64` (2), `str` (11).
- Identificadores: `_fila_bronze` (int64), `viaje_id`, `order_id`, `camion_id`, `producto_id`
  (texto). No se usan como variables numericas en ninguna tabla ni en la matriz de correlaciones.

## Ventana temporal y cadencia

- Timestamp minimo (UTC): 2026-08-01 04:10:00+00:00.
- Timestamp maximo (UTC): 2026-08-31 15:11:00+00:00.
- Timestamps no parseables: 0. Sufijo de zona horaria en el texto original: `+00:00` en todos.
- Intervalos internos por viaje: 30 minutos en 26933 casos, 60 minutos en 313 y 90 minutos
  en 2. Intervalo mediano: 30 minutos.
- Lecturas por viaje: minimo 21, maximo 24, mediana 24. Frecuencia de tamanos: 21 -> 7 viajes,
  22 -> 30, 23 -> 271, 24 -> 892. Ningun viaje supera 24 lecturas.

## Control de granularidad y de multiplicacion

- Filas leidas en esta ejecucion: 28448.
- Filas Silver declaradas en el informe Gold: 28448. Diferencia: 0.
- Filas Gold declaradas en el informe Gold: 28448. Diferencia con lo leido: 0.
- Viajes leidos: 1200, iguales a los declarados.
- Cobertura del objetivo leida: 25777 evaluables y 2671 no evaluables, iguales a las declaradas.
- Conclusiones: una fila Gold por lectura Silver, sin join, sin agregado y sin fan-out.
  No hay diferencias ni duplicados ocultos.

## Duplicados

| Control | Resultado |
|---|---|
| Duplicados exactos (fila completa) | 0 |
| Duplicados en la clave de lectura `viaje_id` + `timestamp` | 0 |
| Duplicados en `_fila_bronze` | 0 |
| Lecturas repetidas en el mismo viaje y timestamp | 0 |

Ninguna fila se elimina: los duplicados se reportan, no se corrigen en el EDA.

## Faltantes por columna

| Columna | Nulos | No nulos | % faltantes |
|---|---|---|---|
| motivo_temperatura_anterior | 27248 | 1200 | 95.7818 |
| motivo_variacion_30min | 26933 | 1515 | 94.6745 |
| desviacion_proximos_60min_flag | 2671 | 25777 | 9.3891 |
| variacion_temperatura_30min | 1515 | 26933 | 5.3255 |
| ts_base_variacion | 1515 | 26933 | 5.3255 |
| temperatura_anterior | 1200 | 27248 | 4.2182 |
| ts_temperatura_anterior | 1200 | 27248 | 4.2182 |
| humedad_cabina_pct | 98 | 28350 | 0.3445 |

- Columnas con al menos un faltante: 8. Total de celdas faltantes: 62380.
- Faltantes en columnas de identificadores: 0.

## Clasificacion de faltantes: esperados e inesperados

| Columna | Tipo | Motivo declarado | Filas |
|---|---|---|---|
| temperatura_anterior | esperado | primera lectura del viaje, sin lectura previa | 1200 |
| variacion_temperatura_30min | esperado | primera lectura del viaje, sin lectura previa | 1200 |
| variacion_temperatura_30min | esperado | sin lectura en [t-45, t-30] min (intervalo previo de 60 o 90 min) | 315 |
| humedad_cabina_pct | esperado (heredado de Silver) | vacio de origen, conservado sin imputar | 98 |
| desviacion_proximos_60min_flag | esperado | ventana futura de 60 min no evaluable dentro del viaje | 2671 |
| ts_temperatura_anterior | esperado (refleja el derivado) | sin temperatura anterior no hay instante de referencia | 1200 |
| ts_base_variacion | esperado (refleja el derivado) | sin variacion no hay instante base | 1515 |
| motivo_temperatura_anterior | esperado (nulo cuando el derivado existe) | el motivo solo existe cuando el derivado falta | 27248 |
| motivo_variacion_30min | esperado (nulo cuando el derivado existe) | el motivo solo existe cuando el derivado falta | 26933 |

- Suma de faltantes de temperatura anterior con motivo: 1200 de 1200.
- Suma de faltantes de variacion con motivo: 1515 de 1515 (1200 + 315).
- Faltantes inesperados (sin causa declarada): 0.
- Los nulos del objetivo coinciden con `ventana_objetivo_evaluable == False` en 28448 de
  28448 filas.
- No se imputo ningun valor y no se elimino ninguna fila.

## Variables categoricas y banderas

| Variable | Frecuencia |
|---|---|
| ventana_objetivo_evaluable | True 25777 (90.61 %), False 2671 (9.39 %) |
| desviacion_termica_flag | 0: 27508 (96.70 %), 1: 940 (3.30 %) |
| calidad_estado | objetivo_evaluable 25777, objetivo_no_evaluable 2671 |
| calidad_motivo | ventana_60min_observada_dentro_de_la_entidad 25777, sin_cobertura_futura_hasta_60min_en_la_entidad 2671 |
| objetivo_coincide_con_silver | True 25774 (90.60 %), False 2674 (9.40 %) |
| motivo_temperatura_anterior | primera_lectura_del_viaje 1200 (4.22 %), nulo 27248 (95.78 %) |
| motivo_variacion_30min | primera_lectura_del_viaje 1200 (4.22 %), sin_lectura_en_[t-45,t-30]_minutos 315 (1.11 %), nulo 26933 (94.67 %) |
| desviacion_proximos_60min_flag (poblacion total) | 0: 24477 (86.04 %), 1: 1300 (4.57 %), nulo: 2671 (9.39 %) |

## Revision de los predictores minimos

Sobre la poblacion Gold completa (28448 filas):

| Predictor | Validos | Faltantes | % faltantes | Media | Desv. est. | Minimo | P01 | P25 | Mediana | P75 | P99 | Maximo | Unidad |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| temperatura_cabina_c | 28448 | 0 | 0.0 | 8.3488 | 14.0397 | -21.63 | -19.23 | 3.44 | 15.5706 | 20.04 | 24.18 | 29.69 | Celsius |
| humedad_cabina_pct | 28350 | 98 | 0.3445 | 61.4729 | 15.4583 | 20.70 | 33.80 | 48.00 | 60.3000 | 75.10 | 91.20 | 100.00 | % HR |
| desviacion_termica_flag | 28448 | 0 | 0.0 | 0.0330 | 0.1788 | 0.00 | 0.00 | 0.00 | 0.0000 | 0.00 | 1.00 | 1.00 | indicador 0/1 |
| temperatura_anterior | 27248 | 1200 | 4.2182 | 8.3571 | 14.0370 | -21.63 | -19.23 | 3.44 | 15.6200 | 20.04 | 24.2253 | 29.69 | Celsius |
| variacion_temperatura_30min | 26933 | 1515 | 5.3255 | -0.0034 | 2.1017 | -11.28 | -5.75 | -1.14 | -0.0200 | 1.13 | 5.7068 | 12.7811 | Celsius por 30 min |

Controles adicionales:

- Valores centinela -999.0 en temperatura: 0. En variacion: 0.
- Humedad fuera del rango 0 a 100: 0. Humedad exactamente en 100 %: 5 lecturas, tratadas
  como limite fisico de medicion, no como error ni centinela.
- Lecturas con desviacion termica actual: 940 de 28448 (3.30 %).
- Lecturas con temperatura negativa (regimen de congelado): 5013.
- Lecturas con variacion absoluta mayor a 5.0 C: 891; se conservan y se describen, no se recortan.
- Distribucion por regimen de temperatura (cortes en -10 C y 10 C, configurados en `config`):
  congelado (<-10 C) 4932 lecturas con 169 desviaciones actuales (3.43 %); templado
  (-10 a 10 C) 8995 con 378 (4.20 %); calido (>10 C) 14521 con 393 (2.71 %).

## Poblacion analitica del objetivo

- Poblacion Gold original: 28448 filas, conservada sin cambios.
- Filtro explicito aplicado: `ventana_objetivo_evaluable == True`. No se uso `dropna()`.
- Filas que entran: 25777. Filas que quedan fuera: 2671.
- Exclusion explicada: las 2671 filas excluidas tienen la ventana futura de 60 minutos no
  observada dentro del viaje; su `calidad_motivo` es
  `sin_cobertura_futura_hasta_60min_en_la_entidad` en las 2671.
- Objetivo nulo en las 2671 filas excluidas y no nulo en las 25777 incluidas.
- El objetivo contiene unicamente 0 y 1 dentro de la poblacion analitica: True.
- 25777 + 2671 = 28448: Gold original intacto.

## Distribucion del objetivo y desbalance de clases

| Clase | Lecturas | Porcentaje | Viajes con la clase | Lecturas por viaje (medio) |
|---|---|---|---|---|
| 0 (sin desviacion futura) | 24477 | 94.9567 % | 1200 | 20.398 |
| 1 (con desviacion futura) | 1300 | 5.0433 % | 338 | 3.846 |

- Prevalencia de desviacion futura: 0.050433.
- Razon mayoria/minoria: 18.8285.
- Viajes con alguna ventana evaluable: 1200. Con al menos una ventana positiva: 338.
  Sin ninguna ventana positiva (todas sus ventanas evaluables son 0): 862, verificado de
  forma independiente sumando los positivos por viaje. Con al menos una ventana negativa:
  1200. Los 1200 viajes aportan alguna fila no evaluable.
- Positivos por viaje: minimo 1, maximo 10, mediana 2.0. Viajes con un solo positivo: 12
  de 338. Viajes con menos de 15 lecturas evaluables: 0.
- Prevalencia por banda de temperatura de cabina:
  congelado 4448 lecturas con 274 positivos (6.160 %); templado 8154 con 556 (6.819 %);
  calido 13175 con 470 (3.567 %).

El desbalance se describe y no se corrige: no hay submuestreo, ponderacion ni cambio de
etiqueta. El desbalance por si solo no permite afirmar que el modelo sera bueno o malo.

## Estadisticas de predictores por clase del objetivo

Poblacion analitica (n = 25777):

| Predictor | Clase | n | Media | Desv. est. | Mediana |
|---|---|---|---|---|---|
| temperatura_cabina_c | 0 | 24477 | 8.5608 | 14.0317 | 16.73 |
| temperatura_cabina_c | 1 | 1300 | 4.9381 | 13.4393 | 5.17 |
| humedad_cabina_pct | 0 | 24395 | 61.0615 | 15.4484 | 59.0 |
| humedad_cabina_pct | 1 | 1295 | 68.8364 | 14.0416 | 72.4 |
| desviacion_termica_flag | 0 | 24477 | 0.0152 | 0.1222 | 0.0 |
| desviacion_termica_flag | 1 | 1300 | 0.4185 | 0.4935 | 0.0 |
| temperatura_anterior | 0 | 23302 | 8.6165 | 14.0110 | 16.755 |
| temperatura_anterior | 1 | 1284 | 4.2004 | 13.5157 | 4.605 |
| variacion_temperatura_30min | 0 | 23033 | -0.0400 | 2.0717 | -0.03 |
| variacion_temperatura_30min | 1 | 1273 | 0.7006 | 2.6830 | 0.22 |

Faltantes por predictor dentro de la poblacion analitica: `temperatura_cabina_c` 0,
`humedad_cabina_pct` 87, `desviacion_termica_flag` 0, `temperatura_anterior` 1191 y
`variacion_temperatura_30min` 1471. Filas con al menos un predictor continuo faltante: 1554;
esta cifra es un informe de calidad, **no** una cantidad de filas excluidas: esas filas no
salen del conjunto de datos y cada grafico declara su propia exclusion sobre la columna que
necesita (87 en el grafico 3 y 1471 en el grafico 5).

## Correlaciones descriptivas entre predictores numericos

Pearson, poblacion analitica, sin identificadores y sin el objetivo:

| | temperatura_cabina_c | humedad_cabina_pct | desviacion_termica_flag | temperatura_anterior | variacion_temperatura_30min |
|---|---|---|---|---|---|
| temperatura_cabina_c | 1.0000 | -0.6435 | -0.0254 | 0.9886 | 0.0761 |
| humedad_cabina_pct | -0.6435 | 1.0000 | 0.1035 | -0.6435 | 0.0018 |
| desviacion_termica_flag | -0.0254 | 0.1035 | 1.0000 | -0.0420 | 0.1025 |
| temperatura_anterior | 0.9886 | -0.6435 | -0.0420 | 1.0000 | -0.0748 |
| variacion_temperatura_30min | 0.0761 | 0.0018 | 0.1025 | -0.0748 | 1.0000 |

Pares con correlacion absoluta mayor o igual a 0.50: temperatura actual con humedad
(-0.6435), temperatura actual con temperatura anterior (0.9886) y humedad con temperatura
anterior (-0.6435). Los predictores estan fuertemente correlacionados entre si, por lo que
su lectura conjunta no puede atribuirse a una sola variable.

## Resumen por viaje

- Viajes incluidos: 1200. Lecturas por viaje en la poblacion analitica: minimo 16, maximo 22,
  mediana 22 (media 21.4808).
- Ventanas positivas por viaje: media 1.0833, maximo 10, 862 viajes con cero.
- Temperatura media por viaje: media 8.3531 C, minimo -18.4170 C, maximo 21.8890 C.
- Prevalencia por viaje: media 0.0502, maximo 0.4545; 862 viajes con prevalencia 0.
- Viajes con mayor numero de ventanas positivas: VIA-00087 (22 lecturas, 10 positivas),
  VIA-00593 (22, 10) y VIA-00792 (22, 9).
- Verificacion 1 a 1 entre viaje y orden: True.

## Graficos: que pregunta responde cada uno y que se observo

Todos los graficos se generaron con titulo, nombres de ejes con unidad, leyenda, paleta
consistente, `tight_layout()` y textos anotativos.

### Grafico 1. Countplot de `desviacion_proximos_60min_flag`

- Filas usadas: 25777 ventanas evaluables. Las 2671 no evaluables quedan fuera por diseno y
  asi lo declara el titulo.
- Pregunta: que tan frecuentes son las desviaciones futuras.
- Observado: clase 0 = 24477 lecturas (94.96 %), clase 1 = 1300 lecturas (5.04 %);
  prevalencia 0.050433.
- Interpretacion: la proporcion de ventanas con desviacion posterior es baja y convierte el
  desbalance en el rasgo dominante del objetivo.
- Limitacion: el conteo por lectura no equivale al conteo por viaje; los viajes aportan
  entre 0 y 10 ventanas positivas y 862 de 1200 viajes no aportan ninguna.

### Grafico 2. Histplot de temperatura actual con `hue` del objetivo

- Filas usadas: 25777. Excluidas por temperatura nula: 0.
- Pregunta: las desviaciones futuras parten de temperaturas diferentes.
- Observado: los tres regimenes configurados estan ocupados (3 de 3) y ambas clases tienen
  lecturas en los tres (regimenes por clase: {0: 3, 1: 3}). Lecturas por regimen y clase:
  clase 0 con 4174 en congelado, 7598 en templado y 12705 en calido; clase 1 con 274, 556 y
  470 respectivamente. Rangos por clase: clase 0 [-21.63, 29.44] C y clase 1
  [-19.62, 29.69] C, con solapamiento de 49.06 C. Medianas: 16.73 C para la clase 0 y
  5.17 C para la clase 1.
- Interpretacion: la diferencia entre medianas se ajusta a la mezcla de regimenes de
  producto, no a un efecto aislado de la temperatura; la temperatura por si sola no separa
  las clases.
- Limitacion: el grafico no mide capacidad predictiva. `producto_id` identifica el regimen
  pero no es un predictor minimo del alcance obligatorio.

### Grafico 3. Boxplot de humedad actual por clase del objetivo

- Filas usadas: 25690. Excluidas solo del eje por humedad nula: 87; nunca se imputan.
- Pregunta: la humedad cambia antes de una desviacion.
- Observado: clase 0 con p25 47.80, mediana 59.0 y p75 74.80 (amplitud intercuartil 27.0
  puntos); clase 1 con p25 59.85, mediana 72.4 y p75 79.2 (amplitud 19.35 puntos).
  Solapamiento entre el p75 de la clase 0 y el p25 de la clase 1: 14.95 puntos porcentuales.
- Interpretacion: la humedad de la clase 1 esta desplazada hacia valores mas altos, pero las
  cajas se solapan de forma amplia: la humedad por si sola no distingue las clases.
- Limitacion: los puntos atipicos mostrados se conservan; el grafico no propone recorte.

### Grafico 4. Barplot de desviacion termica actual frente al promedio del objetivo

- Filas usadas: 25777 ventanas evaluables, con intervalos de confianza bootstrap al 95 %
  (2000 resampleos, semilla 20260925) y numero de observaciones por barra.
- Pregunta: una desviacion presente anticipa otra durante la siguiente hora.
- Observado: sin desviacion actual, promedio del objetivo 0.015157 (IC 0.013605 a 0.016750,
  n = 24477); con desviacion actual, 0.418462 (IC 0.390769 a 0.444615, n = 1300). Razon 27.61.
  El notebook calcula la separacion de los intervalos y obtiene True: el limite inferior con
  desviacion (0.390769) supera el limite superior sin desviacion (0.016750).
- Interpretacion: la desviacion ya presente en el instante t se asocia con una mayor
  proporcion de desviaciones dentro de la siguiente hora. La etiqueta usa la ventana
  (t, t+60] estricta, de modo que la desviacion del instante t no se cuenta como evento
  futuro, pero su presencia indica un estado termico ya alterado.
- Limitacion: la barra es la media de un indicador 0/1; describe ventanas, no viajes, no
  mide riesgo individual y no permite afirmar que la desviacion actual produce la futura.

### Grafico 5. Scatterplot de temperatura actual frente a variacion de 30 minutos con `hue`

- Filas usadas: 24306. Excluidas solo del eje por variacion nula: 1471. Transparencia 0.35
  y tamanho de punto reducido para evitar saturacion.
- Pregunta: la combinacion entre nivel y tendencia permite distinguir riesgo.
- Observado: cuartiles de la variacion, clase 0 con p25 -1.16, mediana -0.03 y p75 1.11;
  clase 1 con p25 -0.76, mediana 0.22 y p75 1.39. Solapamiento intercuartil: 1.87 C.
  Puntos con variacion absoluta mayor a 5.0 C: 825. La nube es continua y las clases se
  superponen sin frontera limpia.
- Interpretacion: la clase 1 se concentra en variaciones positivas y la clase 0 se centra
  cerca de cero, de modo que la pendiente reciente acompana la asociacion, pero el
  solapamiento es amplio.
- Limitacion: es una lectura descriptiva, no una frontera de decision; ademas temperatura
  actual y temperatura anterior tienen correlacion 0.9886, por lo que el nivel y la
  tendencia no son informacion independiente.

### Grafico 6. Lineplot temporal (opcional)

- Filas usadas: los viajes VIA-00087, VIA-00593 y VIA-00792, con 24 lecturas cada uno en
  Gold, 10, 10 y 9 ventanas positivas respectivamente. Criterio reproducible: mas ventanas
  positivas, luego mas lecturas, luego identificador de viaje mas pequeno. Los 338 viajes
  con al menos 15 lecturas evaluables y alguna ventana positiva eran candidatos.
- Pregunta: como se comportan la temperatura y el objetivo dentro de un mismo viaje.
- Observado: VIA-00087 con temperatura entre 1.33 y 11.26 C (mediana 4.62) y 7 lecturas
  con desviacion actual; VIA-00593 entre 1.40 y 10.41 C (mediana 4.47) y 7 desviaciones
  actuales; VIA-00792 entre 1.92 y 10.53 C (mediana 4.69) y 7 desviaciones actuales. Los
  marcadores de objetivo positivo aparecen antes, despues o al mismo tiempo que las
  desviaciones ya presentes.
- Interpretacion: en estos viajes las ventanas positivas se concentran en tramos de
  temperatura baja, coherente con lo observado en los graficos 2, 4 y 5.
- Limitaciones: son precisamente los viajes con casos positivos, no una muestra aleatoria,
  por lo que el grafico es ilustrativo y no generalizable; la cadencia no es regular
  (intervalos de 30, 60 y 90 minutos) y puede faltar alguna lectura intermedia. El objetivo
  representa un evento posterior dentro de (t, t+60], no una desviacion en el instante marcado.
- La columna auxiliar `tiene_ventana_positiva`, usada solo para marcar la serie, se deriva del
  objetivo y no es admisible como variable de entrada del modelo.

## Principales patrones observados

1. La clase positiva es minoritaria (5.04 % de las ventanas evaluables) y se concentra en
   338 de 1200 viajes; el desbalance es de 18.83 a 1.
2. La desviacion termica actual es el predictor con mayor contraste descriptivo: el promedio
   del objetivo pasa de 0.0152 a 0.4185, con intervalos de confianza que no se solapan.
3. La temperatura actual y la temperatura anterior estan casi perfectamente correlacionadas
   (0.9886), de modo que el nivel termico aporta informacion redundante entre ambos.
4. La humedad de la clase 1 es mayor en mediana (72.4 frente a 59.0) pero con solapamiento
   intercuartil de 14.95 puntos: la distribucion se desplaza, no se separa.
5. La variacion de temperatura de 30 minutos muestra medianas de 0.22 C en la clase 1 y
   -0.03 C en la clase 0, con fuerte solapamiento; la tendencia acompaña, no discrimina.
6. La prevalencia de la clase positiva varia segun el regimen de producto (6.16 %, 6.82 %
   y 3.57 %): la mezcla de productos se asocia con una linea base distinta del objetivo, sin
   que ello implique una relacion causal.
7. No hay valores centinela, no hay centinelas fuera de rango, no hay humedades fuera de
   0 a 100 % y no hay faltantes sin causa declarada.

Ninguno de estos patrones es una relacion causal y ninguno permite afirmar que una variable
sea importante para el modelo por si sola.

## Limitaciones

- El EDA describe ventanas de lectura, no viajes completos ni decisiones operativas.
- La cadencia observada es de 30 minutos con intervalos reales de 60 y 90 minutos: la
  variacion de 30 minutos se resuelve con una sola lectura base, no con un promedio, y 315
  lecturas quedan con variacion nula.
- La cobertura futura admite una ventana observada de al menos 45 de los 60 minutos; las
  2671 lecturas sin cobertura no son comparables con las evaluables y por eso se excluyen
  de todo analisis del objetivo.
- La poblacion es multimodal en temperatura por regimen de producto, lo que dificulta una
  lectura aislada del efecto de la temperatura.
- El grafico temporal usa 3 viajes seleccionados por tener el caso: es sesgado a proposito
  y no generalizable.
- Los predictores estan correlacionados entre si, por lo que la lectura conjunta de los
  graficos 2 y 5 no puede aislar el aporte de cada variable.
- No se evaluo ninguna metrica de modelo: el rendimiento se mide en la etapa de regresion
  logistica, no aqui.

## Implicaciones para la regresion logistica

- La unidad de analisis es la lectura, pero la separacion entre entrenamiento y prueba debe
  hacerse por viaje, porque 862 viajes no aportan ninguna ventana positiva y 12 viajes
  aportan una sola; una division por filas permitiria que lecturas consecutivas del mismo
  viaje aparecieran en ambos conjuntos.
- El desbalance de 18.83 a 1 con solo 1300 ventanas positivas limita el numero de viajes
  positivos disponibles para validar (338). Conviene reportar metricas sensibles a la
  clase minoritaria ademas de la exactitud, y declarar el criterio de umbrales.
- `temperatura_cabina_c` y `temperatura_anterior` tienen correlacion 0.9886: incluirlas
  ambas es explicito en el alcance minimo, pero el modelo debe soportar colinealidad y su
  interpretacion debe evitar repartir el merito entre ambas.
- La humedad tiene 98 faltantes y la variacion de 30 minutos 1515 en Gold. El EDA no las
  imputa; la etapa de modelado debe definir una regla reproducible, ajustada solo con
  entrenamiento, y declarar como se tratan.
- La exclusion de las 2671 ventanas no evaluables debe replicarse en el modelado; incluirlas
  con objetivo nulo obligaria a inventar una clase y sesgaria la prevalencia.
- El grafico 4 sugiere que `desviacion_termica_flag` es el predictor con mayor señal
  descriptiva, pero esa lectura no anticipa coeficientes, calibracion ni rendimiento.

## Controles contra fuga temporal verificados en esta ejecucion

- `ts_temperatura_anterior > timestamp`: 0 casos.
- `ts_base_variacion > timestamp`: 0 casos.
- Temperatura anterior presente sin marca de tiempo: 0 casos.
- Variacion presente sin marca de tiempo: 0 casos.
- Los cinco predictores minimos son disjuntos de las nueve columnas no admisibles
  (objetivo, control de cobertura, control de ventana y auditoria): True.
- El objetivo no se recalcula en este notebook: solo se lee y se cuenta.

## Controles finales ejecutados

18 controles, todos en OK:

1. Gold no modificado (SHA-256 identico al inicio y al cierre).
2. Forma Gold 28448 x 20.
3. Clave de lectura unica.
4. Sin duplicados exactos.
5. Faltantes no clasificados en cero.
6. Objetivo nulo solo en ventanas no evaluables.
7. Poblacion analitica usa solo ventanas evaluables (25777 filas).
8. Objetivo contiene solo 0 y 1.
9. Gold conservado: analitica + excluidas = total.
10. Todo nulo de temperatura anterior tiene motivo.
11. Todo nulo de variacion de 30 min tiene motivo.
12. Los motivos de la variacion cubren todos sus nulos.
13. Sin antecedentes posteriores al instante de prediccion.
14. Predictores minimos disjuntos de columnas no admisibles.
15. Sin centinelas en temperatura ni variacion.
16. Humedad dentro de 0 a 100.
17. Timestamps parseados sin errores.
18. No se generaron variables de modelo ni se entreno ningun modelo.

Adicionalmente: el notebook se ejecuto de principio a fin (28 celdas de codigo, 0 errores de
ejecucion, 0 salidas de error), quedan 6 imagenes embebidas (5 graficos obligatorios y el
grafico temporal opcional), no se imputo ningun dato, no se elimino ninguna fila y el
notebook puede volver a ejecutarse desde el inicio.

## Reproducibilidad

- Ejecucion UTC: 2026-09-25T19:28:38.739847+00:00.
- Python 3.14.6, pandas 3.0.5, numpy 2.5.3, seaborn 0.13.2, matplotlib 3.11.2.
- Semilla declarada en `config`: 20260925, usada en el bootstrap del grafico 4
  (2000 resampleos, nivel 95 %) y en el criterio de seleccion reproducible de viajes del
  grafico 6.
- El control de conciliacion con `informes/silver_gold/Informe_S2G_01_IoT_Gold.md` verifica
  primero que el archivo exista; si no estuviera disponible, el notebook lo declara y continua
  con la verificacion directa sobre el CSV, en lugar de interrumpirse.
- Toda la configuracion (rutas, nombres reales de columnas, clave de lectura, objetivo,
  bandera de ventana evaluable, predictores minimos, columnas no admisibles, cortes de
  regimen, parametros visuales y semilla) esta centralizada en el diccionario `CONFIG` de
  la primera celda de codigo; ninguna ruta ni constante se distribute por el resto del
  notebook.
- Dependencias de ejecucion: pandas, numpy, matplotlib y seaborn. En un entorno limpio se
  instalan con `pip install matplotlib seaborn`. No existe `requirements.txt` en el
  repositorio, por lo que el requisito queda declarado aqui y en la celda de reproducibilidad
  del notebook.
- El notebook no escribe archivos de datos: no invoca `to_csv` ni `to_parquet`; la unica
  mencion de esos metodos es un texto informativo de la celda de reproducibilidad.
- Deteccion de raiz: variable de entorno `ANDINALOG_ROOT` o ancestros del directorio actual.
  Ejecutar las celdas en orden desde la raiz del proyecto.

## Correcciones aplicadas tras la auditoria

La auditoria del EDA (0 criticos, 0 importantes, 7 menores) obligo a estas correcciones. Son
de trazabilidad y claridad: no cambian ninguna cifra aprobada, ni la poblacion analitica, ni
los criterios de los graficos, ni las conclusiones.

| Hallazgo | Correccion | Evidencia de cierre |
|---|---|---|
| MENOR-1: etiqueta ambigua de viajes | Se distinguen "viajes sin ninguna ventana positiva: 862" (verificado sumando positivos por viaje) de "viajes con al menos una ventana negativa: 1200" | Celda de desbalance, lineas 5 a 7 de esa salida |
| MENOR-2: dependencias no documentadas | Se declara el requisito `pip install matplotlib seaborn` en el notebook y en este informe | Celda de reproducibilidad, lineas de dependencias |
| MENOR-3: interpretaciones como texto fijo | El grafico 2 imprime regimenes ocupados, lecturas por regimen y clase, y solapamiento de rangos calculados; el grafico 4 imprime los dos IC y el booleano de separacion calculado | Lectura de los graficos 2 y 4 |
| MENOR-4: verbo con connotacion causal | "modula" sustituido por "se asocia con una linea base distinta", sin relacion causal | Patron 6 de este informe |
| MENOR-5: acoplamiento duro al informe Gold | La lectura del informe Gold se condiciona a su existencia y, si falta, se declara la omision del control | Celda de control de granularidad |
| MENOR-6: conteo de 1554 filas mal etiquetado | Se reporta como "filas con al menos un predictor continuo faltante (informe, no exclusiones)" y se desglosa el faltante por predictor (0, 87, 0, 1191, 1471) | Celda de estadisticas por clase |
| MENOR-7: marcador derivado del objetivo | Se declara que `tiene_ventana_positiva` solo marca la serie y no es admisible como entrada del modelo | Celda del grafico 6 y seccion del grafico 6 de este informe |

Gold no fue modificado: el SHA-256 sigue siendo
`f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479`, igual que antes de las
correcciones. El notebook fue reejecutado por completo: 28 celdas de codigo, 0 errores, 0
salidas de error, 6 imagenes embebidas y 18 controles finales en OK.

Este EDA no produce ni exporta archivos CSV: su unico producto es el notebook ejecutado y
este informe, por diseno del alcance de la skill de EDA. El Gold de entrada permanece sin
cambios.

## Rutas de los entregables

- Notebook: `notebooks/eda/EDA_01_AndinaLog_IoT_Gold.ipynb`
- Informe: `informes/eda/Informe_EDA_01_AndinaLog_IoT_Gold.md`
- Entrada analizada: `datos/gold/andinalog_iot_modelado_gold.csv`
