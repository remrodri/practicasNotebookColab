# Contrato de auditoria

## Bronze a Silver

Revisa como minimo:

1. Bronze accesible y no sobrescrito.
2. Entidad, granularidad y claves documentadas.
3. `config` centralizado y funciones encadenadas con `df.pipe()`.
4. Sin `dropna()` ni filtros silenciosos.
5. Transformaciones e imputaciones reproducibles, sin futuro ni identificadores imputados.
6. `calidad_estado` calculado al final.
7. Silver con valores finales canonicos, cero errores bloqueantes y sin versiones tratadas identicas, originales innecesarios o helpers.
8. Cuarentena con valor recibido, origen, intento de tratamiento necesario y motivo suficiente.
9. Reporte de calidad con `regla_id` estable, denominador declarado y conteos recalculables.
10. Reglas evaluadas sin incidencias registradas con cero; no evaluadas diferenciadas de cero.
11. Activaciones solapadas no sumadas como registros unicos.
12. Error intrinseco diferenciado de falta referencial informativa.
13. Hora local de Bolivia convertida a UTC; fechas calendario sin desplazamiento.
14. Privacidad y minimizacion.
15. CSV: `Bronze = Silver + cuarentena`; el reporte no participa en esa suma.
16. JSON y TXT: conciliacion de su granularidad declarada.
17. Notebook ejecutado completamente y sin salidas contradictorias.
18. Conteos coincidentes entre notebook, Silver, cuarentena, reporte e informe.
19. Reproducibilidad con versiones, rutas, zonas, conteos y fecha.

## Silver a Gold

Revisa compuerta de fuentes, granularidad, claves, cardinalidades, joins, cobertura, agregaciones, coherencia matematica, privacidad, temporalidad predictiva, notebook ejecutado e informe consistente.

## Correcciones

En una segunda auditoria verifica primero los hallazgos previos y despues que la correccion no altero conciliacion, granularidad, fechas, privacidad ni resultados relacionados.

## Gold predictivo EDA y modelo

Revisa granularidad por lectura, ventanas dentro del viaje, objetivo en `(t, t+60]`, cobertura, ausencia de fuga, EDA requerido, split sin grupos compartidos, preprocesamiento ajustado solo con entrenamiento y metricas consistentes.
