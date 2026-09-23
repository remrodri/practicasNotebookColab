# Informe S9 — MLP inicial AndinaLog 03B

## Objetivo

Construir una primera red neuronal para clasificar si ocurrirá una desviación térmica durante los próximos 60 minutos y compararla con el baseline y el mejor modelo clásico de S7.

S9 funciona como experimento inicial. La regularización, EarlyStopping, selección de umbral y apertura final de test corresponden a S10.

## Datos y control de fuga

- Lecturas aptas: 28.557.
- Ajuste: 18.946 lecturas y 796 viajes.
- Validación: 4.287 lecturas y 180 viajes.
- Test sellado: 4.274 lecturas y 180 viajes.
- Prevalencia en ajuste: 4,62 %.
- Prevalencia en validación: 3,52 %.

Se reutilizó exactamente la asignación temporal de S6. Imputación, escalamiento y codificación categórica se ajustaron únicamente con AJUSTE.

Se excluyeron el objetivo, el desvío futuro continuo, el número de lecturas futuras, las banderas de aptitud y cualquier dato posterior al instante de predicción.

## Arquitectura inicial

| Capa | Configuración |
|---|---|
| Entrada | 31 variables después del preprocesamiento |
| Oculta 1 | 32 neuronas, ReLU |
| Oculta 2 | 16 neuronas, ReLU |
| Salida | 1 neurona, sigmoide |
| Parámetros entrenables | 1.569 |
| Optimizador | Adam, tasa 0,001 |
| Pérdida | Binary crossentropy |
| Entrenamiento | 20 épocas, batch 32 |

La red no utiliza L2, Dropout, EarlyStopping ni ponderación de clases. Es una referencia inicial coherente con S9.

## Resultado en validación

| Modelo | Accuracy | Precision | Recall | F1 | PR-AUC | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Dummy mayoritaria | 96,48 % | 0,00 % | 0,00 % | 0,000 | 0,035 | 0,500 |
| MLP inicial | 97,22 % | **84,78 %** | 25,83 % | 0,396 | 0,360 | 0,748 |
| Random Forest S7 | 95,19 % | 33,33 % | **36,42 %** | 0,348 | **0,398** | **0,764** |

Con umbral 0,50, la MLP produjo:

- 4.129 verdaderos negativos;
- 7 falsos positivos;
- 112 falsos negativos;
- 39 verdaderos positivos.

La MLP genera pocas falsas alertas y alta precisión, pero omite la mayoría de las desviaciones. Random Forest conserva mejor PR-AUC y recall.

## Curvas de aprendizaje

La menor pérdida de validación aparece en la **época 7**. Después de ese punto, la pérdida de ajuste continúa bajando mientras la validación deja de mejorar y comienza a aumentar lentamente. Esto muestra el inicio de sobreajuste y justifica incorporar EarlyStopping en S10.

El recall de ajuste se estabiliza cerca de 38 %, mientras el de validación queda alrededor de 26–28 %. La diferencia indica que la arquitectura inicial no generaliza suficientemente la clase minoritaria.

## Decisión

La MLP inicial supera al Dummy, pero no supera a Random Forest en la métrica principal PR-AUC. No se abre TEST y no se recomienda todavía una red neuronal final.

S10 deberá comparar, usando únicamente validación:

1. arquitectura inicial como referencia;
2. regularización L2;
3. Dropout;
4. EarlyStopping con restauración de mejores pesos;
5. ponderación de clases y selección de umbral según costo operativo.

Después de fijar configuración y umbral, TEST podrá abrirse una sola vez para la evaluación final de la MLP.

