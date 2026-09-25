# Informe B2S 01 - AndinaLog Productos

## Objetivo, entidad y granularidad
Conversión auditada de productos logísticos desde Bronze a Silver y cuarentena.
- Entidad: producto_logistico.
- Granularidad: una fila por producto_id normalizado.
- Clave funcional: `producto_id` normalizado.

## Contrato de entrada
- Columnas obligatorias: ['producto_id', 'nombre_producto', 'categoria_logistica', 'temperatura_conservacion_requerida_c', 'tolerancia_temperatura_c', 'precio_unitario_bob', 'costo_unitario_bob'].
- Lectura Bronze: {'encoding': 'utf-8', 'dtype': 'str', 'keep_default_na': False}; tipos tratados: texto para identificador/nombre/categoria y numerico para temperatura, tolerancia, precio y costo.
- El esquema exige exactamente las columnas configuradas; columnas extra permitidas: False.

## Perfil Bronze de esta ejecución
- Filas Bronze: 63.
- Columnas: ['producto_id', 'nombre_producto', 'categoria_logistica', 'temperatura_conservacion_requerida_c', 'tolerancia_temperatura_c', 'precio_unitario_bob', 'costo_unitario_bob'].
- Tipos recibidos: {'producto_id': 'str', 'nombre_producto': 'str', 'categoria_logistica': 'str', 'temperatura_conservacion_requerida_c': 'str', 'tolerancia_temperatura_c': 'str', 'precio_unitario_bob': 'str', 'costo_unitario_bob': 'str'}.
- Valores vacíos: {'producto_id': 0, 'nombre_producto': 0, 'categoria_logistica': 0, 'temperatura_conservacion_requerida_c': 2, 'tolerancia_temperatura_c': 0, 'precio_unitario_bob': 0, 'costo_unitario_bob': 0}.
- Filas con clave duplicada normalizada: 6.
- Categorías observadas: {'Seco': 32, 'Fresco': 18, 'Congelado': 10, 'conjelado': 3}.

## Reglas, transformaciones e imputación
- Celsius es la unidad canónica; no hay columnas de fecha ni unidades Fahrenheit/Kelvin en esta fuente.
- Se recortan espacios y se normaliza el identificador a mayúsculas.
- La representación `conjelado` se corrige determinísticamente a `Congelado` y conserva auditoría.
- Cada conversión numérica conserva original, tratado, bandera de conversión inválida y bandera de centinela.
- La temperatura vacía se imputa exclusivamente con el método `catalogo_deterministico_categoria` declarado en `CONFIG`; conserva original, tratado, bandera, método y motivo tanto por campo como a nivel de fila, sin estadísticas ni información futura.
- Se valida la temperatura y la tolerancia contra el catálogo de la categoría, además de rangos monetarios y `costo <= precio`.

## Enrutamiento y controles
- Política de duplicados: cuarentena_de_todas_las_ocurrencias (no elegir arbitrariamente una ocurrencia de una clave funcional duplicada).
- Silver: 54 filas; estados: {'valida': 47, 'valida_con_transformacion': 5, 'valida_con_imputacion': 2}.
- Filas con imputación: 2.
- Cuarentena: 9 filas; motivos: {'producto_id_duplicado': 6, 'temperatura_categoria_incompatible': 2, 'temperatura_categoria_incompatible | tolerancia_categoria_incompatible': 1}.
- Conciliación persistida: Bronze 63 = Silver 54 + cuarentena 9.
- Silver no contiene errores bloqueantes y su clave es única.
- Las filas persistidas de Silver y cuarentena no se solapan y su unión cubre todas las filas Bronze.

## Limitaciones y decisiones defendibles
- El catálogo categoría-temperatura y categoría-tolerancia se deriva de correspondencia consistente en filas con categorias canonicas; alias conflictivos se conservan en cuarentena y se declara explícitamente en `CONFIG`; requiere confirmación si aparece un contrato maestro posterior.
- No se elige una ocurrencia de claves duplicadas, porque la fuente no aporta una regla de precedencia reproducible.
- Las incompatibilidades entre categoría normalizada y temperatura se conservan en cuarentena para corrección operativa.

## Archivos generados
- `notebooks/bronze_silver/01_productos/B2S_01_AndinaLog_Productos.ipynb`
- `datos/silver/andinalog_productos_silver.csv`
- `datos/quarantine/andinalog_productos_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_01_Productos.md`

## Reproducibilidad
- Fecha de ejecución UTC: 2026-09-25T02:47:41.039691+00:00.
- Python: 3.13.15.
- pandas: 3.0.5.
- Bronze se lee con `dtype=str` y no se modifica.
- La raíz se detecta mediante `ANDINALOG_ROOT` o buscando el directorio `datos/bronze`; la fuente se resuelve desde `CONFIG['rutas']['bronze']`.
- Zona de fechas sin zona: America/La_Paz; destino Silver: UTC; no aplica por ausencia de fechas.
- Conteos: Bronze 63, Silver 54, cuarentena 9.
- Ejecutar las celdas en orden; los controles finales se realizan sobre los CSV ya persistidos.
