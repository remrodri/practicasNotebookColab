# Informe B2S 03 - AndinaLog WMS Orders

## Objetivo, entidad y granularidad
Conversión auditada de órdenes WMS desde Bronze a Silver y cuarentena.
- Entidad: orden_wms.
- Granularidad: una fila por order_id normalizado.
- No existe `viaje_id` en la fuente y no se construye una relación sintética.

## Contrato y perfil Bronze
- Columnas obligatorias: ['order_id', 'cliente_id', 'producto_id', 'fecha_despacho', 'centro_distribucion', 'camion_id', 'chofer_id', 'cantidad_solicitada', 'cantidad_entregada', 'tiempo_entrega_prometido_hrs', 'tiempo_entrega_real_hrs', 'otif_on_time', 'otif_in_full', 'otif'].
- Filas: 7550; columnas: 14.
- Tipos recibidos: {'order_id': 'str', 'cliente_id': 'str', 'producto_id': 'str', 'fecha_despacho': 'str', 'centro_distribucion': 'str', 'camion_id': 'str', 'chofer_id': 'str', 'cantidad_solicitada': 'str', 'cantidad_entregada': 'str', 'tiempo_entrega_prometido_hrs': 'str', 'tiempo_entrega_real_hrs': 'str', 'otif_on_time': 'str', 'otif_in_full': 'str', 'otif': 'str'}.
- Valores vacíos: {'order_id': 0, 'cliente_id': 0, 'producto_id': 0, 'fecha_despacho': 0, 'centro_distribucion': 0, 'camion_id': 0, 'chofer_id': 0, 'cantidad_solicitada': 0, 'cantidad_entregada': 80, 'tiempo_entrega_prometido_hrs': 0, 'tiempo_entrega_real_hrs': 0, 'otif_on_time': 0, 'otif_in_full': 0, 'otif': 0}.
- Duplicados exactos: 100 filas; duplicados de clave: 100 filas en 50 claves.
- Espacios en identificadores: {'order_id': 50, 'cliente_id': 20, 'producto_id': 20, 'camion_id': 0, 'chofer_id': 0}.
- Formatos de fecha: {'iso': 7530, 'dmy': 20, 'no_reconocido': 0}.
- Textos no convertibles antes del tratamiento: {'cantidad_solicitada': 15, 'cantidad_entregada': 0, 'tiempo_entrega_prometido_hrs': 0, 'tiempo_entrega_real_hrs': 0, 'otif_on_time': 0, 'otif_in_full': 0, 'otif': 0}.
- Centros observados: {'Tarija': 1586, 'Santa Cruz': 1523, 'Oruro': 1502, 'La Paz': 1494, 'Cochabamba': 1445}.

## Transformaciones, fechas e imputación
- Identificadores se recortan y normalizan a mayúsculas con auditoría.
- `cincuenta` se normaliza inequívocamente a 50 en 15 filas y conserva el original y la bandera.
- Fechas ISO y DD/MM/YYYY se interpretan en America/La_Paz y se convierten a UTC; las fechas imposibles permanecen en cuarentena.
- Fechas inválidas: 4.
- No se imputan identificadores, cantidades, tiempos, fechas ni indicadores; no hay información suficiente para hacerlo inequívocamente.

## OTIF y coherencia
- `otif_on_time` debe concordar con tiempo real <= prometido; `otif_in_full` con cantidad entregada >= solicitada; `otif` con el producto de ambos indicadores.
- Cantidades y tiempos inválidos o incoherentes permanecen en cuarentena.

## Integridad referencial
- Filas sin producto en Productos Silver: 792.
- Filas sin camión en Flota Silver: 346.
- No se inventan correspondencias; cada ausencia se registra y es bloqueante.

## Contradicciones respecto del plan
- la fuente tiene 7550 filas y 14 columnas, no 7551 y 15.
- order_id usa cinco dígitos secuenciales, no tres.
- no existe viaje_id; no se construye una relación de viaje sintética.

## Resultado y conciliación
- Silver: 6261 filas; estados: {'valida_con_transformacion': 6261}.
- Cuarentena: 1289 filas; motivos por regla: {'producto_id_sin_correspondencia_silver': 792, 'camion_id_sin_correspondencia_silver': 346, 'order_id_duplicado': 100, 'requerido_ausente:cantidad_entregada': 80, 'tiempo_real_negativo': 15, 'cantidad_entregada_mayor_solicitada': 13, 'fecha_despacho_invalida': 4, 'otif_on_time_incoherente': 4, 'otif_in_full_incoherente': 2}.
- Conciliación persistida: Bronze 7550 = Silver 6261 + cuarentena 1289.
- Silver tiene clave única, referencias válidas y cero errores bloqueantes.
- Silver y cuarentena son disjuntos y su unión cubre todas las filas Bronze.

## Archivos generados
- `notebooks/bronze_silver/03_wms_orders/B2S_03_AndinaLog_WMS_Orders.ipynb`
- `datos/silver/andinalog_wms_orders_silver.csv`
- `datos/quarantine/andinalog_wms_orders_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_03_WMS_Orders.md`

## Reproducibilidad
- Fecha de ejecución UTC: 2026-09-25T02:49:22.169156+00:00.
- Python: 3.13.15.
- pandas: 3.0.5.
- Rutas de entrada: `datos/bronze/andinalog_wms_orders.csv`, `datos/silver/andinalog_productos_silver.csv`, `datos/silver/andinalog_flota_silver.csv`.
- Rutas de salida: `datos/silver/andinalog_wms_orders_silver.csv`, `datos/quarantine/andinalog_wms_orders_quarantine.csv`, `informes/bronze_silver/Informe_B2S_03_WMS_Orders.md`.
- Zona inicial: America/La_Paz; zona Silver: UTC.
- Conteos: Bronze 7550, Silver 6261, cuarentena 1289.
- Semilla: None (no aplica; el pipeline es determinístico).
- Las entradas no se modifican; los controles finales se ejecutan sobre los CSV persistidos.
