# Proyecto AndinaLog 03B

- Objetivo: anticipar desviaciones térmicas durante los siguientes 60 minutos.
- Unidad de análisis: una lectura de telemetría de un viaje en un instante.
- Flujo: Bronze → Silver y cuarentena → Gold → EDA → regresión logística.
- Grupo de separación del modelo: `viaje_id`.
- Objetivo: `desviacion_proximos_60min_flag`.
- Predictoras mínimas: temperatura, humedad, desviación actual, temperatura anterior y variación de 30 minutos.
- La clase positiva representa cerca del 5% de las ventanas evaluables.
- El modelo reconoce mejor desviaciones ya presentes que eventos nuevos.
- La temperatura y el desempeño deben revisarse por producto.
- No existen rangos térmicos oficiales por producto en los archivos disponibles.
- Todo resultado debe explicarse para personas sin formación analítica.
- Última actualización: 2026-09-30.
