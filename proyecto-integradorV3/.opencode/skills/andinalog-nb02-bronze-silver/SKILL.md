---
name: andinalog-nb02-bronze-silver
description: Crea, revisa o corrige el Notebook 02 que transforma el CSV Bronze de telemetría de AndinaLog 03B en Silver y cuarentena. Úsala para limpieza, tipado, calidad, imputaciones justificadas, trazabilidad por fila y conciliación de salidas.
---

# Notebook 02: Bronze a Silver

## Objetivo

Limpiar y estandarizar la telemetría Bronze, separar registros no utilizables y conservar trazabilidad completa.

## Entradas y salidas

- Entrada: CSV Bronze diagnosticado en el Notebook 01.
- Salidas: CSV Silver, CSV de cuarentena e informe Markdown correspondiente.

## Procedimiento

1. Cargar configuración, rutas y reglas explícitas al inicio.
2. Preservar una referencia estable como `_fila_bronze` antes de transformar.
3. Normalizar nombres, tipos, fechas, texto y valores categóricos documentados.
4. Aplicar reglas de calidad mediante funciones claras y pasos reproducibles.
5. Imputar solo cuando exista justificación técnica y trazabilidad; explicar método, alcance y riesgo.
6. Enviar a cuarentena los registros que no puedan corregirse de manera confiable.
7. Añadir motivo de cuarentena entendible y conservar los valores originales necesarios para auditar.
8. Verificar que `filas Bronze = filas Silver + filas cuarentena`, salvo duplicados eliminados explícitamente y contabilizados.
9. Guardar las salidas y generar el informe con cifras obtenidas del proceso.
10. Explicar en Markdown qué ocurrió y qué significa para una persona no técnica.

## Restricciones

- No sobrescribir el archivo Bronze.
- No inventar temperaturas válidas por producto sin una fuente oficial.
- No ocultar descartes, imputaciones o cambios de tipo.
- No construir todavía variables temporales, objetivo predictivo ni modelo.

## Criterio de cierre

El notebook debe ejecutarse sin errores, las cuentas deben conciliar y una segunda ejecución debe producir resultados equivalentes.

## Memoria

Actualizar las memorias del Notebook 02, Bronze, Silver y la sesión activa.
