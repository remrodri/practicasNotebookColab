# Informe B2S 07 - AndinaLog Flota Eventos

## Objetivo, entidad y granularidad
Conversión auditada de eventos de telemetría desde un JSON padre-hijo hacia Silver.
- Entidad: evento de telemetría de camión.
- Granularidad padre: un objeto por camion_id con lista eventos.
- Granularidad hija: una fila aplanada por evento_id y posicion del arreglo.

## Perfil Bronze de esta ejecución
- Sistema: TELEMATICA-AndinaLog.
- Fecha de exportación: 2026-08-30T00:00:00.
- Objetos padre: 30.
- Eventos hijos: 192.
- Padres sin eventos: 0.
- Filas con evento_id duplicado: 16.
- Valores reconocido ausentes: 22.
- Lecturas inicialmente textuales: 10.

## Reglas y transformaciones
- Se aplana cada evento hijo y se conserva camion_id, posicion_evento y configuración padre.
- Los timestamps sin zona se interpretan en America/La_Paz y se convierten a UTC.
- Se aceptan ISO y DD/MM/YYYY HH:MM; las conversiones quedan auditadas.
- Se normalizan valor_lectura y booleanos solo desde representaciones observadas.
- Duplicados exactos se resuelven con una fila Silver y copias trazables en cuarentena.
- La ausencia de reconocido se conserva como AUSENTE y no se convierte en False.
- N/D en valor_lectura se conserva como no_aplica y no se convierte en cero ni en error.

## Integridad referencial
- Los camiones se comparan con flota Silver como referencia informativa; no se bloquea por falta de correspondencia.
- Los tipos y severidades se validan contra catálogos declarados.
- No se usan datos personales.

## Resultado y conciliación
- Silver: 184 filas.
- Cuarentena: 8 filas.
- Conciliación de granularidad: 30 padres y 192 eventos = 184 Silver + 8 cuarentena.
- Motivos de cuarentena: {'evento_id:duplicado_exacto_copia_resuelta': 8}.

## Archivos generados
- `notebooks/bronze_silver/07_flota_eventos/B2S_07_Flota_Eventos.ipynb`
- `datos/silver/andinalog_flota_eventos_silver.csv`
- `datos/quarantine/andinalog_flota_eventos_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_07_AndinaLog_Flota_Eventos.md`

## Reproducibilidad
- Fecha UTC: 2026-09-24T22:52:11.099270+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- Bronze JSON se lee sin modificar y se conserva el orden de los eventos.
- Ejecutar las celdas en orden; los controles se realizan sobre los CSV persistidos.
