---
name: andinalog-notebook-planner
description: Diseña el plan verificable para crear o modificar un notebook de AndinaLog 03B antes de ejecutar cambios.
---

# Plan de notebook

Inspecciona el notebook, sus entradas, salidas, informe y memorias relacionadas. No modifiques archivos durante la planificación.

## El plan debe declarar

1. Objetivo y pregunta que resuelve.
2. Unidad de observación y población.
3. Archivos de entrada, claves y dependencias.
4. Salidas que se crearán o actualizarán.
5. Secciones y orden de celdas.
6. Reglas de calidad y conciliaciones.
7. Interpretaciones necesarias en lenguaje sencillo.
8. Pruebas de ejecución y criterios de aceptación.
9. Riesgos: fuga, duplicación, imputación, desbalance o falta de contrato.
10. Auditoría inicial, corrección, auditoría final y memoria.

## Cambios de alcance

Si falta una decisión de negocio que alteraría los resultados, detén el plan y solicítala. Si se agrega un CSV, envíalo primero a `andinalog-data-intake`.

## Resultado

Guarda planes aprobados en `.opencode/plans/AAAA-MM-DD-nombre.md`. El plan debe ser suficientemente concreto para que otra sesión lo ejecute sin reinterpretar el objetivo.
