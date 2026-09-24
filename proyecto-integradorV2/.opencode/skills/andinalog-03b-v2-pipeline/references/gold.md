# Productos Gold

Construye Gold solamente desde fuentes Silver conciliadas.

## Requisitos del notebook

- Usa pandas para lectura, joins y agregaciones.
- Declara tabla maestra, tabla transaccional, claves y granularidades.
- Comprueba unicidad de la clave de la maestra.
- Ejecuta `left` join con `validate="1:m"` cuando esa sea la cardinalidad real.
- Si la relacion real no es 1:m, no fuerces la validacion: agrega o corrige la unidad antes del join y documentalo.
- Registra filas coincidentes y no coincidentes sin ocultarlas.
- Conserva todas las entidades maestras.

## Metricas configurables

Define al inicio:

```python
metricas_agg = {
    "columna_numerica": ["mean", "max", "count"],
}
```

Si no se especifican metricas, propone el promedio de columnas numericas pertinentes y excluye claves, fechas, banderas y campos cuyo promedio carezca de significado.

Usa `groupby().agg(metricas_agg)`, aplana el MultiIndex con nombres descriptivos y documenta el tratamiento matematico de nulos, incluido `std` con una sola observacion.

## Salidas

- `<nombre>_detalle_gold.csv`
- `<nombre>_agregado_gold.csv`
- informe MD con contrato del join, metricas, conciliacion, no correspondencias y limitaciones.

## Controles

- filas de cada entrada;
- unicidad de la maestra;
- cardinalidad declarada y validada;
- filas antes y despues del join;
- entidades sin transacciones;
- claves transaccionales sin maestro, si corresponde;
- unicidad de la tabla agregada;
- nulos resultantes y decision aplicada;
- coherencia entre detalle y agregado.

