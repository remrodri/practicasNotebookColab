# Pipeline Bronze a Silver

## Estructura del notebook

1. Titulo, empresa, fuente, entidad y granularidad.
2. Objetivo y contrato de entrada.
3. Importaciones, semilla, rutas y `config`.
4. Lectura Bronze segun formato CSV, JSON o TXT.
5. Perfil inicial sin alterar el dato.
6. Funciones de estructuracion, normalizacion, conversion, imputacion, validacion y enrutamiento.
7. Ejecucion mediante `df.pipe()` sobre una copia.
8. Resumen de banderas, transformaciones e imputaciones.
9. Separacion Silver y cuarentena.
10. Conciliacion de filas y controles finales.
11. Exportacion de los dos CSV.
12. Reproducibilidad.

## Configuracion minima

El diccionario `config` debe contener solo reglas pertinentes a la fuente:

```python
config = {
    "archivo_entrada": "...",
    "prefijo_salida": "...",
    "timezone_local": "America/La_Paz",
    "timezone_silver": "UTC",
    "columnas_requeridas": [],
    "identificadores": {},
    "fechas": {},
    "numericas": {},
    "categorias": {},
    "rangos": {},
    "unidades": {},
    "centinelas": [],
    "imputaciones": {},
}
```

## Auditoria por campo

Cuando sea pertinente, conserva:

- `<campo>_original`
- `<campo>_tratado`
- `<campo>_error`
- `<campo>_motivo`
- `<campo>_fue_transformado`
- `<campo>_fue_imputado`
- `<campo>_metodo_imputacion`
- `<campo>_motivo_imputacion`

Agrega a nivel de fila:

- `fue_transformada`
- `fue_imputada`
- `cantidad_transformaciones`
- `cantidad_imputaciones`
- `calidad_estado`
- `calidad_motivo`

Evita columnas redundantes que repitan literalmente la misma informacion.

## Estado final

Calcula `calidad_estado` despues de todas las transformaciones e imputaciones.

- `VALIDO`: no quedan errores bloqueantes.
- Un codigo estable y descriptivo para cada error residual, por ejemplo `FECHA_INVALIDA`, `CLAVE_INVALIDA`, `UNIDAD_NO_ESPERADA` o `VALOR_FUERA_DE_RANGO`.

Una correccion inequivoca puede quedar en Silver con sus banderas de auditoria. Una duda no resuelta va a cuarentena.

## Fechas

Conserva el texto original. Si la fuente no declara zona horaria, interpreta la fecha en Bolivia y luego convierte a UTC:

```python
serie_local = serie_parseada.dt.tz_localize("America/La_Paz")
serie_utc = serie_local.dt.tz_convert("UTC")
```

Adapta el codigo si la serie ya contiene zona. No localices dos veces. Silver debe tener una columna UTC canonica; puede conservar una columna Bolivia para interpretacion del negocio.

## Controles obligatorios

- columnas requeridas presentes;
- conteo inicial y final;
- unicidad de claves cuando aplique;
- resumen de nulos, centinelas y errores de conversion;
- distribucion de `calidad_estado`;
- ausencia de errores bloqueantes en Silver;
- presencia del registro completo y sus motivos en cuarentena;
- conciliacion de filas o explicacion de cambios de granularidad.

