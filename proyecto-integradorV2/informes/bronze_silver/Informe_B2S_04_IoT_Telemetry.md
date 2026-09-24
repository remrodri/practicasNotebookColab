# Informe B2S 04 - AndinaLog IoT Telemetry

## Objetivo, entidad y granularidad
Conversion auditada de lecturas IoT desde Bronze a Silver y cuarentena.
- Entidad: lectura_iot_cabina.
- Granularidad: una fila por viaje_id y timestamp normalizados.
- Clave de lectura: ['viaje_id', 'timestamp'].

## Perfil Bronze
- Filas: 28920; columnas: 10.
- Columnas: ['timestamp', 'viaje_id', 'order_id', 'camion_id', 'producto_id', 'temperatura_cabina_c', 'temp_unit', 'humedad_cabina_pct', 'desviacion_termica_flag', 'desviacion_proximos_60min_flag'].
- Tipos recibidos: {'timestamp': 'str', 'viaje_id': 'str', 'order_id': 'str', 'camion_id': 'str', 'producto_id': 'str', 'temperatura_cabina_c': 'str', 'temp_unit': 'str', 'humedad_cabina_pct': 'str', 'desviacion_termica_flag': 'str', 'desviacion_proximos_60min_flag': 'str'}.
- Vacios: {'timestamp': 0, 'viaje_id': 0, 'order_id': 0, 'camion_id': 0, 'producto_id': 0, 'temperatura_cabina_c': 80, 'temp_unit': 0, 'humedad_cabina_pct': 100, 'desviacion_termica_flag': 0, 'desviacion_proximos_60min_flag': 0}.
- Duplicados exactos: 230 filas.
- Claves de lectura duplicadas: 240 filas en 120 claves.
- Espacios en identificadores: {'viaje_id': 0, 'order_id': 0, 'camion_id': 50, 'producto_id': 0}.
- Fechas invalidas: 15; frecuencia observada en minutos: {0.0: 120, 30.0: 27572, 60.0: 13}.

## Temperatura, humedad y unidades
- Unidades observadas: {'C': 28865, 'F': 50, 'K': 5}.
- Fahrenheit convertido exactamente a Celsius: 50 filas.
- Kelvin no esperado enviado a cuarentena: 5 filas.
- Centinelas de temperatura: 120; centinelas de humedad: 0.
- Temperaturas ausentes: 80; humedades ausentes conservadas sin imputar: 100.
- Humedades fuera de 0-100: 15.
- No se aplican limites termicos inventados. La desviacion se evalua contra temperatura requerida y tolerancia de Producto Silver cuando estan disponibles.

## Desviaciones operacionales e imputacion
- Desviaciones termicas observadas: 951.
- Banderas de desviacion en proximos 60 minutos: 1342.
- Una desviacion operacional valida se conserva en Silver; no es un error de calidad.
- No se imputa ninguna variable. No se usan promedio, mediana, ffill, bfill ni lecturas futuras.

## Integridad referencial
- Filas sin WMS Silver: 4942.
- Filas sin Producto Silver: 3159.
- Filas sin Flota Silver: 1637.
- Las faltas de correspondencia son banderas informativas, no errores intrinsecos de sensor. Una contradiccion con una orden WMS existente si es bloqueante.

## Contradicciones respecto del plan
- hay 80 temperaturas vacias y 120 centinelas -999.0; el plan habia indicado ausencia de ambos.
- hay 100 humedades vacias, no 951.
- hay 15 fechas imposibles aunque todas cumplen el patron textual.
- hay 230 filas duplicadas exactas y 240 filas en 120 claves de lectura duplicadas.
- la frecuencia regular observada es 30 minutos, no 20-21.
- no se aplican limites termicos -50/50 o -10/40 porque no existe contrato que los sustente.
- las faltas referenciales se mantienen informativas, no bloqueantes, por no ser errores intrinsecos de sensor.

## Resultado y conciliacion
- Estados: {'valida_con_transformacion': 28448, 'cuarentena': 472}.
- Motivos de cuarentena: {'lectura_duplicada:viaje_id_timestamp': 240, 'centinela:temperatura_cabina_c': 120, 'temperatura_ausente': 80, 'humedad_fuera_rango_0_100': 15, 'timestamp_invalido': 15, 'unidad_temperatura_no_esperada:K': 5}.
- Banderas informativas: {'order_id_sin_correspondencia_wms_silver': 4942, 'producto_id_sin_correspondencia_silver': 3159, 'camion_id_sin_correspondencia_silver': 1637, 'secuencia_fuente_fuera_orden': 113, 'humedad_ausente_no_imputada': 100}.
- Conciliacion: Bronze 28920 = Silver 28448 + cuarentena 472.
- Silver tiene clave de lectura unica, UTC, Celsius canonico y cero errores bloqueantes.
- Las columnas originales coinciden fila a fila con Bronze.

## Archivos generados
- `notebooks/bronze_silver/04_iot_telemetry/B2S_04_AndinaLog_IoT_Telemetry.ipynb`
- `datos/silver/andinalog_iot_telemetry_silver.csv`
- `datos/quarantine/andinalog_iot_telemetry_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_04_IoT_Telemetry.md`

## Reproducibilidad
- Fecha de ejecucion UTC: 2026-09-24T18:45:40.652908+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- Rutas de entrada: `datos/bronze/andinalog_iot_telemetry.csv`, `datos/silver/andinalog_wms_orders_silver.csv`, `datos/silver/andinalog_productos_silver.csv`, `datos/silver/andinalog_flota_silver.csv`.
- Rutas de salida: `datos/silver/andinalog_iot_telemetry_silver.csv`, `datos/quarantine/andinalog_iot_telemetry_quarantine.csv`, `informes/bronze_silver/Informe_B2S_04_IoT_Telemetry.md`.
- Zona inicial: America/La_Paz; zona Silver: UTC.
- Conteos: Bronze 28920, Silver 28448, cuarentena 472.
- Semilla: None (no aplica; pipeline deterministico).
- Las entradas no se modifican; los controles finales se ejecutaron sobre CSV persistidos.
