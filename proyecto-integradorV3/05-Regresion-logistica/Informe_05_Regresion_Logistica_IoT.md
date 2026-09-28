# Informe 05 — Regresión logística IoT

## Metodología

- Filas modeladas: 25,797
- Entrenamiento: 20,623 filas y 960 viajes
- Prueba: 5,174 filas y 240 viajes
- Viajes compartidos: 0
- Semilla: 42
- Umbral: 0.50
- Clase positiva en prueba: 5.37%
- Modelo: regresión logística con `class_weight="balanced"`
- Preparación: imputación por mediana y escalado ajustados solo con entrenamiento

## Resultados finales en prueba

- Precisión: 0.2820
- Recall: 0.4676
- F1: 0.3518
- ROC AUC: 0.7489
- PR AUC: 0.3732
- Verdaderos negativos: 4,565
- Falsos positivos: 331
- Falsos negativos: 148
- Verdaderos positivos: 130

## Línea base

La referencia siempre predice la clase 0. Su recall y F1 son 0 porque no identifica ninguna desviación futura.

## Interpretación

El modelo aporta capacidad para ordenar el riesgo y detectar parte de las desviaciones, pero todavía produce falsos negativos y falsos positivos. Cualquier cambio del umbral debe basarse en el costo operativo de ambos errores y evaluarse con validación separada, no con esta prueba final.

## Limitaciones

- La clase positiva es poco frecuente.
- Los coeficientes son asociaciones, no efectos causales.
- El resultado corresponde a una sola división por viaje con semilla fija.
- No se optimizó el umbral con la prueba.

## Reproducibilidad

- Python: 3.12.14
- pandas: 3.0.1
- NumPy: 2.3.5
- scikit-learn: 1.9.1
- Ejecución UTC: 2026-09-28T17:46:46.702510+00:00
