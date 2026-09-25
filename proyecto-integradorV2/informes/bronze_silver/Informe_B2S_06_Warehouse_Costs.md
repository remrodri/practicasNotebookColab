# Informe B2S 06 - AndinaLog Warehouse Costs

## Objetivo, entidad y granularidad
Conversión auditada de costos de almacén desde Bronze hacia Silver y cuarentena.
- Entidad: costos de almacenaje por centro de distribución.
- Granularidad: una fila por centro_distribucion y periodo_mes.
- Clave funcional: `centro_distribucion` + `periodo_mes`.

## Perfil Bronze de esta ejecución
- Filas Bronze: 6.
- Columnas: ['centro_distribucion', 'rotacion_stock_dias', 'perdida_mermas_bob', 'periodo_mes', 'costo_almacenamiento_mensual_bob'].
- Valores vacíos: {'centro_distribucion': 0, 'rotacion_stock_dias': 1, 'perdida_mermas_bob': 0, 'periodo_mes': 0, 'costo_almacenamiento_mensual_bob': 0}.
- Centros observados: ['Cochabamba', 'La Paz', 'Oruro', 'Santa Cruz', 'Tarija'].
- Periodos observados: ['2026-08'].
- Filas con clave duplicada: 2.

## Reglas y transformaciones
- El periodo es calendario y se conserva sin desplazamiento de zona horaria.
- Los centros se validan contra el catálogo configurado.
- La moneda observada es BOB por los sufijos de columna.
- Las columnas numéricas conservan original, valor tratado y banderas de conversión/centinela.
- La clave se valida por centro y periodo; los duplicados conflictivos se bloquean.

## Imputación y errores
- No se imputa rotación ausente porque Tarija+2026-08 tiene dos filas con estados incompatibles y no existe una correspondencia única inequívoca.
- Ambas filas Tarija+2026-08 permanecen en cuarentena; no se usa cero, promedio, estadística global ni información futura.

## Resultado y conciliación
- Silver: 4 filas.
- Cuarentena: 2 filas.
- Conciliación: Bronze 6 = Silver 4 + cuarentena 2.
- El plan previo de 5+1 no se mantiene: el perfil exige cuarentena de ambos registros con duplicado conflictivo.

## Archivos generados
- `notebooks/bronze_silver/06_warehouse_costs/B2S_06_Andinalog_Warehouse_Costs.ipynb`
- `datos/silver/andinalog_warehouse_costs_silver.csv`
- `datos/quarantine/andinalog_warehouse_costs_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_06_Warehouse_Costs.md`

## Reproducibilidad
- Fecha UTC: 2026-09-25T02:51:13.875031+00:00.
- Python: 3.13.15.
- pandas: 3.0.5.
- Bronze se lee como texto sin modificar.
- Ejecutar las celdas en orden; los controles se realizan sobre los CSV persistidos.
