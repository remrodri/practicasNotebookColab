# Informe Técnico Final — Proyecto Integrador Módulo 3

## Requisitos generales

- **Formato:** WORD
- **Extensión máxima:** 6 páginas
- **Nombre sugerido:** `M3_EquipoXX_InformeFinal.docx`
- **Carpeta:** `03_Informe`

El informe técnico final debe conectar de manera coherente:

**Problema industrial → Datos → EDA → Modelo → Validación → Resultados → Interpretación → Recomendaciones**

---

# A. Problema y valor industrial

Esta sección debe presentar claramente el problema industrial que se pretende abordar.

Debe incluir:

- **Contexto y situación problemática concreta.**
- **Usuario o área que utilizará el resultado.**
- **Objetivo medible.**
- **Decisión que se pretende apoyar.**
- **Alcance del proyecto.**
- **Exclusiones.**
- **Criterio de éxito.**

La sección debe permitir responder:

> **¿Qué problema industrial se quiere resolver, quién utilizará los resultados y qué decisión se pretende apoyar?**

---

# B. Datos y preparación

Esta sección debe explicar los datos utilizados y todo el proceso realizado antes del análisis y modelado.

## 1. Descripción de las fuentes

Para cada una de las aproximadamente 10 tablas fuente del subcaso se debe indicar:

- Fuente.
- Periodo.
- Población o muestra.
- Unidad de observación.

## 2. Calidad de los datos

Documentar los problemas encontrados relacionados con:

- Valores faltantes.
- Valores atípicos.
- Duplicados.
- Inconsistencias.
- Posibles sesgos.

## 3. Preparación de los datos

Explicar:

- Transformaciones realizadas.
- Justificación de las transformaciones.
- Integración de las diferentes tablas.
- Prevención de fuga de información (_data leakage_).

## 4. Documentación y trazabilidad

Debe existir:

- Diccionario de datos tabla por tabla.
- Diccionario en formato largo.
- Trazabilidad de los datos.
- Resguardo de la versión original de cada archivo fuente.

La sección debe permitir responder:

> **¿De dónde provienen los datos, qué problemas tenían y cómo fueron preparados para obtener un dataset adecuado para el análisis?**

---

# C. Análisis Exploratorio de Datos (EDA)

El EDA debe estar relacionado directamente con el problema industrial.

Debe incluir:

- Distribuciones relevantes.
- Relaciones entre variables pertinentes al problema.
- Hallazgos interpretados.
- Anomalías relevantes.
- Segmentos relevantes.
- Efecto de los hallazgos sobre el modelado posterior.

## Importante

No se deben presentar únicamente gráficos descriptivos.

Cada hallazgo debería seguir aproximadamente la lógica:

**Evidencia → Hallazgo → Interpretación → Implicación**

Por ejemplo:

> Se observa **X comportamiento en los datos**. Esto indica **Y situación relevante para el problema industrial**, por lo que se considera **Z decisión o consideración para el modelado**.

La sección debe permitir responder:

> **¿Qué mostró el EDA antes de realizar el modelado y cómo influyeron esos descubrimientos en las decisiones posteriores?**

---

# D. Modelo y validación

Esta sección debe explicar el modelo utilizado y demostrar que su evaluación es adecuada.

Debe incluir:

## 1. Selección del modelo

- Modelo seleccionado.
- Justificación de su elección.
- Comparación o consideración frente a otras alternativas.

## 2. Baseline

Debe existir una:

- **Referencia o baseline explícito.**

El modelo debe poder compararse contra esta referencia.

## 3. Pipeline y partición

Explicar:

- Preparación utilizada para el modelado.
- División de los datos.
- Pipeline utilizado.
- Medidas tomadas para evitar fuga de información.

## 4. Métricas

Presentar las métricas pertinentes para evaluar el modelo.

## 5. Validación

Debe analizarse:

- Resultados obtenidos.
- Rendimiento del modelo.
- Errores.
- Estabilidad.
- Incertidumbre.

La sección debe permitir responder:

> **¿Por qué se eligió este modelo, contra qué referencia se compara, qué tan bien funciona y dónde falla?**

---

# E. Interpretación y decisión

Esta sección debe transformar los resultados técnicos en información útil para el contexto industrial.

Debe incluir:

## Hallazgo principal

Presentar el principal resultado utilizando **lenguaje industrial**, evitando limitar la explicación únicamente a métricas estadísticas o de Machine Learning.

## Recomendaciones

Las recomendaciones deben ser:

- Específicas.
- Priorizadas.
- Respaldadas por evidencia.

Debe existir una conexión clara:

**Resultado → Interpretación → Recomendación**

## Diferenciación conceptual

El informe debe distinguir entre:

- **Resultado:** lo que muestran directamente los datos o el modelo.
- **Inferencia:** interpretación derivada de los resultados.
- **Recomendación:** acción propuesta a partir de la evidencia.
- **Causalidad:** afirmación de que una variable o fenómeno produce otro.

No debe afirmarse causalidad si los datos y el análisis no permiten demostrarla.

La sección debe permitir responder:

> **¿Qué decisión industrial puede apoyarse utilizando la evidencia obtenida?**

---

# F. Responsabilidad, continuidad y uso de IA

