# Contrato Silver a Gold

## Relaciones del dominio

- productos a inventario y telemetria mediante claves y puentes observados;
- camiones a viajes y eventos;
- ordenes a viajes;
- centros a inventario, costos y flota.

Declara la granularidad antes de cada union. Si dos tablas contienen multiples filas por clave, agrega una de ellas antes de unir para evitar multiplicacion artificial.

## Metricas configurables

Usa una configuracion como:

```python
metricas_agg = {
    "temperatura_c": ["mean", "max", "count"],
}
```

Elige solamente metricas interpretables para el producto. Documenta el caso de desviacion estandar nula o faltante con una sola observacion.

## Controles

- filas de cada entrada;
- unicidad de la maestra;
- cardinalidad esperada y observada;
- filas del join;
- entidades maestras sin transacciones;
- claves transaccionales sin maestro;
- unicidad del agregado;
- nulos resultantes;
- conciliacion entre detalle y agregado.

## Informe MD

Incluye objetivo, fuentes, granularidades, contrato de joins, metricas, resultados, no correspondencias, controles, limitaciones, rutas y decisiones defendibles. Obtiene las cifras de la ejecucion entregada.

