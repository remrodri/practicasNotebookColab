# Perfil Bronze-Silver IoT Telemetry

- Granularidad: una lectura por entidad y timestamp; confirma clave y duplicados.
- Interpreta timestamps sin zona como `America/La_Paz` y conviertelos a UTC.
- Celsius es canonico. Fahrenheit es convertible con auditoria. Kelvin no es esperado operacionalmente y permanece en cuarentena.
- `-999` y otros centinelas declarados no son mediciones.
- Una excursion termica plausible es evento operativo, no error de calidad.
- No uses informacion futura ni apliques media, mediana, `ffill` o `bfill` automaticamente.
- La falta de WMS para enriquecer una lectura valida es informativa salvo contradiccion con una referencia existente.
- En Silver, `timestamp`, `temperatura_cabina_c` y `temp_unit` contienen los valores finales UTC, Celsius y `C`. No exportes otra columna `_tratado` identica.
- Conserva originales de timestamp, temperatura, unidad o identificador solo cuando prueban una transformacion; para el resto basta `_fila_bronze` y el motivo agregado.
- Lleva al reporte las reglas de unidad, centinela, ausencia, humedad, timestamp, duplicidad, secuencia e integridad referencial, incluso si no dejan bandera propia en Silver.
- La cuarentena conserva valores recibidos e intentos de normalizacion necesarios. Identifica causas con `regla_id` dentro de `errores_bloqueantes` y `calidad_motivo`.
