# Contrato de ingesta — Eventos de flota AndinaLog 03B

## Fuente y estructura

- **Fuente:** plataforma telemática `TELEMATICA-AndinaLog`.
- **Formato:** JSON jerárquico, con camiones, configuración y eventos.
- **Granularidad analítica:** un evento por fila después del aplanado.
- **Clave esperada:** `evento_id` único con formato `EVT-ALOG-#####`.
- **Clave de integración:** `camion_id`, con formato `CAM-##` y referencia a Flota.
- **Zona horaria:** las fechas sin zona explícita se interpretan en `America/La_Paz`.

## Semántica y calidad

| Campo | Contrato |
|---|---|
| `tipo` | EXCESO_VELOCIDAD, ALERTA_TEMP_CADENA_FRIO, MANTENIMIENTO_PROGRAMADO, FALLA_MOTOR o GEOCERCA_SALIDA |
| `severidad` | Baja, Media o Alta |
| `valor_lectura` | Valor asociado al tipo; no existe una unidad común declarada |
| `reconocido` | verdadero, falso o nulo cuando la fuente no informa el estado |
| `umbral_temp_cabina_c` | Configuración en °C, rango contractual 0 a 15 |
| `geocerca_radio_km` | Configuración en km, rango contractual mayor que 0 y hasta 200 |
| `ultimo_mantenimiento` | Fecha válida y no posterior a la exportación |

`N/D` significa lectura no disponible. No equivale a cero. La ausencia de `reconocido` tampoco equivale a falso.

