# Informe de integración temporal — IoT y eventos de flota

## Objetivo

Enriquecer la Evidencia 3 de AndinaLog con información telemática histórica disponible al momento de cada lectura. La integración respeta la unidad de análisis de una lectura IoT y evita fuga de información futura.

## Regla aplicada

Un evento participa cuando cumple simultáneamente:

1. pertenece al mismo `camion_id`;
2. `timestamp_evento < timestamp_lectura`;
3. cae dentro de la ventana histórica correspondiente.

No se realiza una unión muchos a muchos. Los eventos se resumen antes de agregarlos a cada lectura mediante búsquedas temporales y conteos.

## Variables incorporadas

| Familia | Variables |
|---|---|
| Frecuencia | Eventos previos en 60 minutos, 180 minutos y 24 horas |
| Cadena de frío | Alertas térmicas previas en 60 minutos, 180 minutos y 24 horas |
| Estado operativo | Fallas de motor, eventos de severidad alta y eventos no reconocidos en 24 horas |
| Calidad de respuesta | Reconocimientos faltantes durante las 24 horas previas |
| Recencia | Minutos desde el último evento y desde la última alerta térmica |
| Configuración | Umbral de temperatura, radio de geocerca, último mantenimiento y días desde mantenimiento |

`valor_lectura_numerico` no se incorporó como predictor porque su unidad depende del tipo de evento y el contrato de origen no la declara.

## Auditoría de integración

| Control | Resultado |
|---|---:|
| Lecturas IoT de entrada | 28.677 |
| Lecturas después de integrar | 28.677 |
| Eventos Silver disponibles | 184 |
| Camiones en IoT | 30 |
| Camiones en eventos | 30 |
| Cobertura de configuración | 100 % |
| Lecturas con evento previo en 60 minutos | 282 |
| Lecturas con evento previo en 180 minutos | 832 |
| Lecturas con evento previo en 24 horas | 5.243 |
| Lecturas con alerta térmica previa en 24 horas | 1.290 |

Las pruebas confirman que no se perdieron ni multiplicaron lecturas, los conteos nunca son negativos, las ventanas mayores contienen a las menores y la recencia usa eventos estrictamente anteriores.

## Hallazgos exploratorios

| Grupo | Lecturas | Tasa de desviación en próximos 60 min | Desvío futuro medio |
|---|---:|---:|---:|
| Sin evento previo en 24 h | 23.434 | 4,32 % | -1,897 °C |
| Con evento previo en 24 h | 5.243 | 5,89 % | -1,753 °C |

La presencia de eventos previos coincide con una tasa futura mayor, pero este resultado muestra asociación y no causalidad. Además, una alerta térmica previa por sí sola presenta una tasa de 5,50 % frente a 4,57 % en las demás lecturas.

## Uso en las siguientes sesiones

- **S6, regresión:** comparar el error de un modelo base sin eventos contra el mismo modelo enriquecido.
- **S7, clasificación:** comprobar si estas variables mejoran recall y costo operativo de falsos negativos.
- **S9–S10:** utilizar solo variables disponibles al instante de predicción y mantener el test temporal sellado.

La tabla enriquecida conserva las mismas columnas de la Evidencia 3 y añade únicamente variables históricas de eventos.

