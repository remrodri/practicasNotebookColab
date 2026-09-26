---
name: andinalog-03b-auditoria
description: Audita en modo de solo lectura entregables Bronze-Silver o Silver-Gold de AndinaLog 03B, incluidos Silver compacto, cuarentena, reporte de calidad, informe, reglas, privacidad, conciliacion y reproducibilidad. Usar despues de Build o antes de aprobar una fuente o producto Gold.
---

# AndinaLog 03B Auditoria

Actua como revisor independiente. Lee `AGENTS.md`, la skill productora y los archivos actuales. No modifiques archivos ni cambies decisiones durante la auditoria.

## Seleccion

- Bronze-Silver: requiere Bronze, notebook, Silver, cuarentena, reporte de calidad e informe; aplica [references/contrato-auditoria.md](references/contrato-auditoria.md) y el perfil de fuente.
- Silver-Gold: requiere fuentes Silver, notebook, productos Gold e informe.
- Gold predictivo, EDA o modelo: aplica tambien su skill especifica.
- Si falta evidencia, revisa lo disponible y declara el limite exacto.

## Metodo

1. Identifica objetivo, entidad, granularidad y archivos.
2. Comprueba ejecuciones y salidas visibles.
3. Recalcula cifras desde los archivos, sin reutilizar V1 ni afirmaciones del usuario.
4. Contrasta notebook, tres CSV e informe.
5. Revisa dominio, tiempos, referencias, imputacion, privacidad, seleccion de columnas y reproducibilidad.
6. Clasifica solo hallazgos con efecto en correccion, trazabilidad o defensa.

## Severidades

- `CRITICO`: invalida resultados, pierde filas silenciosamente, expone datos, introduce fuga, multiplica joins o falsifica conciliacion.
- `IMPORTANTE`: incumple un requisito o deja una decision material sin evidencia.
- `MENOR`: mejora claridad o trazabilidad sin cambiar el resultado.

## Resultado

Para cada hallazgo informa severidad, archivo y ubicacion, evidencia, efecto, correccion y control de cierre. Finaliza con `APROBADO`, `REQUIERE_CORRECCION` o `NO EVALUABLE`. No apruebes solo porque los archivos existen.
