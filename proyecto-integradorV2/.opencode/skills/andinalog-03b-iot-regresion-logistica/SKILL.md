---
name: andinalog-03b-iot-regresion-logistica
description: Genera o revisa el notebook ejecutado y el informe del modelo de regresion logistica de AndinaLog 03B para predecir desviacion termica en los proximos 60 minutos desde la tabla Gold IoT. Usar despues del Gold y EDA aprobados.
---

# AndinaLog 03B Regresion Logistica

Entrena y evalua el modelo requerido usando Gold como entrada. Lee [references/contrato.md](references/contrato.md) antes de dividir los datos.

## Entregables

1. Notebook de modelado `.ipynb` ejecutado con resultados visibles.
2. Informe `.md` con metodologia, resultados, interpretacion y limitaciones.

## Flujo

1. Valida esquema y selecciona solo ventanas objetivo evaluables.
2. Usa los predictores minimos y declara cualquier predictor adicional.
3. Separa entrenamiento y prueba por viaje u orden con semilla fija; demuestra que no comparten grupos.
4. Ajusta transformaciones e imputaciones exclusivamente con entrenamiento mediante un `Pipeline`.
5. Entrena regresion logistica y documenta hiperparametros, desbalance y umbral.
6. Compara contra una linea base simple apropiada al desbalance.
7. Evalua sobre prueba una sola vez para el resultado final.
8. Presenta matriz de confusion, precision, recall, F1, ROC AUC y PR AUC cuando sean definibles.
9. Interpreta coeficientes considerando escalado y sin afirmar causalidad.
10. Registra versiones, semilla, filas, grupos, clases y limitaciones.

## Reglas estrictas

- Ningun viaje u orden puede aparecer en entrenamiento y prueba.
- No uses identificadores, timestamp bruto, objetivo, ventana evaluable ni columnas futuras como predictores.
- No ajustes escalado, imputacion, seleccion ni umbral con prueba.
- Si prueba carece de una clase, el split no permite evaluar el modelo.
- No reportes accuracy como unica metrica.
