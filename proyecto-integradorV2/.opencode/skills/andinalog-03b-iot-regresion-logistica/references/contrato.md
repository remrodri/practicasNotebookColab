# Contrato del modelo IoT

Objetivo: `desviacion_proximos_60min_flag` en filas con `ventana_objetivo_evaluable = True`.

Predictores minimos: temperatura actual, humedad actual, desviacion termica actual, temperatura anterior y variacion de temperatura de 30 minutos. Adapta nombres a las columnas reales y documenta el mapeo.

Realiza split por viaje u orden, con cada grupo en una sola particion. Todo parametro aprendido se ajusta con entrenamiento. La etiqueta futura y cualquier dato posterior a `t` quedan fuera de `X`.

Evalua matriz de confusion, precision, recall, F1, ROC AUC, PR AUC, prevalencia y linea base. Explica el costo de falsos negativos y positivos antes de recomendar otro umbral.
