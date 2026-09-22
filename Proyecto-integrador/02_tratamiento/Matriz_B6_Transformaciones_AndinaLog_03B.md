# B6 — Matriz de transformaciones de AndinaLog 03B

**Responsable:** Grupo 06, rol Operaciones, Planificación y Datos.  
**Versión de esta matriz:** 1.0.  
**Fecha:** 2026-09-22.  
**Alcance:** las versiones didácticas de Notebook 2 en `proyecto-integrador/02_tratamiento/` para IoT, Productos, Flota e Inventory Tracking, más la comprobación relacional IoT–Productos–Flota.  
**Criterio:** el diagnóstico registra el problema sin cambiar Bronze; el tratamiento deja el original, escribe un campo tratado, marca la acción y conserva su motivo. Una imputación es una estimación identificada, no un valor observado.

La lámina B6 muestra ejemplos genéricos (`codigo_activo`, `fecha_parada`). Esos campos no pertenecen a los cuatro CSV tratados aquí; la matriz utiliza sus variables reales.

## IoT Telemetry

| Variable / entrada | Regla o decisión | Salida y bandera | Prueba documentada |
|---|---|---|---|
| `temperatura_cabina_c=-999` | Interpretar el centinela como faltante analítico; interpolar solo si existen dos vecinos válidos del mismo viaje, camión y producto, separados hasta 60 min y con variación hasta 2 °C. | Bronze intacto; `temperatura_cabina_c_tratada`, `temperatura_imputada`, `acciones_tratamiento` y `motivos_tratamiento`. Si no se recupera, `en_cuarentena_final=True`. | Verificar que `-999` nunca sea una temperatura tratada; 120 temperaturas imputadas entre tratadas; ninguna apta para KPI observado. |
| `temp_unit=F` | Convertir `(F−32)×5/9`. | `temperatura_cabina_c_tratada` en °C, `temp_unit_tratado=C`, acción `CONVERTIR_F_A_C`. | 50 conversiones; todas las filas tratadas tienen unidad canónica `C`. |
| `temp_unit=K` u otra no operativa | No convertir automáticamente. | `motivo_cuarentena_final` y `decision_tratamiento=CUARENTENA`. | Ninguna fila Kelvin entra al tratado; partición total entre tratado y cuarentena. |
| `timestamp` sin zona | Interpretar como hora `America/La_Paz` y derivar UTC. | `timestamp_utc`; Bronze `timestamp` intacto. | Comprobar que las filas tratadas tienen UTC no vacío y que diagnóstico declara zona de origen `America/La_Paz`. |
| `camion_id` recuperable con espacios/minúsculas | Normalizar a `CAM-##`; no inventar un ID distinto. | `camion_id_tratado`, acción/motivo de normalización. | 50 IDs normalizados; todos los IDs tratados cumplen el patrón. |
| Humedad faltante o fuera de 0–100 % | Interpolar solo entre vecinos válidos con cambio máximo de 20 puntos; si no hay evidencia suficiente, cuarentena. | `humedad_cabina_pct_tratada`, `humedad_imputada`, acción/motivo. | 92 humedades imputadas entre tratadas; ninguna tratada queda sin humedad utilizable. |
| Lectura repetida o clave en conflicto | Excluir copia posterior; poner en cuarentena variantes contradictorias. | `motivo_cuarentena_final`, `decision_tratamiento`. | `fila_bronze` única; 28.920 diagnosticadas = 28.677 tratadas + 243 en cuarentena final. |
| Lectura térmica tratada | Exigir temperatura **observada**, umbral **observado** del Productos Silver didáctico actual y bandera de desvío coherente. | `umbral_producto_evaluable`, `flag_termico_coherente`, `apta_kpi_termico`. | 26.183 aptas; ninguna temperatura imputada apta; EDA verifica concordancia fila por fila. |
| Producto `Fresco`/`Congelado` observado en camión registrado `Seco` | Marcar para revisión operativa, sin cambiar categoría/tipo ni enviar automáticamente a cuarentena. | `posible_incompatibilidad_termica=True`, `compatibilidad_tipo_camion_estado=REVISAR`, motivo; `NO_EVALUABLE` si faltan datos confiables. | 407 lecturas de 17 viajes marcadas; el EDA contrasta la marca con Productos y Flota Silver. |

## Productos

