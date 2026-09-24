# Perfil Bronze-Silver: IoT Telemetry

- Granularidad esperada: una lectura por entidad y timestamp; confirma identificadores y posibles duplicados.
- Interpreta timestamps sin zona como `America/La_Paz` y conviértelos a UTC en Silver.
- Celsius es canonico. Fahrenheit es reconocido y convertible con auditoria. Kelvin no es esperado operacionalmente y permanece en cuarentena.
- `-999` y otros centinelas declarados no son mediciones; conviértelos en ausencia analitica con bandera y motivo.
- Una excursion termica plausible es un evento operativo, no un error de calidad. Conserva la lectura y genera una bandera de negocio separada.
- No uses datos futuros para imputar series. No apliques media, mediana, `ffill` o `bfill` automaticamente.
- Valida referencias a camion y viaje cuando existan. La falta de WMS para enriquecer una lectura valida es informativa salvo que el contrato exija esa referencia para interpretar la fila.
