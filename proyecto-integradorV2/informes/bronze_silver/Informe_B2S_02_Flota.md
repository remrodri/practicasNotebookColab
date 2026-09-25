# Informe B2S 02 - AndinaLog Flota

## Objetivo, entidad y granularidad
Conversión auditada de la fuente Bronze de flota a Silver y cuarentena.
- Entidad: camion.
- Granularidad: una fila por camion_id normalizado.
- Clave funcional: `camion_id` normalizado.

## Contrato de entrada
- Columnas obligatorias: ['camion_id', 'centro_distribucion_base', 'capacidad_kg', 'tipo_camion'].
- Lectura Bronze: {'encoding': 'utf-8', 'dtype': 'str', 'keep_default_na': False}.
- Centros válidos: ['Cochabamba', 'La Paz', 'Santa Cruz', 'Oruro', 'Tarija'].
- Tipos de camión válidos: ['Seco', 'Refrigerado'].

## Perfil Bronze de esta ejecución
- Filas: 32.
- Columnas: ['camion_id', 'centro_distribucion_base', 'capacidad_kg', 'tipo_camion'].
- Tipos recibidos: {'camion_id': 'str', 'centro_distribucion_base': 'str', 'capacidad_kg': 'str', 'tipo_camion': 'str'}.
- Valores vacíos: {'camion_id': 0, 'centro_distribucion_base': 0, 'capacidad_kg': 0, 'tipo_camion': 0}.
- Claves duplicadas normalizadas: ['CAM-01', 'CAM-27'] (4 filas).
- Centros observados: {'Cochabamba': 14, 'La Paz': 6, 'Santa Cruz': 5, 'Oruro': 4, 'Tarija': 3}.
- Tipos observados: {'Refrigerado': 16, 'Seco': 16}.
- Capacidades observadas: [2000, 5000, 8000, 12000] kg; rango observado 2000 a 12000 kg.

## Reglas y decisiones
- Formato de identificador aplicado: `^CAM-\d{2}$`; evidencia: todos los identificadores observados usan dos dígitos; el patrón de tres dígitos del plan contradice la fuente.
- Se normalizan espacios y mayúsculas de identificadores; las correcciones inequívocas pueden llegar a Silver con auditoría.
- Centro y tipo se validan contra los catálogos aprobados.
- No se fija capacidad mínima operacional: no existe evidencia ni regla de dominio para inventar una capacidad mínima operacional. Solo se exige capacidad numérica positiva por significado físico.
- Imputación de capacidad deshabilitada: no hay ausencias y no existe una regla inequívoca aprobada.
- No hay fechas en la fuente; la regla America/La_Paz a UTC no aplica.

## Contradicciones detectadas respecto del plan
- La fuente contiene dos claves duplicadas, `CAM-01` y `CAM-27`; se aplica la política aprobada a las cuatro ocurrencias.
- La fuente usa identificadores de dos dígitos; se detuvo la regla incompatible de tres dígitos y se validó el patrón observado, sin inventar otra codificación.

## Enrutamiento y controles
- Política de duplicados: cuarentena_de_todas_las_ocurrencias (no elegir arbitrariamente una ocurrencia de una clave funcional duplicada).
- Silver: 28 filas; estados: {'valida': 26, 'valida_con_transformacion': 2}.
- Filas imputadas: 0.
- Cuarentena: 4 filas; motivos: {'camion_id_duplicado': 4}.
- Conciliación persistida: Bronze 32 = Silver 28 + cuarentena 4.
- Silver tiene clave única y no contiene errores bloqueantes.

## Limitaciones
- La fuente no contiene una regla de precedencia para resolver duplicados.
- No existe evidencia para establecer una capacidad mínima operacional distinta de la validación física de positividad.

## Archivos generados
- `notebooks/bronze_silver/02_flota/B2S_02_AndinaLog_Flota.ipynb`
- `datos/silver/andinalog_flota_silver.csv`
- `datos/quarantine/andinalog_flota_quarantine.csv`
- `informes/bronze_silver/Informe_B2S_02_Flota.md`

## Reproducibilidad
- Fecha de ejecución UTC: 2026-09-25T02:48:38.278350+00:00.
- Python: 3.13.15.
- pandas: 3.0.5.
- Ruta Bronze relativa: `datos/bronze/andinalog_flota.csv`.
- Ruta Silver relativa: `datos/silver/andinalog_flota_silver.csv`.
- Ruta cuarentena relativa: `datos/quarantine/andinalog_flota_quarantine.csv`.
- Zona de fechas sin zona: America/La_Paz; destino Silver: UTC; no aplica por ausencia de fechas.
- Conteos: Bronze 32, Silver 28, cuarentena 4.
- Bronze se lee con `dtype=str` y no se modifica; los controles finales se ejecutan sobre los CSV persistidos.
