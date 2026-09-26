# Informe del Plan de Correcciones - Grupo 06, AndinaLog 03B

Proyecto Integrador · Módulo 3 · Entregable 6 de 6 (solo si aplica) · alerta térmica en los próximos 60 minutos.

Este informe acompaña y explica el archivo `documentacion/Plan_de_Correcciones_Grupo06_AndinaLog_03B.xlsx`, generado desde la plantilla oficial `GIAD-M3_Plantilla_Plan_de_Correcciones.xlsx` sin sobrescribirla. El Excel conserva la estructura, las fórmulas, las validaciones, los colores, las celdas combinadas y las filas de ejemplo de la plantilla; este documento describe lo que cada sección pide, con la misma información y sin divergir de ella.

## 1. Identificación

| Campo del Excel | Valor |
|---|---|
| Equipo | Grupo 06 · AndinaLog · Subcaso 03B (alerta térmica en los próximos 60 minutos) |
| Fecha de la Preentrega (S12) | Pendiente |
| Fecha de esta actualización | 2026-09-25 |
| Integrantes | Completar nombres de integrantes antes de la entrega |
| Estado recibido en la Preentrega | Pendiente |

Nota visible en el Excel: Pendiente de completar después de recibir la Rúbrica de Preentrega S12. La Rúbrica S12 aún no fue recibida, por lo que el Estado recibido y la Fecha de la Preentrega quedan como Pendiente.

La Rúbrica de Preentrega S12 no ha sido recibida por el equipo. Se buscó en todo el repositorio del proyecto y en la carpeta de descargas del docente y no existe el archivo `GIAD_M3_S12_Rubrica_Preentrega_CALCULADORA.xlsx` ni ninguna copia de sus resultados. Por eso la Fecha de la Preentrega y el Estado recibido quedan como **Pendiente** en lugar de asumir un estado que no está documentado.

## 2. Por qué se preparó la plantilla

La hoja `Léame` de la plantilla establece que el archivo solo es obligatorio si el estado automático de la Rúbrica de Preentrega **no** dio `LISTA PARA DEFENSA`. Como el equipo no conoce todavía ese estado, se completó la identificación y se dejó constancia de las correcciones internas ya aplicadas, de modo que el archivo quede preparado para completarse con los hallazgos oficiales en cuanto la Rúbrica llegue. Si la Rúbrica termina dando `LISTA PARA DEFENSA`, este archivo no se entrega y no hay nada que corregir.

## 3. Hallazgos oficiales de la Preentrega

La Rúbrica S12 incluye en su Sección 5 tres filas fijas para el hallazgo crítico y hasta dos hallazgos importantes, anotados con el docente presente. La plantilla retoma exactamente esos hallazgos con la misma Prioridad y la misma Categoría.

**No se recibió ningún hallazgo oficial**, por lo que no hay filas que copiar desde la Sección 5 de la Rúbrica. Ninguna de las filas registradas se presenta como hallazgo recibido en la Preentrega, ninguna se clasificó como CRÍTICA o IMPORTANTE y ninguna prioridad o categoría fue inventada. Cuando la Rúbrica llegue, sus hallazgos se incorporarán a partir de la fila 23 del Excel, que es la primera fila amarilla libre, conservando la redacción, la Prioridad y la Categoría originales.

## 4. Correcciones internas registradas

Las 6 filas del Excel son correcciones internas del proyecto, todas con prioridad **MENOR**, que es un valor permitido por la validación de datos de la propia plantilla (`CRÍTICA,IMPORTANTE,MENOR`). Cada una dice explícitamente su origen para que no se confundan con hallazgos recibidos del docente. Se inventariaron porque la hoja `Léame` pide que la acción correctiva quede registrada de forma verificable, y porque el informe del modelo ya las documenta.

| N.° | Prioridad | Categoría | Origen | Estado |
|---|---|---|---|---|
| 1 | MENOR | Validez y reproducibilidad | interna | Resuelto |
| 2 | MENOR | Validez y reproducibilidad | interna | Resuelto |
| 3 | MENOR | Validez y reproducibilidad | interna | Resuelto |
| 4 | MENOR | Coherencia y completitud | interna | Resuelto |
| 5 | MENOR | Responsabilidad y autoría | interna | Resuelto |
| 6 | MENOR | Validez y reproducibilidad | decisión metodológica | Resuelto |

### 4.1 Categorías críticas y por qué se asignó cada una

Las cuatro categorías son las mismas de la Preentrega S12 y de la Defensa S13:

