# Informe B2S 08 - AndinaLog HR Drivers

## Objetivo, entidad y granularidad
Conversión auditada de atributos laborales desde Bronze CSV hacia Silver y cuarentena.
- Entidad: conductor con un identificador operativo no personal.
- Granularidad: una fila por `chofer_id` después de resolver copias exactas.
- Clave funcional: `chofer_id`.

## Perfil Bronze de esta ejecución
- Filas Bronze: 156.
- Columnas Bronze: 6.
- Centros observados: Cochabamba, La Paz, Oruro, Santa Cruz, Tarija.
- Identificadores normalizados: 5.
- Filas involucradas en duplicados operativos: 10.
- Conflictos de clave: 0.

## Reglas, privacidad y transformaciones
- Bronze se lee como texto y no se modifica.
- `chofer_nombre` se elimina antes de generar Silver o cuarentena por minimización de PII.
- `chofer_id` se normaliza mediante recorte y mayúsculas; no se imputan identificadores.
- Los centros se validan contra el catálogo configurado.
- Horas, salario y ausentismo conservan original, valor tratado y banderas de conversión y centinela.
- Las copias exactas conservan la primera instancia en Silver y envían copias adicionales a cuarentena.

## Imputaciones
- No se realizaron imputaciones.
- No se usaron cero, medias, medianas, modas, `ffill`, `bfill` ni información futura.

## Evidencia de contradicción con el plan previo
- El plan indicó 157 filas; el archivo real contiene 156. La conciliación de esta ejecución prevalece.
- El plan atribuyó cinco casos a identificadores inválidos; la inspección encontró cinco grupos de copias operativas exactas.
- Se normalizó un identificador con espacios y minúsculas; no fue enviado a cuarentena por ese motivo.

## Integridad referencial y uso de auxiliares
- Los cinco grupos duplicados presentan campos operativos idénticos y no constituyen conflictos.
- Warehouse Costs 06 se considera contextual y no se utiliza: no aporta claves ni atributos necesarios para HR Drivers.
- No se usan variables laborales para sancionar conductores ni se afirma causalidad.

## Resultado y conciliación
- Silver: 151 filas.
- Cuarentena: 5 filas.
- Conciliación: Bronze 156 = Silver 151 + cuarentena 5.
- Motivos de cuarentena: {'chofer_id:duplicado_exacto_copia_resuelta': 5}.

## Limitaciones
- La fuente es contextual y no debe entrar a Gold sin necesidad analítica demostrada y proporcional.
- Los atributos laborales no sustituyen evidencia de cumplimiento, безопасidad o causalidad.

## Archivos generados
- `notebooks/bronze_silver/08_hr_drivers/B2S_08_HR_Drivers.ipynb`
- `datos/silver/andinalog_HR_Drivers_silver.csv`
- `datos/quarantine/andinalog_HR_Drivers_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_08_HR_Drivers.md`

## Reproducibilidad
- Fecha UTC: 2026-09-24T23:09:46.665863+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- Ejecutar las celdas en orden desde la raíz del proyecto.
- Los controles finales se aplican sobre los CSV persistidos.
