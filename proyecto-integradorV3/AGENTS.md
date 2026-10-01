# Agentes del proyecto AndinaLog 03B

## Propósito

Mantener los notebooks, datos e informes de AndinaLog 03B reproducibles, explicados en lenguaje sencillo y coherentes entre sí.

## Orden del proyecto

1. `01-Diagnostico`: examina Bronze sin modificarlo.
2. `02-Bronze-silver`: limpia, transforma y separa cuarentena.
3. `03-Silver-gold`: crea variables temporales y el objetivo futuro.
4. `04-EDA`: analiza Gold y responde las preguntas con gráficos.
5. `05-Regresion-logistica`: entrena y evalúa el modelo.
6. `06-Documentacion`: consolida contrato, informe y presentación.

## Enrutamiento de skills

- Plan nuevo o cambio importante: `andinalog-notebook-planner`.
- CSV nuevo: `andinalog-data-intake`.
- Coordinación general: `andinalog-project-router`.
- Notebook 01: `andinalog-nb01-diagnostico`.
- Notebook 02: `andinalog-nb02-bronze-silver`.
- Notebook 03: `andinalog-nb03-silver-gold`.
- Notebook 04: `andinalog-nb04-eda`.
- Notebook 05: `andinalog-nb05-regresion`.
- Antes de corregir: `andinalog-auditoria-inicial`.
- Después de corregir: `andinalog-auditoria-final`.
- Al cerrar la sesión: `andinalog-memory-updater`.

## Flujo obligatorio

Planificar → construir o modificar → ejecutar completo → auditoría inicial → corregir → auditoría final → actualizar informe y memoria.

## Reglas comunes

- No modificar ni sobrescribir Bronze.
- Preservar claves, trazabilidad y filas descartadas en cuarentena.
- No imputar mediciones físicas sin evidencia y justificación documentada.
- No inventar rangos térmicos por producto.
- Separar entrenamiento y prueba por `viaje_id`.
- No ajustar decisiones usando el conjunto de prueba.
- Una celda de texto debe explicar cada resultado importante en lenguaje no técnico.
- Toda cifra declarada debe provenir de una salida ejecutada.
- Cada notebook debe ejecutarse de arriba abajo sin errores antes de aprobarse.
- Si cambia un resultado, actualizar el informe asociado y la documentación que lo cite.
- Preservar cambios existentes que no pertenezcan a la tarea actual.

## Incorporación de datos

Todo archivo nuevo debe registrarse primero con `andinalog-data-intake`. El registro debe indicar ruta, capa, unidad de observación, clave, columnas, calidad, relaciones, notebook responsable y salida prevista.

## Auditorías

La auditoría inicial es de solo lectura y produce hallazgos numerados. La auditoría final verifica cada hallazgo con evidencia nueva y busca regresiones. Construcción y aprobación no deben confundirse.

## Memoria

`MEMORY.md` es el índice. Los detalles viven en `.opencode/memory/`. Ningún archivo de memoria puede superar 50 líneas. Actualizar solo decisiones, resultados comprobados, pendientes y siguiente paso; no copiar conversaciones ni salidas extensas.

## Definición de terminado

Un trabajo termina cuando el notebook está ejecutado, sus salidas existen, las cifras concilian, el informe coincide, la auditoría final no tiene hallazgos críticos y la memoria quedó actualizada.