| Categoría | Definición oficial | Filas asignadas | Justificación |
|---|---|---|---|
| Validez y reproducibilidad | Fuga de información, evaluación solo en entrenamiento, o el notebook no ejecuta de principio a fin | 1, 2, 3 y 6 | Filas 1, 2, 3 y 6 tocan la validez de la evaluación: controles que deben comprobar en vez de afirmar, estadísticas que no deben incluir la prueba, una regla de imputación acotada y una comparación de modelos resuelta sin usar el conjunto de prueba. |
| Coherencia y completitud | El problema y las recomendaciones no guardan relación verificable, o falta evidencia indispensable | 4 | Faltaba el elemento de lectura de dos gráficos exigidos por el estándar de entrega. |
| Responsabilidad y autoría | Se afirma causalidad sin sustento, se ocultan resultados desfavorables o no se declara el uso de IA | 5 | Presentar probabilidades no calibradas como riesgo absoluto es una afirmación sin sustento, de la misma familia que afirmar causalidad. |
| Confidencialidad | Se exponen datos personales, credenciales o secretos operativos sin anonimizar o sin autorización | ninguna | No se encontró exposición de datos personales: el alcance de 03B usa un solo CSV de telemetría y el informe no muestra nombres, documentos, teléfonos ni correos. |

## 5. Detalle de las correcciones

### 5.1 Validez y reproducibilidad — MENOR

**Hallazgo registrado en el Excel:** Observación interna de la auditoría propia del proyecto (no proviene de la Rúbrica S12, que aún no se recibe): dos controles finales afirmaban una condición en lugar de comprobarla (un único ajuste del Pipeline y una única evaluación del conjunto de prueba).

**Acción correctiva aplicada:** Se sustituyeron ambos controles por controles que calculan su propia evidencia: se registró cada ajuste del modelo principal con la forma exacta de X usada y se envolvió la predicción sobre prueba en un contador por modelo. El control verifica que hubo un solo ajuste con X de entrenamiento y que hubo una sola pasada de predicción por modelo, en lugar de afirmar el resultado.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 19 (registro de ajustes) y celda 29 (contador de pasada sobre prueba); celda 40, tabla de controles: «Pipeline ajustado una sola vez y solo con X_tr (verificado, no afirmado) True» y «El conjunto de prueba se evaluo una sola vez por modelo (contador verificado) True»; salida de la celda 29: «Pasadas de prediccion sobre el conjunto de prueba: {'modelo_principal': 1, 'linea_base': 1}».

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

### 5.2 Validez y reproducibilidad — MENOR

**Hallazgo registrado en el Excel:** Observación interna de la auditoría propia del proyecto (no proviene de la Rúbrica S12, que aún no se recibe): las estadísticas descriptivas que justificaban la mediana se calculaban sobre toda la población de modelado, que incluye las filas reservadas de prueba.

**Acción correctiva aplicada:** Se movió la tabla descriptiva después del split y se limitó al conjunto de entrenamiento, indicando en la propia salida cuántas filas se usaron, de modo que ninguna cifra resumida incluya el conjunto de prueba. El imputador del Pipeline ya se ajustaba solo con entrenamiento.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 19, salida «Justificacion de la mediana con los datos reales, SOLO de entrenamiento (filas usadas: 20621)»; celda 40, control «Las estadisticas descriptivas se resumen solo con filas de entrenamiento» en OK.

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

### 5.3 Validez y reproducibilidad — MENOR

**Hallazgo registrado en el Excel:** Observación interna de la auditoría propia del proyecto (no proviene de la Rúbrica S12, que aún no se recibe): la función de codificación neutral de ausencia de historia no revalidaba que el nulo correspondiera a una causa estructural declarada, dependía de la celda previa.

**Acción correctiva aplicada:** La función ahora valida por sí misma los motivos declarados antes de codificar y detiene la ejecución con un error explícito si algún nulo carece de motivo estructural o tiene un motivo no estructural, de modo que la regla no pueda aplicarse a un faltante inesperado aunque se reutilice la función.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 13, función preparar_faltantes_estructurales (validación de motivos y raise ValueError); celda 12, salida «Regla aplicada solo a ausencias estructurales declaradas: OK».

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

### 5.4 Coherencia y completitud — MENOR

**Hallazgo registrado en el Excel:** Observación interna de la auditoría propia del proyecto (no proviene de la Rúbrica S12, que aún no se recibe): dos gráficos del modelo carecían de leyenda o de etiqueta del eje X.

