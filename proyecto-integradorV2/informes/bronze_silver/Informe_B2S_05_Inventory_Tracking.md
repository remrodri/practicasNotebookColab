# Informe B2S 05 - Andinalog Inventory Tracking

## Objetivo, entidad y granularidad
Conversión auditada de movimientos de inventario desde Bronze hacia Silver y cuarentena.
- Entidad: movimiento de inventario por lote, producto, centro y movimiento.
- Granularidad: una fila por movimiento_id, lote_id, producto_id y centro_distribucion.

## Perfil Bronze de esta ejecución
- Filas Bronze: 6040.
- Columnas: ['movimiento_id', 'lote_id', 'producto_id', 'centro_distribucion', 'fecha_ingreso', 'fecha_salida', 'fecha_vencimiento', 'cantidad_ingreso', 'cantidad_salida', 'cantidad_merma', 'dias_en_almacen', 'costo_unitario_bob'].
- Valores vacíos: {'movimiento_id': 0, 'lote_id': 0, 'producto_id': 0, 'centro_distribucion': 0, 'fecha_ingreso': 0, 'fecha_salida': 0, 'fecha_vencimiento': 18, 'cantidad_ingreso': 0, 'cantidad_salida': 0, 'cantidad_merma': 0, 'dias_en_almacen': 0, 'costo_unitario_bob': 0}.
- Filas con movimiento_id duplicado: 80.
- Filas con lote_id duplicado: 80.
- Centros observados: ['Cochabamba', 'La Paz', 'Oruro', 'Santa Cruz', 'Tarija'].
- Productos observados: 83.

## Reglas y transformaciones
- Las fechas calendario se conservan sin desplazamiento de zona horaria.
- Se acepta ISO y se corrige de forma determinista DD/MM/YYYY cuando la fecha es válida.
- Los centros se validan directamente contra el catálogo configurado.
- Los valores originales se conservan antes de convertir texto, fechas y números.
- Los duplicados exactos se resuelven conservando una fila y enviando la copia con trazabilidad.
- Los duplicados conflictivos se envían íntegramente a cuarentena.

## Integridad referencial y enriquecimiento
- Silver WMS no contiene lote_id; por lo tanto no se puede recuperar fecha_vencimiento desde esa fuente.
- Los vencimientos observados se conservan como bronze_observada; los vacíos se registran como no_disponible_wms.
- La correspondencia con productos Silver es informativa y no bloquea la fila.
- La bandera vence_dentro_30_dias usa la fecha de corte fija declarada y no es error de calidad.

## Resultado y conciliación
- Silver: 5980 filas.
- Cuarentena: 60 filas.
- Conciliación: Bronze 6040 = Silver 5980 + cuarentena 60.
- Fecha de corte: 2026-08-31.

## Contradicciones documentadas del plan
- El plan aprobado estimaba 537 registros; la inspección real encontró 6040 registros.
- El plan Approved preveía salidas vacías ycantidad_salida mayor que cantidad_ingreso; no se observaron en la fuente actual.
- WMS Silver no expone lote_id, por lo que no se realiza la recuperación de vencimiento prevista.

## Archivos generados
- `notebooks/bronze_silver/05_inventory_tracking/B2S_05_Inventory_Tracking.ipynb`
- `datos/silver/andinalog_inventory_tracking_silver.csv`
- `datos/quarantine/andinalog_inventory_tracking_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_05_Andinalog_Inventory_Tracking.md`

## Reproducibilidad
- Fecha UTC: 2026-09-24T22:26:35.289849+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- Bronze se lee como texto y no se modifica.
- Ejecutar las celdas en orden; los controles se realizan sobre los CSV persistidos.
