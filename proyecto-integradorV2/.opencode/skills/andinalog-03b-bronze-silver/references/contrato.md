# Contrato Bronze a Silver

## Dominio

- Empresa AndinaLog, Grupo 06, subcaso 03B.
- Mandato: cadena de frio, rotacion de inventario y alerta termica.
- Celsius es canonica; Fahrenheit se convierte exactamente; Kelvin no es esperado operacionalmente.
- Centinelas como `-999` no son mediciones.
- Fechas sin zona se interpretan en Bolivia y se convierten a UTC.
- Centros conocidos: Cochabamba, La Paz, Santa Cruz, Oruro y Tarija.
- Tipos de camion observados: Seco y Refrigerado.

Valida estas reglas contra la fuente y cualquier contrato oficial posterior.

## Imputacion

Imputa solo si la regla es reproducible, inequivoca, compatible con el dominio, utiliza informacion disponible y esta declarada en `config`.

Prioriza:

1. correccion deterministica de representacion;
2. recuperacion por clave unica desde un maestro valido;
3. valor consistente de la misma entidad y periodo con correspondencia unica;
4. estadistica por grupo solamente si tiene sentido y no genera fuga.

No uses media, mediana, moda, `ffill` o `bfill` automaticamente. Si una imputacion aprende parametros, ajustalos solo con entrenamiento cuando el dato se use en modelado.

Una fecha estimada no se presenta como confirmada. Un identificador ambiguo no se imputa.

## Informe MD

Incluye objetivo, granularidad, perfil Bronze, reglas, transformaciones, imputaciones, enrutamiento, conteos, conciliacion, limitaciones, archivos generados y decisiones defendibles. Obtiene todas las cifras de la ejecucion entregada.

