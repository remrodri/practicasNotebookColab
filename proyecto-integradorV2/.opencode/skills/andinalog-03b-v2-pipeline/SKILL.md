---
name: andinalog-03b-v2-pipeline
description: Coordina AndinaLog Grupo 06 subcaso 03B, mantiene decisiones comunes y dirige tareas a Bronze-Silver, Silver-Gold, Gold IoT, EDA, modelo o auditoria. Usar para alcance, orden y coherencia; no para crear carpetas.
---

# AndinaLog 03B V2 Pipeline

Coordina V2 desde fuentes hasta modelo. El prompt S11 y el contrato oficial del subcaso prevalecen. No copies codigo, estructuras, conteos ni conclusiones de V1.

## Enrutamiento

- Fuente CSV, JSON o TXT: `$andinalog-03b-bronze-silver`.
- Integracion Silver-Gold: `$andinalog-03b-silver-gold`.
- Producto predictivo minimo: `$andinalog-03b-iot-gold`, luego `$andinalog-03b-iot-eda` y `$andinalog-03b-iot-regresion-logistica`.
- Revision independiente: `$andinalog-03b-auditoria`.

## Reglas comunes

1. Inspecciona el archivo real y conserva Bronze.
2. Cada Bronze-Silver entrega notebook, informe, Silver compacto, cuarentena investigable y reporte de calidad por regla.
3. Usa `America/La_Paz` para interpretar timestamps sin zona y UTC como tiempo canonico.
4. Mantiene trazabilidad de transformaciones, imputaciones, cuarentena y joins sin duplicar columnas sin funcion.
5. Usa prompts estandarizados; los perfiles resuelven particularidades de fuente.

## Compuerta a Gold

Cada fuente necesaria debe tener notebook ejecutado, Silver, cuarentena, reporte de calidad, informe, conciliacion valida y auditoria sin hallazgos criticos o importantes. Documenta fuentes usadas, contextuales y excluidas. Para el modelo minimo solo IoT Silver es obligatorio.

## Evidencia

No conviertas una suposicion en regla. Distingue hechos observados, inferencias y recomendaciones. El reporte de calidad no participa en `Bronze = Silver + cuarentena`; se verifica regla por regla y sus activaciones pueden solaparse.
