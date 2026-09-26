# Esquemas de salida Bronze-Silver

## Regla general

Las columnas internas del dataframe de trabajo no determinan los CSV. Declara en `config` tres proyecciones explicitas: `columnas_silver`, `columnas_cuarentena` y `columnas_reporte_calidad`. No se fija un numero universal de columnas; cada una debe tener una funcion documentada.

## Silver compacto

Silver contiene:

1. columnas de negocio con valores finales canonicos;
2. clave de trazabilidad hacia Bronze;
3. originales solo de campos realmente transformados o imputados cuando la clave Bronze no baste;
4. motivos y conteos resumidos de transformacion e imputacion;
5. banderas informativas necesarias para consumir o unir el dato;
6. `calidad_estado` y `calidad_motivo`.

No exporta versiones `_tratado` identicas a la columna final, copias `_original` de campos que nunca cambian, helpers de calculo ni banderas bloqueantes que son siempre falsas en Silver.

## Cuarentena investigable

Cuarentena contiene:

1. valores recibidos de Bronze o columnas `_original` inequívocas;
2. clave o posicion de origen;
3. valores tratados necesarios para decidir si la fila puede recuperarse;
4. `errores_bloqueantes`, `banderas_informativas`, conteos y motivos;
5. estado, motivo principal y controles referenciales relevantes.

Prefiere identificadores de regla dentro de `errores_bloqueantes` antes que una columna booleana por error. Conserva una bandera individual solo si habilita una accion posterior o evita ambiguedad.

## Reporte de calidad

`<prefijo>_reporte_calidad.csv` tiene una fila por regla y estas columnas minimas:

- `dataset`, `etapa`, `regla_id`, `columna_evaluada`
- `dimension_calidad`, `descripcion_regla`, `tipo_resultado`, `severidad`
- `filas_evaluadas`, `filas_afectadas`, `porcentaje_afectado`
- `accion_aplicada`, `filas_silver`, `filas_cuarentena`
- `estado_regla`, `evidencia`

`regla_id` es estable. `porcentaje_afectado` usa `filas_afectadas / filas_evaluadas` salvo denominador distinto documentado. Registra cero cuando una regla fue evaluada sin incidencias y diferencia ese caso de una regla no evaluada.

Una fila puede activar varias reglas. La suma de `filas_afectadas`, `filas_silver` o `filas_cuarentena` entre reglas no representa registros unicos.

## Conciliacion

- CSV: `filas_bronze = filas_silver + filas_cuarentena`, con claves de origen disjuntas y exhaustivas.
- JSON o TXT: usa la conciliacion de granularidad declarada en su perfil.
- El reporte de calidad no participa en la conciliacion de filas; se valida regla por regla contra calculos independientes.

## Controles posteriores a exportar

1. Releer los tres CSV.
2. Verificar lista y orden de columnas.
3. Confirmar Silver sin errores bloqueantes.
4. Confirmar cuarentena sin filas carentes de motivo.
5. Confirmar trazabilidad exhaustiva y sin solape.
6. Recalcular conteos por regla y compararlos con reporte, notebook e informe.
7. Detectar columnas duplicadas o constantes sin funcion documentada.
8. Confirmar valores finales canonicos en las columnas principales.