| Variable / entrada | Regla o decisión | Salida y bandera | Prueba documentada |
|---|---|---|---|
| `producto_id` con espacios/minúsculas | Quitar espacios exteriores y pasar a mayúsculas si cumple `PROD-###`. | `producto_id_tratado`, acción/motivo. | 6 IDs normalizados; 60 claves únicas en Silver. |
| Categoría `conjelado` no permitida | Inferir categoría solo si objetivo térmico, tolerancia y vida útil observada coinciden con **un único** patrón. No sustituir por `Congelado` por parecido ortográfico. | `categoria_logistica_tratada`, `categoria_imputada=True`, método/motivo. | Tres categorías inferidas: `PROD-026→Fresco`, `PROD-028→Seco`, `PROD-036→Fresco`, respaldadas por lotes observados. |
| Temperatura objetivo vacía | Inferir solo con categoría, tolerancia y vida útil observada concordantes. | `temperatura_conservacion_requerida_c_tratada`, `temperatura_imputada=True`, método/motivo. | Dos temperaturas inferidas (`PROD-018`, `PROD-049`); ninguna se etiqueta como umbral completamente observado. |
| Copia o ID preparado con atributos contradictorios | Excluir copia posterior; cuarentena de variantes en conflicto. | `en_cuarentena_final`, motivo. | 63 filas = 60 Silver + 3 copias en cuarentena; ID Silver único. |
| Umbral para KPI térmico | Requiere categoría y objetivo/tolerancia observados, sin inferencia. | `apto_umbral_termico_observado`. | 55 productos observados y 5 con algún atributo inferido; los cinco tienen marca `False`. |

## Flota

| Variable / entrada | Regla o decisión | Salida y bandera | Prueba documentada |
|---|---|---|---|
| `camion_id` con espacios/minúsculas | Normalizar si cumple `CAM-##` y no hay conflicto. | `camion_id_tratado`, `camion_id_normalizado`, acción/motivo. | 2 IDs normalizados; 30 claves únicas en Silver. |
| Centro o tipo fuera del catálogo del caso | Aceptar solo cinco centros confirmados y `Seco`/`Refrigerado`; valores desconocidos a cuarentena. | Campos `*_tratado`, `motivo_cuarentena_final`. | Todas las filas Silver tienen centro y tipo permitidos. |
| `capacidad_kg` faltante, inválida o no positiva | No imputar una capacidad de otro camión. | `capacidad_kg_tratada` o cuarentena final; `<750 kg` positivo se marca para revisar ficha. | Todas las capacidades Silver son positivas; `capacidad_revisar_ficha` identifica las pequeñas. |
| Copia posterior o atributos contradictorios para mismo ID | Excluir copia; cuarentena de variantes contradictorias. | `en_cuarentena_final`, motivo. | 32 filas = 30 Silver + 2 copias en cuarentena. |

## Inventory Tracking

| Variable / entrada | Regla o decisión | Salida y bandera | Prueba documentada |
|---|---|---|---|
| Fecha válida `DD/MM/AAAA` | Parsear como día/mes/año y escribir `AAAA-MM-DD`; fecha imposible a cuarentena. | `fecha_*_tratada`, acción `NORMALIZAR_FECHA_...` y motivo. | 25 fechas normalizadas; ninguna fecha imposible entra en Silver. |
| `producto_id` con espacios/minúsculas | Preparar en mayúsculas. | `producto_id_tratado`, acción `NORMALIZAR_PRODUCTO_ID`. | 30 IDs normalizados; clave disponible para unir con Productos Silver. |
| `fecha_vencimiento` vacía | Estimar ingreso + vida útil observada del producto solo con ≥20 lotes válidos y una única duración. | `fecha_vencimiento_tratada`, `vencimiento_imputado=True`, `vida_util_producto_dias_usada`, acción/motivo. | 18 vencimientos imputados; los 18 quedan fuera de `apto_kpi_vencimiento_observado`. |
| `fecha_salida` vacía | Conservar como lote aún en almacén; no inventar salida. | `fecha_salida_tratada` vacía y evaluación contextual de lote abierto. | Contar lotes sin salida; la salida Silver actual tiene 0. |
| `cantidad_ingreso="cien"` o merma negativa | No convertir texto ambiguo ni invertir signo. | Cuarentena final y motivo. | 10 ingresos no numéricos y 5 mermas negativas en cuarentena final. |
| Cantidades válidas | Calcular `ingreso−salida−merma`; saldo negativo a cuarentena. | `saldo_unidades_inventario`, decisión final. | Todos los saldos Silver no son negativos; no se exige saldo cero. |
| Salida posterior a vencimiento | Conservar el hecho si el resto es válido y marcar riesgo; indicar si vencimiento fue imputado. | `riesgo_salida_post_vencimiento`, `riesgo_basado_en_vencimiento_imputado`. | 468 filas Silver con salida posterior al vencimiento; ninguna usa vencimiento imputado. |
| Copia o conflicto de movimiento/lote | Excluir copias; cuarentena de claves con atributos distintos. | `en_cuarentena_final`, motivo. | 6.040 diagnosticadas = 5.980 Silver + 60 en cuarentena; 40 copias excluidas. |

## Cómo usar la matriz

1. Leer la columna **Entrada** junto al dato Bronze, sin modificarlo.
2. Comprobar en Notebook 2 la **regla** y las marcas de la salida correspondiente.
3. Ejecutar la **prueba** indicada y registrar cualquier cifra que cambie al regenerar los CSV. Los conteos de esta matriz corresponden a las salidas didácticas actuales, no son constantes de negocio.
4. Para un dato imputado, citar fuente, condiciones y motivo; nunca presentarlo como medición o fecha confirmada.

Esta matriz es documentación de decisiones. Los notebooks contienen la implementación y sus comprobaciones; no hace falta un catálogo ejecutable adicional para esta versión didáctica.