Esta sección debe documentar las limitaciones y el uso responsable de los resultados.

## 1. Limitaciones

Incluir:

- Limitaciones técnicas.
- Limitaciones de los datos.
- Limitaciones del modelo.
- Aspectos que no pueden concluirse con los resultados disponibles.

## 2. Responsabilidad y privacidad

Considerar:

- Privacidad.
- Sesgos.
- Riesgos.
- Supervisión humana.
- Límites de uso.

No deben exponerse:

- Datos personales.
- Credenciales.
- Secretos operativos.
- Información industrial no autorizada.

## 3. Uso de Inteligencia Artificial

Se debe declarar explícitamente:

- Herramienta de IA utilizada.
- Propósito para el cual fue utilizada.
- Contenido asistido mediante IA.
- Forma en que se realizó la verificación humana.

Si no se utilizó IA, debe incluirse una declaración expresa indicando que no se utilizó.

### Ejemplo de estructura

**Herramienta utilizada:** ChatGPT.

**Propósito:** apoyo en la revisión, estructuración y documentación del análisis.

**Contenido asistido:** apoyo en redacción, interpretación y revisión de determinados contenidos del proyecto.

**Verificación humana:** los integrantes revisaron y validaron los resultados, código, cálculos, interpretaciones y conclusiones antes de incorporarlos al proyecto.

> Este texto debe adecuarse al uso real que haya realizado el equipo de las herramientas de IA.

## 4. Continuidad hacia el Módulo 4

Identificar los elementos que pueden transferirse al siguiente módulo:

- KPI.
- Variables relevantes.
- Métricas.
- Necesidades de visualización.

La sección debe permitir responder:

> **¿Cuáles son las limitaciones del trabajo, cómo debe utilizarse responsablemente y qué resultados pueden continuar utilizándose en el Módulo 4?**

---

# Distribución sugerida de las 6 páginas

| Página aproximada | Contenido                                                 |
| ----------------- | --------------------------------------------------------- |
| 1                 | A. Problema y valor industrial                            |
| 1–2               | B. Datos y preparación                                    |
| 2–3               | C. Análisis exploratorio (EDA)                            |
| 3–4               | D. Modelo y validación                                    |
| 4–5               | E. Interpretación y decisión                              |
| 5–6               | F. Responsabilidad, limitaciones, uso de IA y continuidad |

> Esta distribución es una propuesta para cumplir el límite de seis páginas; la guía no establece una cantidad específica de páginas para cada sección.

---

# Relación del informe con la evaluación

El informe técnico participa como evidencia en los cuatro criterios grupales principales:

| Criterio                                                 | Peso | Parte del informe |
| -------------------------------------------------------- | ---: | ----------------- |
| Problema, valor industrial y análisis exploratorio       |  20% | A y C             |
| Datos: calidad, documentación y reproducibilidad técnica |  20% | B                 |
| Modelo: selección, construcción y validación             |  20% | D                 |
| Interpretación, recomendaciones, ética y uso responsable |  20% | E y F             |

Por tanto, las seis secciones del informe están directamente relacionadas con la evaluación grupal del proyecto.

---

# Verificación antes de entregar

Antes de generar el PDF final se debe comprobar:

- [ ] El informe tiene máximo 6 páginas.
- [ ] El problema industrial está claramente definido.
- [ ] Existe un objetivo medible.
- [ ] Está identificada la decisión que se pretende apoyar.
- [ ] Las fuentes de datos están documentadas.
- [ ] Se documenta la calidad de los datos.
- [ ] Las transformaciones están justificadas.
- [ ] Existe trazabilidad de los datos.
- [ ] El EDA contiene interpretaciones y no solamente gráficos.
- [ ] Los hallazgos del EDA están relacionados con el problema.
- [ ] El modelo está justificado.
- [ ] Existe un baseline.
- [ ] La validación utiliza métricas pertinentes.
- [ ] No existe fuga de información.
- [ ] Se analizan errores, estabilidad e incertidumbre.
- [ ] Las recomendaciones están respaldadas por evidencia.
- [ ] No se afirma causalidad sin evidencia.
- [ ] Se presentan las limitaciones.
- [ ] Se consideran privacidad, sesgos y riesgos.
- [ ] El uso de IA está declarado.
- [ ] Se identifican resultados transferibles al Módulo 4.
- [ ] Las cifras del informe coinciden con los notebooks.
- [ ] Las métricas coinciden con los notebooks.
- [ ] Los gráficos coinciden con los resultados obtenidos.
- [ ] Las conclusiones coinciden entre notebook, informe y presentación.

---

# Idea central del Informe Técnico Final

El informe no debe ser simplemente un resumen de todo el código realizado.

Debe demostrar una cadena lógica y trazable:

**Problema industrial**

↓

**Datos disponibles**

↓

**Calidad y preparación de los datos**

↓

**EDA y descubrimiento de patrones**

↓

**Selección y construcción del modelo**

↓

**Validación y métricas**

↓

**Resultados**

↓

**Interpretación industrial**

↓

**Recomendaciones respaldadas por evidencia**

↓

**Limitaciones, ética y uso responsable**

↓

**Continuidad hacia el Módulo 4**
