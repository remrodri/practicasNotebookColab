---
name: andinalog-project-router
description: Coordina tareas de AndinaLog 03B, selecciona la skill correcta y mantiene coherencia entre notebooks, datos, informes, auditorías y memoria.
---

# Coordinación del proyecto

Lee `AGENTS.md` y `MEMORY.md` antes de decidir el flujo.

## Enrutamiento

- Cambio sin plan aprobado: usar `andinalog-notebook-planner`.
- CSV nuevo o reemplazado: usar `andinalog-data-intake`.
- Trabajo en un notebook: usar su skill numerada.
- Revisión antes de cambios: usar `andinalog-auditoria-inicial`.
- Verificación después de cambios: usar `andinalog-auditoria-final`.
- Cierre de trabajo: usar `andinalog-memory-updater`.

## Decisiones comunes

- Mantén Bronze inmutable.
- No inventes reglas de negocio o rangos por producto.
- Conserva trazabilidad, cuarentena y conciliación de filas.
- Ejecuta el notebook completo y actualiza su informe.
- Si cambia una cifra citada en documentación, señala los archivos que también requieren actualización.

## Salida

Indica alcance, skill elegida, archivos afectados, dependencias y condición de terminado. No crees carpetas o notebooks nuevos sin necesidad demostrada.
