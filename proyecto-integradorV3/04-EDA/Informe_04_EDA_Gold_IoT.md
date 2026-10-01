# Informe 04 — Análisis exploratorio de la tabla Gold IoT

## 1. Propósito

Este informe explica qué contiene la tabla Gold y qué patrones aparecen antes de una desviación térmica. El objetivo vale 0 cuando no ocurre una desviación durante los siguientes 60 minutos y 1 cuando sí ocurre. El análisis es descriptivo: no demuestra causalidad ni realiza todavía una predicción.

## 2. Población y calidad estructural

- Filas Gold: 28,465
- Columnas: 17
- Viajes: 1,200
- Ventanas evaluables: 25,797
- Ventanas no evaluables: 2,668
- Duplicados por viaje + timestamp: 0

Cada fila representa una lectura de telemetría de un viaje en un momento determinado. La ausencia de claves repetidas indica que los cruces no multiplicaron lecturas.

## 3. Valores vacíos

- Temperatura anterior: 1,200 vacíos (4.22%). Aparecen principalmente al inicio de cada viaje, cuando todavía no existe una lectura anterior.
- Variación de temperatura en 30 minutos: 1,504 vacíos (5.28%). No existe una lectura anterior suficientemente cercana para calcularla.
- Objetivo futuro: 2,668 vacíos (9.37%). El viaje termina antes de completar los 60 minutos futuros.

Estos vacíos tienen una explicación temporal y no representan necesariamente fallas de los sensores. No se encontraron faltantes inesperados. Las ventanas sin futuro completo se conservan en Gold, pero no se usan en los gráficos del objetivo.

## 4. Respuestas a las preguntas

### 4.1 ¿Qué tan poco frecuentes son las desviaciones futuras?

Se observan 1,296 casos positivos de 25,797 ventanas evaluables, equivalentes al 5.02%. En palabras sencillas, cerca de 5 de cada 100 lecturas anuncian una desviación futura. Por eso el modelo posterior deberá prestar atención a una clase poco frecuente.

### 4.2 ¿Las futuras desviaciones parten de temperaturas diferentes?

La mediana es 16.73 °C sin desviación futura y 5.24 °C con desviación futura. La diferencia es 11.49 °C. Las desviaciones futuras parten, en general, de temperaturas más bajas, aunque existe superposición y una temperatura aislada no determina el resultado.

### 4.3 ¿La humedad cambia antes de una desviación?

La mediana es 59.00% sin desviación futura y 72.40% con desviación futura. La diferencia es 13.40 puntos porcentuales. Los casos futuros se asocian con mayor humedad, pero la humedad no debe utilizarse sola como regla automática.

### 4.4 ¿Una desviación presente anticipa otra en la siguiente hora?

La frecuencia futura es 3.03% sin desviación actual y 59.41% con desviación actual. La diferencia es 56.38 puntos porcentuales. La desviación actual es la señal más clara, aunque no es una regla perfecta y no identifica por sí misma todos los eventos nuevos.

### 4.5 ¿La combinación de nivel y tendencia permite reconocer el riesgo?

El grupo con riesgo difiere -11.46 °C en nivel y +0.25 °C en variación de 30 minutos respecto al grupo sin riesgo. La diferencia principal está en el nivel de temperatura. La superposición de colores indica que ambas variables aportan contexto, pero no separan todos los casos.


## 5. Análisis por producto

La comparación por producto muestra tres niveles térmicos observados: medianas cercanas a -18 °C, 4 °C y 20 °C. Esto confirma que la temperatura no debe interpretarse de la misma manera para todos los productos.

- Mediana menor a 0 °C: 10 productos, temperatura mediana -17.96 °C y desviación futura 7.44%
- Mediana entre 0 y 10 °C: 20 productos, temperatura mediana 4.04 °C y desviación futura 7.85%
- Mediana mayor o igual a 10 °C: 30 productos, temperatura mediana 20.03 °C y desviación futura 2.39%

Los mayores porcentajes observados de desviación futura corresponden a:

- PROD-047: temperatura mediana 4.08 °C; desviación futura 12.41%
- PROD-056: temperatura mediana 4.04 °C; desviación futura 11.23%
- PROD-008: temperatura mediana -17.89 °C; desviación futura 10.98%
- PROD-034: temperatura mediana 4.02 °C; desviación futura 10.90%
- PROD-051: temperatura mediana -17.94 °C; desviación futura 10.62%

Estos porcentajes describen asociaciones históricas y no prueban que el producto sea la causa. Los grupos térmicos son resúmenes de los datos observados, no rangos permitidos. Para evaluar cumplimiento se necesita una tabla oficial con los límites por producto.

## 6. Gráfico temporal opcional

Los tres viajes seleccionados permiten observar la secuencia de la temperatura y los momentos desde los que aparece riesgo durante la hora siguiente. Son ejemplos con casos positivos y no representan necesariamente a todos los viajes.

## 7. Conclusiones

- La estructura Gold es consistente y no presenta multiplicación de lecturas.
- Los vacíos observados tienen explicaciones temporales.
- Las desviaciones futuras son poco frecuentes.
- Temperatura, humedad, desviación actual y tendencia contienen señales descriptivas.
- La desviación actual es la señal más marcada, lo que anticipa que reconocer problemas nuevos será más difícil que reconocer la continuidad de uno existente.

## 8. Limitaciones

- El análisis es descriptivo y no demuestra causalidad.
- Los patrones históricos pueden cambiar en viajes nuevos.
- Las ventanas no evaluables no participan en los gráficos del objetivo.
- El gráfico temporal muestra solamente tres viajes con casos positivos.
- Ninguna diferencia observada garantiza por sí sola una buena predicción.
- No se proporcionaron rangos térmicos permitidos por producto; los grupos mostrados son descriptivos.

Ejecución UTC: 2026-09-30T00:43:01.417511+00:00
