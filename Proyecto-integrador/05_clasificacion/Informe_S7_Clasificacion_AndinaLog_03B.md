# Informe S7 — Clasificación térmica AndinaLog 03B

## Pregunta predictiva

¿Habrá una desviación térmica durante los próximos 60 minutos?

- **Clase positiva:** `clasificacion_objetivo_60min = 1`.
- **Unidad:** una lectura IoT.
- **Acción posible:** revisar o intervenir el transporte antes de que la desviación afecte la cadena de frío.
- **Error crítico:** falso negativo, porque representa una desviación real no advertida.

## Datos y partición

Se utilizaron 28.557 lecturas aptas para clasificación. La prevalencia global positiva es 4,63 %, por lo que accuracy no se utiliza como criterio principal.

Se reutilizó exactamente `asignacion_split_viajes.csv` de S6:

| Partición | Viajes | Lecturas | Positivos | Prevalencia |
|---|---:|---:|---:|---:|
| Ajuste | 796 | 18.946 | 876 | 4,62 % |
| Validación | 180 | 4.287 | 151 | 3,52 % |
| Test | 180 | 4.274 | 232 | 5,43 % |

Los 44 viajes marcados `EXCLUIDO_MARGEN` no participan. No existe cruce de viajes entre particiones.

## Selección en validación

Se compararon regresiones logísticas con distintos valores de `C` y ponderación de clases, además de Random Forest. Cada alternativa fue evaluada con variables base y con variables históricas de eventos.

El modelo seleccionado por **PR-AUC de validación** fue **Random Forest base**:

| Métrica de validación a umbral 0,50 | Resultado |
|---|---:|
| PR-AUC | 0,397 |
| ROC-AUC | 0,762 |
| Recall | 35,76 % |
| Precision | 32,73 % |
| F1 | 0,342 |

Random Forest con eventos obtuvo PR-AUC 0,387. Los eventos no mejoraron esta clasificación en la validación actual.

## Selección del umbral

El umbral se eligió únicamente con validación. Se utilizó una relación didáctica de costo:

- falso negativo: 5 unidades;
- falso positivo: 1 unidad.

El menor costo relativo se obtuvo con **umbral 0,71**. En validación produjo 51 verdaderos positivos, 100 falsos negativos, 15 falsos positivos y 66 alertas.

Esta relación 5:1 no representa todavía una decisión oficial de AndinaLog. El negocio debe definir cuánto cuesta perder una desviación y cuántas alertas puede atender.

## Evaluación final en test

| Métrica | Random Forest | Dummy mayoritaria |
|---|---:|---:|
| Accuracy | 96,35 % | 94,57 % |
| Balanced accuracy | 72,27 % | 50,00 % |
| Precision | 78,36 % | 0,00 % |
| Recall | 45,26 % | 0,00 % |
| F1 | 0,574 | 0,000 |
| PR-AUC | 0,527 | 0,054 |
| ROC-AUC | 0,844 | 0,500 |

Matriz de confusión del modelo seleccionado:

|  | Predice normal | Predice desviación |
|---|---:|---:|
| Real normal | 4.013 | 29 |
| Real desviación | 127 | 105 |

El modelo genera 134 alertas, equivalentes al 3,14 % de las lecturas de test.

## Interpretación operativa

El modelo supera ampliamente al baseline y sus alertas tienen buena precisión. Sin embargo, detecta solo 105 de las 232 desviaciones: quedan **127 falsos negativos**.

Por ello, este umbral todavía no debe considerarse una alarma operativa aprobada. Antes de implementarlo se debe:

1. confirmar la relación de costo entre falso negativo y falso positivo;
2. definir cuántas alertas puede atender el equipo;
3. elegir el umbral con esos límites;
4. validar el desempeño en datos futuros y no sintéticos.

## Conclusión

Random Forest base fue la mejor alternativa en validación y alcanzó PR-AUC 0,527 y recall 45,26 % en test. Los eventos de flota no añadieron mejora en este experimento. El modelo tiene valor analítico, pero el número de desviaciones omitidas impide recomendar su uso directo como alarma sin recalibrar el umbral y mejorar las variables disponibles.

