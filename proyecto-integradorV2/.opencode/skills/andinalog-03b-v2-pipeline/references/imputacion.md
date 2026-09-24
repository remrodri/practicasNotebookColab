# Imputacion auditable

El prompt S11 no define imputaciones. En V2, imputar es una decision de calidad que exige evidencia y trazabilidad.

## Condiciones para imputar

Permite una imputacion solo si es reproducible, inequivoca, compatible con el dominio, basada en informacion disponible, declarada en `config` y verificable con un control posterior.

## Prioridad de metodos

1. Correccion deterministica de representacion: numero escrito en palabras, error ortografico con una unica categoria valida o conversion exacta de unidad.
2. Recuperacion por clave desde un maestro valido con relacion unica.
3. Valor consistente de la misma entidad y periodo cuando existe una unica correspondencia demostrable.
4. Estadistica por grupo solo si el significado y el uso analitico lo permiten, el grupo se define sin fuga y se documenta la incertidumbre.

No uses media, mediana, moda, forward fill o backward fill como respuesta automatica. Justifica por campo y evita usar informacion futura en tareas predictivas.

## Casos que permanecen en cuarentena

- identificador desconocido o ambiguo;
- multiples candidatos posibles;
- fecha contractual o de vencimiento sin evidencia suficiente;
- valor operacional que solo puede estimarse inventando una regla;
- imputacion que requiere el objetivo futuro;
- campo sensible cuya utilizacion no es necesaria.

## Auditoria

Para cada imputacion conserva valor original, valor tratado, bandera, metodo y motivo. Agrega conteos por metodo al informe. Una fecha estimada nunca debe presentarse como confirmada.

## Entrenamiento y evaluacion

Si una imputacion estadistica aprende parametros, ajustalos solo con entrenamiento y aplicalos sin reajuste a validacion y prueba. Las correcciones deterministicas de formato pueden aplicarse antes del split si no usan distribuciones ni objetivos.

