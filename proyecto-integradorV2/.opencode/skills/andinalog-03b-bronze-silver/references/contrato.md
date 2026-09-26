# Contrato Bronze a Silver

## Dominio

- Empresa AndinaLog, Grupo 06, subcaso 03B.
- Mandato: cadena de frio, rotacion de inventario y alerta termica.
- Celsius es canonica; Fahrenheit se convierte exactamente; Kelvin no es esperado operacionalmente.
- Centinelas como `-999` no son mediciones.
- Timestamps con hora sin zona se interpretan en Bolivia y se convierten a UTC.
- Fechas calendario, vencimientos y periodos se conservan sin desplazamiento horario.
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

No uses media, mediana, moda, `ffill` o `bfill` automaticamente. No uses informacion futura. Si una imputacion aprende parametros, ajustalos solo con entrenamiento cuando el dato se use en modelado.

Una fecha estimada no se presenta como confirmada. Los identificadores no se imputan.

## Integridad referencial

Clasifica cada fallo como error intrinseco, error referencial bloqueante o falta informativa para enriquecimiento. Define el criterio en `config`. Una fila valida no se rechaza solo porque una fuente auxiliar tenga su clave en cuarentena o no disponible.

## Privacidad

Minimiza identificadores directos de HR Drivers y Bitacora. Si existe un identificador operativo valido, no conserves nombres u otros identificadores personales innecesarios en Silver. No muestres datos personales en el informe. No uses variables laborales para sancionar ni para afirmar causalidad.

## JSON y TXT

Para JSON registra objetos padre, elementos hijos, objetos sin hijos y filas aplanadas. Para TXT registra codificacion, lineas fisicas, registros logicos, lineas no parseables y numero de origen. No uses un modelo generativo para clasificar cada registro de texto; usa reglas deterministicas o categorias no clasificables.

## Informe MD

Incluye objetivo, granularidad, perfil Bronze, reglas, transformaciones, imputaciones, enrutamiento, cobertura referencial, conteos, conciliacion, resumen del reporte de calidad, criterio de seleccion de columnas, limitaciones, archivos generados y decisiones defendibles. No suma activaciones solapadas como filas unicas. Obtiene todas las cifras de la ejecucion entregada.
