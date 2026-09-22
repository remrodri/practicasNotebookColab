# Informe de diagnóstico — Flota v2

Grupo 06, AndinaLog 03B. Fecha: 2026-09-22.

## Qué se evaluó

ID CAM-## único; centros Cochabamba, La Paz, Santa Cruz, Oruro o Tarija; tipo Seco o Refrigerado; capacidad numérica positiva en kg. Menos de 750 kg requiere revisión de ficha, sin cuarentena automática. Se conservaron todos los valores Bronze. El diagnóstico detecta y explica; no normaliza ni imputa.

## Resultado verificado

| Medida | Filas |
|---|---:|
| Bronze y diagnosticado | 32 |
| Cuarentena diagnóstica | 4 |
| Sin cuarentena inicial | 28 |

La salida incluye, para cada una de las 4 columnas Bronze, una bandera `*_en_cuarentena` y su `*_motivo`. `en_cuarentena` resume las banderas. El reporte de calidad contiene conteos globales y por campo. `cuarentena` contiene exactamente las filas marcadas del diagnosticado.

## Destino

El tratamiento lee el diagnosticado completo, incluidas las 4 filas marcadas, porque algunas anomalías tienen resolución trazable. 750 kg es umbral de revisión, no mínimo normativo. La compatibilidad térmica de una asignación debe analizarse junto con el producto y el viaje.
