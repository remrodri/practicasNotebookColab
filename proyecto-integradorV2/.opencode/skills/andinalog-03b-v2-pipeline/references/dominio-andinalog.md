# Dominio AndinaLog 03B

## Mandato

Proteger la cadena de frio, mejorar la rotacion del inventario y anticipar desviaciones termicas durante el transporte.

## Fuentes previstas

- WMS Orders
- Flota
- IoT Telemetry
- Warehouse Costs
- HR Drivers
- Productos
- Inventory Tracking
- Flota Eventos JSON
- Bitacora Choferes TXT

Inspecciona los archivos reales antes de fijar nombres de columnas o claves.

## Relaciones de negocio

- productos a inventario y telemetria mediante las claves y puentes observados;
- camiones a viajes y eventos;
- ordenes a viajes;
- centros a inventario, costos y flota.

Declara la granularidad de cada fuente y evita joins muchos a muchos no controlados.

## Temperatura

- Celsius es la unidad operacional canonica.
- Fahrenheit es reconocida y puede convertirse exactamente a Celsius con auditoria.
- Kelvin es una unidad fisica valida, pero no esperada en el dominio operacional adoptado; se envia a cuarentena salvo que un contrato de fuente posterior disponga otra cosa.
- `-999` y otros centinelas declarados representan ausencia o error, no mediciones.

## Tiempo

- Una fecha sin zona explicita se interpreta como hora de Bolivia.
- Localiza en `America/La_Paz` y convierte a UTC para Silver.
- En analisis predictivo, cada variable debe estar disponible antes o en el instante de prediccion.

## Categorias conocidas

- Centros aprobados en el alcance actual: Cochabamba, La Paz, Santa Cruz, Oruro y Tarija.
- Tipos de camion observados: Seco y Refrigerado.

No conviertas estas listas en contratos universales si el archivo o una especificacion oficial posterior demuestra categorias adicionales.

## Interpretacion responsable

- Una asociacion entre producto, camion, evento o desviacion no demuestra causalidad.
- No atribuyas responsabilidad automatica a conductores.
- Minimiza o seudonimiza informacion personal de HR Drivers.
- Separa hechos observados, inferencias y recomendaciones.

