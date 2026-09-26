---
name: andinalog-03b-bronze-silver
description: Genera o revisa el pipeline Bronze-Silver de una fuente CSV, JSON o TXT de AndinaLog 03B, con notebook ejecutado, Silver compacto, cuarentena investigable, reporte de calidad e informe MD. Usar cuando el usuario indique una fuente Bronze concreta.
---

# AndinaLog 03B Bronze a Silver

Procesa una fuente por invocacion. Inspecciona el archivo real antes de definir reglas. El prompt S11 controla la arquitectura; [references/contrato.md](references/contrato.md) define dominio e imputacion y [references/esquemas-salida.md](references/esquemas-salida.md) define las tres salidas tabulares.

## Perfil de la fuente

Lee el perfil correspondiente en `references/fuentes/` antes de Plan o Build:

- `andinalog_productos.csv` -> `productos.md`
- `andinalog_flota.csv` -> `flota.md`
- `andinalog_wms_orders.csv` -> `wms-orders.md`
- `andinalog_iot_telemetry.csv` -> `iot-telemetry.md`
- `andinalog_inventory_tracking.csv` -> `inventory-tracking.md`
- `andinalog_warehouse_costs.csv` -> `warehouse-costs.md`
- `andinalog_flota_eventos.json` -> `flota-eventos.md`
- `andinalog_hr_drivers.csv` -> `hr-drivers.md`
- `andinalog_bitacora_choferes.txt` -> `bitacora-choferes.md`

El perfil orienta el dominio; siempre se contrasta con el archivo real y la documentacion oficial.

## Entregables obligatorios

1. Notebook `.ipynb` ejecutado de principio a fin.
2. `<prefijo>_silver.csv` compacto y listo para consumo.
3. `<prefijo>_quarantine.csv` con evidencia suficiente para investigar.
4. `<prefijo>_reporte_calidad.csv` con una fila por regla.
5. Informe `.md` basado en esa ejecucion.

## Flujo

1. Declara entidad, granularidad, claves y contrato de entrada.
2. Centraliza rutas, reglas y listas `columnas_silver`, `columnas_cuarentena` y `columnas_reporte_calidad` en `config`.
3. Lee Bronze sin modificarlo y conserva una clave de trazabilidad.
4. Perfila esquema, tipos, nulos, duplicados y categorias.
5. Implementa estructuracion, normalizacion, conversion, imputacion, validacion y estado final mediante funciones encadenadas con `df.pipe()`.
6. Calcula `calidad_estado` despues del tratamiento y la imputacion.
7. Enruta filas sin errores residuales a Silver y errores no resueltos a cuarentena.
8. Construye el reporte agregado desde los resultados reales de cada regla.
9. Proyecta esquemas distintos para las tres salidas; no exportes automaticamente todas las columnas internas.
10. Persiste, relee y valida los tres CSV.
11. Concilia Bronze con Silver y cuarentena y redacta el informe.

## Reglas estrictas

- No uses `dropna()` para descartar errores.
- Antes de una conversion coercitiva conserva el valor recibido o una referencia inequívoca a Bronze.
- Una correccion deterministica puede llegar a Silver con auditoria; una imputacion ambigua permanece en cuarentena.
- Interpreta timestamps sin zona en `America/La_Paz` y conviertelos a UTC; no desplaces fechas calendario, vencimientos ni periodos.
- Silver contiene valores finales canonicos y cero errores bloqueantes.
- No conserves a la vez una columna final, otra `_tratado` identica y una `_original` que nunca cambia.
- En Silver conserva originales solo si prueban una transformacion o imputacion real.
- Cuarentena conserva valor recibido, intento de tratamiento necesario y motivos completos; no requiere una bandera por regla cuando `errores_bloqueantes` identifica la causa sin ambiguedad.
- El reporte de calidad registra todas las reglas evaluadas, incluso las de cero incidencias.
- Los conteos por regla pueden solaparse; no se suman como registros unicos.
- Distingue error intrinseco, fallo referencial bloqueante y falta informativa de enriquecimiento.
- No envies a cuarentena una fila valida solo porque una fuente auxiliar no permita enriquecerla.
- Minimiza datos personales y no los expongas en informes.

## Formatos semiestructurados

- JSON: declara granularidad padre e hija, aplanamiento y conciliacion de objetos.
- TXT: declara codificacion, patron, lineas fisicas, registros logicos y numero de origen. No clasifiques fila por fila con un modelo generativo.

## Auditoria minima

Para toda transformacion o imputacion real conserva valor recibido o clave Bronze, valor final, bandera, metodo y motivo. A nivel de fila conserva `_fila_bronze` o equivalente, `fue_transformada`, `fue_imputada`, conteos, `calidad_estado` y `calidad_motivo`. El reporte de calidad conserva el detalle agregado de las reglas que no necesitan columnas propias.
