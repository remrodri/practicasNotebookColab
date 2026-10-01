---
name: andinalog-nb01-diagnostico
description: Crea, revisa o corrige el Notebook 01 de diagnóstico inicial del CSV Bronze de AndinaLog 03B. Úsala para perfilar la fuente sin modificarla y documentar estructura, calidad, claves, rangos y problemas que deberá resolver Bronze-Silver.
---

# Notebook 01: diagnóstico

## Objetivo

Examinar la fuente Bronze de forma reproducible y comprensible, sin limpiar ni alterar sus datos.

## Entradas

- CSV Bronze indicado por el usuario.
- Requisitos del caso 03B disponibles en el proyecto.

## Procedimiento

1. Confirmar la ruta, existencia y lectura del archivo.
2. Mostrar dimensiones, nombres de columnas, tipos y una muestra prudente.
3. Explicar la unidad de observación en lenguaje sencillo.
4. Medir valores faltantes, filas duplicadas y duplicados según la clave candidata.
5. Revisar fechas, identificadores, categorías y rangos observados.
6. Diferenciar claramente observaciones de datos y reglas oficiales; no inventar umbrales.
7. Resumir los problemas encontrados y su tratamiento propuesto para el Notebook 02.
8. Incluir celdas Markdown que interpreten cada resultado importante.

## Restricciones

- No modificar, imputar, eliminar ni sobrescribir el Bronze.
- No construir todavía Silver, Gold, EDA final ni modelos.
- No presentar un rango observado como regla de negocio.
- Evitar análisis que no ayuden a decidir la limpieza posterior.

## Salida mínima

- Notebook ejecutado de arriba abajo, sin errores.
- Diagnóstico con cifras verificables y explicaciones para público no técnico.
- Lista concreta de hallazgos que alimentará el plan del Notebook 02.

## Memoria

Al terminar, actualizar `MEMORY.md`, `.opencode/memory/notebooks/01-diagnostico.md`, la memoria del CSV Bronze y la sesión correspondiente.
