# AGENTS.md

## Alcance y estructura

- La raíz del repositorio es `practicasNotebookColab/`. Las rutas de los notebooks son relativas a esa raíz.
- `datasets/AndinaLog_03B_Bronce/` contiene los Bronze originales; no los modifiques.
- `proyecto-integrador/` contiene el trabajo V1 (diagnóstico, tratamiento, integración, EDA y modelado). `proyecto-integradorV2/` es un trabajo separado: no copies código, salidas, conteos ni decisiones de V1 automáticamente.
- El trabajo V2 está definido principalmente por el prompt S11 del docente y por `proyecto-integradorV2/SKILL.md`; `proyecto-integradorV2/AGENTS.template.md` resume sus entregables y reglas de dominio.

## Flujo de datos

- Mantén la separación Bronze → copia de trabajo → Silver y cuarentena. Conserva valores originales, banderas y motivos; no uses `dropna()` para ocultar o descartar errores silenciosamente.
- Inspecciona cada Bronze antes de definir reglas: no inventes columnas, claves, rangos, categorías ni reglas de imputación.
- Para cada fuente, entrega notebook ejecutado, informe `.md`, Silver y cuarentena. Valida que `filas_bronze == filas_silver + filas_cuarentena` salvo una transformación estructural documentada.
- En V2, centraliza reglas, rutas, columnas, formatos, zonas horarias, catálogos, rangos, centinelas e imputaciones en `config`; encadena funciones con `df.pipe()`.
- Fechas sin zona explícita se interpretan como `America/La_Paz`; convierte a UTC solo cuando la fuente o el contrato lo justifique. La regla específica de V2 exige UTC para Silver.
- Celsius es la unidad canónica; `-999` es centinela, no una medición. Las imputaciones deben ser reproducibles, auditables y sin información futura.

## Integración y modelado

- Antes de cada join declara unidad, claves, cardinalidad, dirección, cobertura y riesgo de multiplicación. Agrega hechos antes de unir hechos y conserva la población principal con `how="left"` cuando corresponda.
- Para series IoT, ordena y agrupa por `viaje_id` y tiempo antes de `shift`, `rolling` u objetivos futuros. No mezcles viajes.
- Separa train/validation/test por viajes completos y en orden temporal. Ajusta imputadores, codificadores y escaladores solo con train; selecciona modelo, hiperparámetros y umbral con validation; abre test una sola vez.
- Verifica tipos y disponibilidad temporal real de cada columna: el diccionario y la bandera precomputada no bastan. Evita fuga de información y no trates las asociaciones como causalidad.

## Ejecución y verificación

- No hay manifiesto, CI, suite de tests, lint, typecheck ni task runner definidos en este repositorio. La verificación principal es ejecutar los notebooks aplicables de principio a fin, con salidas visibles, y revisar sus CSVs/informes generados.
- Los notebooks existentes auto detectan la raíz buscando `datasets/AndinaLog_03B_Bronce/`; el flujo integrado también acepta `ANDINALOG_ROOT`. En Colab pueden usar `/content/drive/MyDrive/GIAD` mediante su configuración `ENTORNO`.
- Al modificar un notebook, conserva las rutas relativas a la raíz, la semilla cuando exista y las salidas ejecutadas; no sobrescribas Bronze.
- Para cambios de modelos, conserva evidencia de baseline, validación, test y métricas por error; una ejecución técnica no demuestra utilidad operativa.

## Referencias

- `documentacion/01_Definición del proyecto — AndinaLog 03B.md`
- `documentacion/Revision_Documentacion_Grupo06_AndinaLog_03B.md`
- `documentacion/02_Guía de trabajo — Proyecto Integrador AndinaLog 03B (hasta S6).md`
- `documentacion/03_Tablas_Relaciones_Joins_Seis_Subcasos_v8.md`
- `documentacion/GIAD-M3_Guia_Estudiantes_Contratos_Predictivos_v8.md`