**Acción correctiva aplicada:** Se agregó la leyenda explicativa de cada región en el mapa de calor de las matrices de confusión y se rotuló el eje horizontal del gráfico de comparación de métricas, de modo que los cinco gráficos tengan título, ambos ejes y leyenda.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 34 (leyenda del mapa de calor) y celda 37 (etiqueta del eje X del gráfico de barras); cinco imágenes embebidas.

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

### 5.5 Responsabilidad y autoría — MENOR

**Hallazgo registrado en el Excel:** Observación interna de la auditoría propia del proyecto (no proviene de la Rúbrica S12, que aún no se recibe): el informe no declaraba que las probabilidades del modelo balanceado no están calibradas, por lo que la salida podía leerse como riesgo absoluto.

**Acción correctiva aplicada:** Se declaró en el notebook y en el informe que class_weight='balanced' reescala la frontera de decisión y que la salida debe interpretarse como puntaje de priorización, no como probabilidad calibrada. El umbral se fija con validación sobre entrenamiento y no leyendo probabilidades.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 38, bloque «CALIBRACION»; Informe_MOD_01_AndinaLog_Regresion_Logistica.md · sección «Interpretacion de coeficientes» (apartado Calibracion) y «Recomendacion operativa prudente», pauta 4.

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

### 5.6 Validez y reproducibilidad — MENOR

**Hallazgo registrado en el Excel:** Decisión metodológica documentada (no es un hallazgo recibido): se mantiene class_weight='balanced' como modelo principal pese a que la variante sin ponderar obtiene mayor PR AUC, porque el falso negativo tiene mayor costo operativo en cadena de frío. El equilibrio definitivo precisión-recall queda pendiente de un costo de negocio o de la confirmación del docente.

**Acción correctiva aplicada:** Se documentó el bloque de criterios de selección en la configuración del notebook: criterio principal recall, restricción operativa sobre precisión y volumen de alertas, PR AUC como métrica global complementaria y no único criterio, alternativa operativa class_weight=None y pendiente de definición. Además se declaró de forma explícita que balanced no es superior en todas las métricas. La comparación se resolvió únicamente con validación cruzada por grupos dentro de entrenamiento, sin usar el conjunto de prueba, que se reservó para una sola evaluación final.

**Responsable:** Asignar integrante

**Evidencia de cierre:** MOD_01_AndinaLog_Regresion_Logistica.ipynb · celda 2 (config['sensibilidad']) y celda 25 (bloque de criterios y lectura contra cada criterio); celda 40, control «La comparacion de ponderacion no se hizo con el conjunto de prueba» en OK; Informe_MOD_01_AndinaLog_Regresion_Logistica.md · secciones «Criterio de seleccion del modelo» y «Desbalance y ponderacion de clases»; datos/modelado/metricas_mod_01_regresion_logistica.csv · bloque sensibilidad_B_ponderacion.

**Fecha de cierre:** 2026-09-25

**Estado:** Resuelto. La acción está aplicada y tiene evidencia, pero ningún otro integrante ha confirmado todavía la evidencia, por lo que la regla de la plantilla impide marcarla como `Verificado`.

## 6. Resumen automático de la Sección 2

Las celdas de la Sección 2 contienen fórmulas de la plantilla y **no fueron editadas**. Estos son los valores que el Excel calcula con las filas registradas:

| Total | Pendientes | En progreso | Resueltos | Verificados | CRÍTICA sin cerrar | Estado del plan |
|---|---|---|---|---|---|---|
| 6 | 0 | 0 | 6 | 0 | 0 | Completo - todos los hallazgos cerrados |

Lectura del resumen según la regla de la hoja `Léame`: mientras haya hallazgos CRÍTICA sin cerrar el proyecto no está en condiciones de defenderse. Hoy hay 0, y tampoco quedan IMPORTantes sin cerrar (0), de modo que el plan figura completo en cuanto a las filas registradas. Ese estado **no sustituye** la Rúbrica: describe únicamente lo que está escrito en el Excel.

Comprobaciones realizadas sobre el resumen:

- Las fórmulas `A10` a `G10` siguen siendo las de la plantilla y no se les escribió encima.
- Los rangos `B17:B28` e `I17:I28` empiezan en la fila 17, por lo que las filas de ejemplo de la fila 14 y 15 y la nota de la fila 16 quedan fuera del conteo, tal como exige la hoja `Léame`.
- No se encontraron errores de referencia ni de fórmula en el archivo generado.
- Quedan 6 filas amarillas libres (23 a 28) para los hallazgos oficiales de la Rúbrica, con el formato ya copiado hacia abajo.

