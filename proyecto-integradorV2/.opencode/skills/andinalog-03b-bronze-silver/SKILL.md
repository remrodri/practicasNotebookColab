---
name: andinalog-03b-bronze-silver
description: Genera o revisa un notebook ejecutado y un informe MD para convertir una fuente Bronze CSV, JSON o TXT de AndinaLog 03B en Silver y cuarentena, siguiendo el prompt S11 con config, funciones, df.pipe, auditoria e imputacion justificada. Usar cuando el usuario indique una fuente Bronze concreta.
---

# AndinaLog 03B Bronze a Silver

Procesa una fuente por invocacion. Inspecciona el archivo real antes de definir reglas. El prompt S11 del docente controla la arquitectura y [references/contrato.md](references/contrato.md) añade el contrato de imputacion y dominio.

## Entradas

Necesitas la ruta de la fuente Bronze. Usa la carpeta de salida indicada por el usuario o, si existe un `AGENTS.md` del proyecto, sus convenciones. Acepta CSV, JSON y TXT.

## Entregables obligatorios

1. Notebook `.ipynb` listo para Colab y ejecutado de principio a fin.
2. Informe `.md` basado en la ejecucion actual.
3. `<prefijo>_silver.csv`.
4. `<prefijo>_quarantine.csv`.

## Flujo

1. Describe entidad, granularidad y contrato de entrada.
2. Centraliza rutas, columnas, zonas, formatos, catalogos, rangos, unidades, centinelas e imputaciones en `config`.
3. Lee Bronze con el metodo apropiado y conserva los valores originales.
4. Perfila estructura, tipos, nulos, duplicados y categorias sin alterar Bronze.
5. Implementa funciones de estructuracion, normalizacion, conversion, imputacion, validacion y estado final.
6. Ejecuta las funciones con `df.pipe()` sobre una copia de trabajo.
7. Calcula `calidad_estado` despues de tratamiento e imputacion.
8. Envia a Silver las filas sin errores residuales y a cuarentena los registros no resueltos.
9. Concilia filas y exporta los dos CSV.
10. Incluye reproducibilidad y redacta el informe.

## Reglas estrictas

- No uses `dropna()` para descartar errores.
- Antes de `errors="coerce"`, conserva el valor original y genera bandera y motivo.
- Una correccion inequivoca puede llegar a Silver con auditoria.
- Una imputacion ambigua permanece en cuarentena.
- Para JSON aplanado, documenta el cambio de granularidad.
- Interpreta fechas sin zona en `America/La_Paz` y conviertelas a UTC para Silver.
- Comprueba que Silver no contenga errores bloqueantes.
- No copies reglas o cifras de V1; derivalas del archivo, el prompt y el dominio oficial.

## Auditoria minima

Conserva, cuando corresponda, valor original, valor tratado, bandera, motivo, indicador de transformacion, indicador de imputacion, metodo de imputacion y motivo de imputacion. A nivel de fila incluye `fue_transformada`, `fue_imputada`, conteos, `calidad_estado` y `calidad_motivo`.

