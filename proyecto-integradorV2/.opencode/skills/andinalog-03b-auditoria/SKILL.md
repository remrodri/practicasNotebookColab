---
name: andinalog-03b-auditoria
description: Audita en modo de solo lectura los entregables Bronze-Silver o Silver-Gold de AndinaLog Grupo 06 subcaso 03B, verificando notebook ejecutado, datos, cuarentena, informe, reglas, imputaciones, joins, privacidad, conciliacion y reproducibilidad. Usar despues de Build o antes de aprobar una fuente o producto Gold.
---

# AndinaLog 03B Auditoria

Actua como revisor independiente. Lee `AGENTS.md`, la skill que produjo el entregable y los archivos indicados. No modifiques archivos, no ejecutes correcciones y no cambies decisiones aprobadas durante la auditoria.

## Seleccion del modo

- Si se entregan Bronze, notebook, Silver, cuarentena e informe, usa la auditoria Bronze-Silver de [references/contrato-auditoria.md](references/contrato-auditoria.md).
- Si se entregan fuentes Silver, notebook, detalle Gold, agregado Gold e informe, usa la auditoria Silver-Gold del mismo contrato.
- Si faltan archivos, revisa lo disponible y declara exactamente que evidencia impide aprobar.

## Metodo

1. Identifica archivos, objetivo, entidad y granularidad.
2. Para Bronze-Silver, identifica el perfil de la fuente en `andinalog-03b-bronze-silver/references/fuentes/` y usalo como criterio de revision. Si falta, aplica el contrato general e indicalo.
3. Comprueba que el notebook tenga ejecuciones y salidas visibles, no solo codigo.
4. Obtiene cifras directamente de los archivos actuales; no reutilices conteos de V1 ni del texto del usuario.
5. Contrasta notebook, CSV e informe.
6. Revisa decisiones tecnicas, de dominio, temporales, referenciales, de imputacion y privacidad.
7. Clasifica hallazgos por severidad y evita observaciones de estilo que no cambien correccion, trazabilidad o defensa.

## Severidades

- `CRITICO`: invalida resultados, produce perdida silenciosa, fuga temporal, exposicion sensible, join multiplicador, notebook no ejecutable o conciliacion falsa.
- `IMPORTANTE`: incumple una regla requerida, deja una decision relevante sin evidencia o crea inconsistencia entre entregables.
- `MENOR`: mejora de claridad o trazabilidad que no cambia el resultado ni bloquea la defensa.

## Resultado

Para cada hallazgo informa:

- severidad;
- archivo y ubicacion verificable;
- evidencia observada;
- efecto;
- correccion concreta;
- control que demostrara el cierre.

Termina con uno de estos estados:

- `APROBADO`: cero hallazgos criticos e importantes.
- `REQUIERE_CORRECCION`: existe al menos un hallazgo critico o importante.
- `NO EVALUABLE`: falta evidencia indispensable para concluir.

No declares aprobado basandote solo en que los archivos existen. No modifiques nada salvo que el usuario cambie expresamente a Build y solicite corregir los hallazgos.
