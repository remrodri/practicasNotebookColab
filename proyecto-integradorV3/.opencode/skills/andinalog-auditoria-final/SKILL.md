---
name: andinalog-auditoria-final
description: Verifica después de las correcciones que los hallazgos iniciales de AndinaLog 03B estén resueltos y que no existan regresiones.
---

# Auditoría final

Requiere el informe de auditoría inicial y los archivos corregidos. No asumas que una edición resolvió el problema: comprueba salidas ejecutadas.

## Revisión por hallazgo

Para cada identificador registra:

- Resuelto.
- Parcialmente resuelto.
- No resuelto.
- No aplica, con justificación.

Incluye evidencia actual, no solo una descripción del cambio.

## Pruebas de regresión

- Ejecución completa sin errores.
- Conteos y conciliaciones conservados.
- Salidas e informes regenerados.
- Variables, claves y contratos intactos.
- Interpretaciones consistentes con los nuevos resultados.
- Ningún dato fuente sobrescrito.

## Salida

Guarda `.opencode/audits/AAAA-MM-DD-final-<alcance>.md`. Aprueba solo si no quedan hallazgos críticos o altos y todos los criterios de aceptación se cumplen. Después activa `andinalog-memory-updater`.
