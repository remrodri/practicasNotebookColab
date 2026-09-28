# Informe 04 — EDA de la tabla Gold IoT

## Población analizada

- Filas Gold: 28,465
- Columnas: 17
- Viajes: 1,200
- Ventanas evaluables: 25,797
- Ventanas no evaluables: 2,668
- Duplicados por viaje + timestamp: 0

## Respuestas a las preguntas

1. **¿Qué tan poco frecuentes son las desviaciones futuras?**  
   Aparecen en 1,296 lecturas, equivalentes al 5.02% de las ventanas evaluables.

2. **¿Las futuras desviaciones parten de temperaturas diferentes?**  
   La mediana es 16.73 °C sin desviación futura y 5.24 °C con desviación futura.

3. **¿La humedad cambia antes de una desviación?**  
   La mediana es 59.00% sin desviación futura y 72.40% con desviación futura.

4. **¿Una desviación presente anticipa otra en la siguiente hora?**  
   La frecuencia futura es 3.03% sin desviación actual y 59.41% con desviación actual.

5. **¿La combinación de nivel y tendencia permite reconocer el riesgo?**  
   El grupo con riesgo difiere -11.46 °C en nivel y +0.25 °C en variación de 30 minutos respecto del grupo sin riesgo. El gráfico sigue mostrando superposición entre clases.

## Limitaciones

- El análisis es descriptivo y no demuestra causalidad.
- Las ventanas no evaluables se conservan en Gold, pero no participan en los gráficos del objetivo.
- El gráfico temporal muestra únicamente tres viajes seleccionados por contener casos positivos.

Ejecución UTC: 2026-09-28T17:43:27.645182+00:00