## 7. Cumplimiento de las reglas de la plantilla

| Regla de la hoja `Léame` | Cumplimiento |
|---|---|
| Solo es obligatoria si la Rúbrica no dio `LISTA PARA DEFENSA` | El estado aún no se conoce; se completó la identificación y se dejó constancia de la regla. |
| Copiar cada hallazgo de la Sección 5 con su Prioridad y Categoría | No hay hallazgos recibidos; las filas internas se marcan como tales y ninguna se presenta como oficial. |
| Describir la acción correctiva de forma verificable | Cada fila dice qué cambió en el notebook o en el informe, con celda y salida concretas. |
| `Resuelto` cuando la acción está aplicada; `Verificado` cuando otro integrante confirma | Las seis filas están en `Resuelto`; ninguna en `Verificado`. |
| Revisar el resumen automático antes de la entrega | Sección 6 de este informe, con los valores calculados. |
| No editar, borrar ni contar las filas de ejemplo | Filas 14, 15 y 16 idénticas a la plantilla y fuera de los rangos de las fórmulas. |
| Agregar filas amarillas copiando el formato hacia abajo | Seis filas escritas con el formato existente, ajuste de texto activo y alto ajustado. |
| No modificar la plantilla original | Se copió y se trabajó sobre la copia; SHA-256 de la plantilla sin cambios: `da2fcb67efc54b3404adc67cc1af858f1c5ba2cb3cf3822d464c42c6729c0c9d`. |

## 8. Verificación técnica de las correcciones

| Verificación | Resultado |
|---|---|
| Notebook `MOD_01_AndinaLog_Regresion_Logistica.ipynb` ejecutado de principio a fin | 42 celdas, 25 de código, 0 errores y 0 tracebacks, 5 gráficos embebidos |
| Controles finales del notebook | 34 de 34 en OK |
| Gold no modificado | SHA-256 `f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479` al inicio y al cierre de la ejecución |
| Población de modelado | 25777 ventanas evaluables de 28448, 1200 viajes, prevalencia 0.050433 |
| Separación por viaje | 960 viajes de entrenamiento y 240 de prueba, intersección de grupos igual a 0 |
| Evaluación del conjunto de prueba | Una sola pasada por modelo, verificada por contador: `{'modelo_principal': 1, 'linea_base': 1}` |
| Métricas de prueba | PR AUC 0.324069, ROC AUC 0.759304, precisión 0.303191, recall 0.457831, F1 0.364800, frente a una línea base con recall 0 y PR AUC igual a la prevalencia |
| Segunda auditoría de las correcciones | 5 hallazgos menores cerrados, 0 críticos y 0 importantes, sin regresiones |

## 9. Estado de las filas y próximos pasos

1. Asignar un responsable real en las seis filas. Ningún archivo oficial del proyecto contiene nombres de integrantes, por lo que se escribió `Asignar integrante` en lugar de inventar un nombre.
2. Completar los nombres de integrantes en la Sección 1 antes de la entrega.
3. Pasar cada fila de `Resuelto` a `Verificado` solo cuando un integrante distinto de quien hizo la corrección confirme la evidencia, anotando su nombre.
4. Recibida la Rúbrica S12, copiar sus hallazgos desde la Sección 5 a partir de la fila 23 del Excel, respetando redacción, Prioridad y Categoría, y completar la Fecha de la Preentrega y el Estado recibido.
5. Si el estado de la Rúbrica resulta `LISTA PARA DEFENSA`, este archivo no se entrega.

## 10. Rutas

- Excel del plan: `documentacion/Plan_de_Correcciones_Grupo06_AndinaLog_03B.xlsx`
- Este informe: `Informe_Plan_de_Correcciones_Grupo06_AndinaLog_03B.md`
- Plantilla oficial de origen: `C:/Users/remrodri/Downloads/GIAD-M3_Plantilla_Plan_de_Correcciones.xlsx` (sin modificar)
- Contrato oficial de variables: `documentacion/GIAD-M3_Variables_Objetivo_y_Predictoras_Minima.md`
- Cumplimiento del contrato oficial: `documentacion/Contrato_03B_Cumplimiento_Variables_Objetivo_y_Predictoras.md`
- Informe del modelo: `informes/modelado/Informe_MOD_01_AndinaLog_Regresion_Logistica.md`
- Métricas de prueba, validación y sensibilidad: `datos/modelado/metricas_mod_01_regresion_logistica.csv`

Generado el 2026-09-25 a partir del contenido del propio Excel, para que el informe y la planilla no puedan divergir.
