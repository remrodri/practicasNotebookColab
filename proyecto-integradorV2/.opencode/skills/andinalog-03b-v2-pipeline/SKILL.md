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
- Para el alcance predictivo minimo, usa en orden `$andinalog-03b-iot-gold`, `$andinalog-03b-iot-eda` y `$andinalog-03b-iot-regresion-logistica` despues de aprobar IoT Silver.

## Interaccion estandar

Los prompts de Plan, Build y Auditoria deben mantener la misma estructura entre fuentes. Las diferencias de productos, flota, WMS, IoT, inventario, costos, JSON de eventos, HR y bitacora se resuelven mediante los perfiles incluidos en la skill Bronze-Silver. No obligues al usuario a repetir reglas ya codificadas en esos perfiles.

## Reglas comunes

1. Conserva Bronze sin modificar y crea una copia de trabajo.
2. No mezcles automaticamente codigo, estructuras, salidas o conteos de V1 con V2.
3. Cada notebook se entrega ejecutado junto con su informe MD y sus archivos de salida.
4. Interpreta fechas sin zona explicita en `America/La_Paz` y usa UTC como tiempo canonico de Silver.
5. Conserva trazabilidad de transformaciones, imputaciones, cuarentena y joins.
6. V3 sera el espacio para comparar y combinar V1 y V2.

## Compuerta previa a Gold

Antes de dirigir una tarea a Silver-Gold, verifica que cada fuente necesaria tenga notebook ejecutado, Silver, cuarentena, informe, conciliacion valida y auditoria sin hallazgos criticos o importantes. No exijas que las nueve fuentes entren en todos los productos. Registra cuales son utilizadas, contextuales o excluidas y el motivo.

Revisa tambien que las decisiones transversales sean consistentes: semantica temporal, codigos de calidad, tratamiento de claves, unidades, privacidad y definicion de imputacion.

Para el modelo minimo a 60 minutos solo IoT Silver es obligatorio. No exijas joins ni las nueve fuentes si IoT contiene temperatura, humedad, desviacion actual, identificador de viaje u orden y timestamp.

## Decisiones que requieren evidencia

No conviertas una suposicion en regla. Distingue hechos observados, inferencias y recomendaciones.
