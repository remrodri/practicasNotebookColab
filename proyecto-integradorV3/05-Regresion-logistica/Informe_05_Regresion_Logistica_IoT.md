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

## Resultado según la desviación actual

### Sin desviación actual

- Lecturas: 4,976
- Desviaciones futuras reales: 158
- Verdaderos positivos: 10
- Falsos negativos: 148
- Falsos positivos: 253
- Recall: 6.33%
- Precisión: 3.80%

### Con desviación actual

- Lecturas: 198
- Desviaciones futuras reales: 120
- Verdaderos positivos: 120
- Falsos negativos: 0
- Falsos positivos: 78
- Recall: 100.00%
- Precisión: 60.61%

## Interpretación

El modelo depende fuertemente de la desviación actual. Cuando la lectura todavía es normal, detecta solamente 10 de 158 desviaciones futuras. Cuando la desviación ya está presente, genera una alerta para todos los casos del grupo: detecta las 120 continuaciones, pero también produce 78 falsas alertas.

Por tanto, el desempeño global describe principalmente la continuidad de desviaciones existentes y no representa adecuadamente la capacidad de anticipar eventos nuevos.

## Comparación diagnóstica

El modelo sin `desviacion_termica_flag` aumenta el recall, pero reduce fuertemente la precisión y el PR AUC. Esta comparación no reemplaza el modelo oficial y no se utilizó para ajustar el umbral con la prueba.

## Línea base

La referencia siempre predice la clase 0. Su recall y F1 son 0 porque no identifica ninguna desviación futura.

## Limitaciones

- La clase positiva es poco frecuente.
- El modelo separa débilmente las nuevas desviaciones cuando el estado actual es normal.
- La evaluación corresponde a una sola división por viaje con semilla fija.
- No se optimizó el umbral con la prueba.
- Los coeficientes muestran asociaciones y no efectos causales.

## Reproducibilidad

- Python: 3.12.14
- pandas: 3.0.1
- NumPy: 2.3.5
- scikit-learn: 1.9.1
- Ejecución UTC: 2026-09-29T19:51:10.601493+00:00
