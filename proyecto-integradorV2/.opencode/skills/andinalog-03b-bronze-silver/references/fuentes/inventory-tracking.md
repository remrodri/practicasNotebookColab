# Perfil Bronze-Silver: Inventory Tracking

- Declara la granularidad por lote, producto, centro y movimiento o estado, según el archivo.
- Conserva fechas calendario sin conversion de zona horaria.
- Una `fecha_salida` vacia puede significar lote aun en almacen cuando la cantidad restante es positiva; no la marques automaticamente como error.
- Si la cantidad restante es cero y falta una salida requerida, trata la incoherencia como bloqueante.
- Recupera `fecha_vencimiento` desde WMS solo cuando el mismo `lote_id` tenga exactamente una fecha valida y consistente; registra la fuente y no la presentes como observada.
- Usa una fecha de corte fija y declarada para dias en almacen o dias para vencer; no uses la fecha actual de ejecucion.
- Un umbral de vencimiento, por ejemplo 30 dias, es bandera operativa configurable y no error de calidad por sí mismo.
- Evalua `cantidad_salida > cantidad_ingreso` como error bloqueante solo si ambas columnas representan acumulados comparables de la misma fila. Si son movimientos, valida acumulados por grupo y orden temporal.
- Para centros, valida directamente contra los cinco centros esperados. Usa WMS como control adicional, no como sustituto del catalogo.
