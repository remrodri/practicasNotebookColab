# Informe de tratamiento — Eventos de flota AndinaLog 03B

## Objetivo

Consumir la salida diagnosticada, normalizar únicamente lo justificable y producir Silver sin perder los datos originales.

## Transformaciones

- Normalización de identificadores y categorías mediante espacios, mayúsculas y capitalización controlada.
- Conversión de los dos formatos de fecha observados a `YYYY-MM-DD HH:MM:SS`, interpretados como hora de Bolivia.
- Conversión de `valor_lectura` a número cuando es posible.
- Conversión de `N/D` a nulo analítico, acompañada por `valor_lectura_no_disponible=True`.
- Conversión de `reconocido` a booleano anulable y creación de `reconocido_faltante`.
- Conversión numérica de las configuraciones de temperatura y geocerca.
- Cálculo de `dias_desde_ultimo_mantenimiento` en el momento del evento.
- Conservación de cada dato recibido en columnas `*_original`.

## Resultado

| Métrica | Resultado |
|---|---:|
| Entrada diagnosticada | 192 |
| Silver | 184 |
| Cuarentena final | 8 |
| `N/D` conservados mediante bandera en Silver | 10 |
| `reconocido` faltante en Silver | 20 |

De los 22 reconocimientos faltantes originales, 2 pertenecían a copias duplicadas que quedaron en cuarentena final. No se imputaron estados ni unidades.

## Uso para modelado

Los eventos pueden agregarse por camión en ventanas previas de 60 minutos, 180 minutos o 24 horas. El enlace con IoT debe usar `camion_id` y únicamente eventos con `timestamp_bolivia` estrictamente anterior a la lectura, evitando fuga de información y multiplicación de filas.

`valor_lectura_numerico` no debe entrar automáticamente al primer modelo: su significado depende de `tipo` y la fuente no declara una unidad por categoría.

## Salidas

1. `andinalog_flota_eventos_silver.csv`: 184 eventos únicos y tratados.
2. `andinalog_flota_eventos_cuarentena_final.csv`: 8 copias posteriores.
3. `andinalog_flota_eventos_reporte_calidad.csv`: conteos de control.

