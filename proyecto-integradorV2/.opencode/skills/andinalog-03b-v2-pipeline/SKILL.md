---
name: andinalog-03b-v2-pipeline
description: Coordina el proyecto V2 de AndinaLog Grupo 06 subcaso 03B, mantiene sus decisiones comunes y dirige cada tarea a la skill Bronze-Silver o Silver-Gold. Usar para revisar alcance, orden de trabajo, coherencia entre entregables o reglas compartidas; no usar para crear carpetas.
---

# AndinaLog 03B V2 Pipeline

Coordina V2 desde los archivos fuente hasta Gold. El prompt S11 del docente es la especificacion principal. Esta skill no crea estructuras de carpetas.

## Limites de V2

- No copies codigo, salidas, conteos ni estructuras de V1 sin una solicitud expresa del usuario.
- Puedes usar las fuentes oficiales y el contexto de negocio para formular y justificar reglas.
- Inspecciona cada archivo Bronze antes de definir reglas. No inventes columnas, categorias, rangos ni claves.
- Entrega cada notebook `.ipynb` junto con un informe `.md` que refleje los resultados realmente ejecutados.
- V3 sera el espacio para comparar y combinar V1 y V2.

## Seleccion del flujo

- Para procesar un CSV, JSON o TXT Bronze, usa `$andinalog-03b-bronze-silver`.
- Para integrar fuentes Silver y producir detalle y agregado Gold, usa `$andinalog-03b-silver-gold`.
- Para revisar el avance general, el orden, la coherencia o una decision transversal, permanece en esta skill.
- Aplica como contexto comun [references/dominio-andinalog.md](references/dominio-andinalog.md).

## Reglas comunes

1. Conserva Bronze sin modificar y crea una copia de trabajo.
2. No mezcles automaticamente codigo, estructuras, salidas o conteos de V1 con V2.
3. Cada notebook se entrega ejecutado junto con su informe MD y sus archivos de salida.
4. Interpreta fechas sin zona explicita en `America/La_Paz` y usa UTC como tiempo canonico de Silver.
5. Conserva trazabilidad de transformaciones, imputaciones, cuarentena y joins.
6. V3 sera el espacio para comparar y combinar V1 y V2.

## Decisiones que requieren evidencia

No conviertas una suposicion en regla. Distingue hechos observados, inferencias y recomendaciones.
