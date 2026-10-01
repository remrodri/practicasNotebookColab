---
name: andinalog-data-intake
description: Registra y perfila un CSV nuevo o reemplazado antes de incorporarlo al pipeline AndinaLog 03B.
---

# Ingreso de datos

Trabaja primero en modo de solo lectura. No limpies ni sobrescribas la fuente.

## Perfil mínimo

- Ruta, nombre, tamaño, filas, columnas y huella cuando sea posible.
- Capa propuesta: Bronze, Silver, Gold o auxiliar.
- Unidad de observación y clave candidata.
- Columnas, tipos, ejemplos y dominio aparente.
- Faltantes, duplicados, sentinelas y valores fuera de rango.
- Periodo temporal y zona horaria.
- Identificadores sensibles u operativos.
- Relación y cardinalidad con datasets existentes.

## Decisión de incorporación

Indica si el archivo requiere un notebook nuevo, amplía uno existente o solo aporta contexto. No inventes joins ni reglas de negocio. Para rangos de temperatura por producto exige una fuente contractual identificable.

## Registro

Crea o actualiza `.opencode/memory/datasets/<nombre>.md` con máximo 50 líneas. Incluye notebook responsable, salida esperada, riesgos y decisión pendiente. Después solicita un plan con `andinalog-notebook-planner`.
