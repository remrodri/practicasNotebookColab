# Contrato de auditoria

## Bronze a Silver

Revisa como minimo:

1. Fuente Bronze accesible y no sobrescrita.
2. Entidad, granularidad y claves documentadas.
3. `config` centralizado con reglas realmente utilizadas.
4. Funciones encadenadas mediante `df.pipe()`.
5. Valores originales conservados antes de conversiones coercitivas.
6. Ausencia de `dropna()` u otro filtro que elimine errores sin registrarlos.
7. Transformaciones deterministicas auditadas.
8. Imputaciones reproducibles, inequivocas, sin identificadores ni informacion futura.
9. Estimaciones diferenciadas de valores confirmados.
10. `calidad_estado` calculado despues del tratamiento y la imputacion.
11. Silver sin errores bloqueantes.
12. Cuarentena con registro y motivo suficientes.
13. Error intrinseco diferenciado de fallo referencial informativo.
14. Timestamps con hora localizados en Bolivia y convertidos a UTC.
15. Fechas calendario, vencimientos y periodos sin desplazamiento horario.
16. Privacidad y minimizacion cuando existan datos personales.
17. CSV: conciliacion Bronze = Silver + cuarentena.
18. JSON: conciliacion de padres, hijos, objetos sin hijos y filas aplanadas.
19. TXT: conciliacion de lineas fisicas, registros logicos, Silver y cuarentena.
20. Notebook ejecutado completamente, sin errores ocultos ni salidas contradictorias.
21. Conteos y decisiones coincidentes entre notebook, CSV e informe.
22. Reproducibilidad con versiones, rutas, zonas, conteos y fecha de ejecucion.

Comprobaciones por formato:

- JSON: estructura real, vinculo padre-hijo, claves tecnicas documentadas y duplicados sin perdida silenciosa.
- TXT: codificacion, patron reproducible, numero de linea, registros no parseables y ausencia de clasificacion generativa fila por fila.
- HR o bitacora: identificadores directos minimizados y no expuestos en informes o salidas visibles.

## Silver a Gold

Revisa como minimo:

1. Cada fuente necesaria tiene pipeline aprobado y conciliado.
2. Fuentes utilizadas, contextuales y excluidas documentadas.
3. Objetivo, unidad analitica y granularidad declarados.
4. Claves y cardinalidades comprobadas antes de unir.
5. Unicidad de la maestra verificada.
6. `left join` y `validate="1:m"` usados cuando corresponda.
7. Agregacion previa cuando evita un muchos a muchos.
8. Filas antes y despues de cada join.
9. Cobertura y no correspondencias registradas.
10. Nulos posteriores al join tratados con significado, no rellenados automaticamente.
11. `metricas_agg` declarado y limitado a metricas interpretables.
12. MultiIndex aplanado con nombres descriptivos.
13. Agregado unico en su clave.
14. Coherencia matematica entre detalle y agregado.
15. Para prediccion, variables disponibles antes o en el instante de corte.
16. Eventos y bitacoras posteriores excluidos.
17. Datos personales y variables laborales innecesarias excluidos.
18. Ausencia de afirmaciones causales no sustentadas.
19. Notebook ejecutado y entregables consistentes.
20. Informe y reproducibilidad completos.

## Revision posterior a correcciones

En una segunda auditoria, verifica primero cada hallazgo previo y su control de cierre. Despues revisa que la correccion no haya alterado conciliacion, granularidad, fechas, privacidad o resultados relacionados. No reabras decisiones aprobadas sin evidencia nueva.

