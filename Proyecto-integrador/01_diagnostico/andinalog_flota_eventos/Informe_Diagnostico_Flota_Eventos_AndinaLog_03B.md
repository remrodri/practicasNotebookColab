# Informe de diagnóstico — Eventos de flota AndinaLog 03B

## Objetivo

Evaluar la calidad técnica y de negocio del JSON sin modificar los valores recibidos. El documento se aplana a una fila por evento y cada campo recibe su bandera de cuarentena y su motivo.

## Resultado

| Métrica | Resultado |
|---|---:|
| Eventos recibidos | 192 |
| Eventos únicos | 184 |
| Copias exactas posteriores | 8 |
| Lecturas `N/D` | 10 |
| `reconocido` no informado | 22 |
| Filas en cuarentena de diagnóstico | 8 |

Los 30 `camion_id` existen en Flota. Los formatos de identificadores son válidos, todas las fechas pueden interpretarse y no existen eventos posteriores a la fecha de exportación. Los catálogos de tipo y severidad cumplen el contrato.

## Decisiones

- La segunda aparición de cada uno de los 8 eventos duplicados se marca para cuarentena. La primera conserva el evento real.
- `N/D` se documenta como lectura no disponible y no invalida todo el evento.
- `reconocido` ausente se conserva como información desconocida; no se imputa como `False`.
- `valor_lectura` no se interpreta como una misma magnitud para todos los tipos, porque la fuente no declara una unidad común.
- Las fechas sin zona se consideran hora de Bolivia conforme a la decisión del proyecto.

## Salidas

1. `andinalog_flota_eventos_diagnosticado.csv`: las 192 filas y sus banderas.
2. `andinalog_flota_eventos_cuarentena.csv`: las 8 copias posteriores.
3. `andinalog_flota_eventos_reporte_calidad.csv`: conteos de control.

