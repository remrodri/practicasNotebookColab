# Informe S10 — MLP regularizada y test final AndinaLog 03B

## Objetivo

Regularizar la MLP inicial de S9, seleccionar modelo y umbral exclusivamente con validación y abrir test una sola vez para obtener la evaluación final.

El costo didáctico utilizado, siguiendo el laboratorio de S10, fue:

- falso negativo: 10 unidades;
- falso positivo: 1 unidad.

Este costo sirve para el experimento y todavía requiere confirmación operativa de AndinaLog.

## Diseño experimental

Se mantuvieron el mismo objetivo, las mismas variables base y el split temporal congelado:

| Partición | Lecturas | Viajes |
|---|---:|---:|
| Ajuste | 18.946 | 796 |
| Validación | 4.287 | 180 |
| Test | 4.274 | 180 |

El preprocesamiento fue ajustado únicamente con AJUSTE. Test no participó en la elección de arquitectura, regularización ni umbral.

## Modelos comparados

### MLP inicial

- Capas 32 → 16 → 1.
- Sin L2 ni Dropout.
- 60 épocas.
- Mejor `val_loss`: época 7.
- Después de esa época, la pérdida de entrenamiento continuó bajando mientras validación empeoró, mostrando sobreajuste.

### MLP regularizada

- Capas 32 → Dropout 0,20 → 16 → 1.
- Regularización L2 de 0,001.
- EarlyStopping con paciencia 8 y restauración de mejores pesos.
- Ejecutó 27 épocas.
- Mejor `val_loss`: época 23.

La regularización redujo la separación entre las curvas y detuvo el entrenamiento antes de las 100 épocas máximas.

## Selección en validación

| Modelo | Umbral | Precision | Recall | F1 | PR-AUC | ROC-AUC | FP | FN | Costo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy | 0,50 | 0 % | 0 % | 0,000 | 0,035 | 0,500 | 0 | 151 | 1.510 |
| MLP inicial | 0,35 | 72,31 % | 31,13 % | 0,435 | 0,354 | 0,745 | 18 | 104 | 1.058 |
| **MLP regularizada** | **0,10** | **67,11 %** | **33,77 %** | **0,449** | **0,370** | **0,766** | **25** | **100** | **1.025** |

Antes de abrir test quedaron congelados:

- modelo: **MLP regularizada**;
- umbral: **0,10**.

## Evaluación única en test

| Modelo | Precision | Recall | F1 | PR-AUC | ROC-AUC | FP | FN | TP | Costo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy | 0 % | 0 % | 0,000 | 0,054 | 0,500 | 0 | 232 | 0 | 2.320 |
| **MLP regularizada** | 71,33 % | **46,12 %** | 0,560 | 0,501 | **0,850** | 43 | **125** | **107** | **1.293** |
| Random Forest S7 | **78,36 %** | 45,26 % | **0,574** | **0,526** | 0,844 | **29** | 127 | 105 | 1.299 |

La MLP detectó dos desviaciones adicionales frente a Random Forest, pero generó 14 falsas alertas adicionales. Su costo didáctico fue solo 6 unidades menor. Random Forest mantiene mejor precision, F1 y PR-AUC.

## Interpretación

La regularización mejoró la estabilidad y permitió seleccionar una configuración mejor que la MLP inicial bajo el costo definido. No obstante, la ventaja final frente a Random Forest es mínima:

- MLP: costo 1.293;
- Random Forest: costo 1.299.

Esta diferencia de 0,46 % en el costo no justifica por sí sola la complejidad adicional de una red neuronal. Además, la MLP todavía omite 125 de las 232 desviaciones reales del test.

## Recomendación

Se recomienda **continuar la investigación** y conservar Random Forest como referencia principal por su simplicidad y desempeño comparable. La MLP regularizada queda como candidata experimental, pero no como reemplazo aprobado.

Antes de un piloto se necesita:

1. confirmar con AndinaLog el costo real de FP y FN;
2. definir capacidad máxima de alertas;
3. mejorar datos y variables capaces de distinguir excursiones;
4. validar en otro periodo y con datos reales;
5. comprobar estabilidad por producto, camión, centro y ruta.

## Limitaciones

- Datos sintéticos y periodo único.
- Costos de error didácticos.
- Baja prevalencia y cambio de prevalencia entre validación y test.
- No se demuestra impacto económico ni causalidad.
- La apertura final de test describe este corte histórico; no autoriza despliegue.

