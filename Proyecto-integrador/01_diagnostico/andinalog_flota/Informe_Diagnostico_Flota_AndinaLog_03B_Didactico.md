# Informe del Notebook 1: diagnóstico didáctico de Flota — AndinaLog 03B

## Objetivo

El notebook `S4_01_AndinaLog_Flota_Diagnostico_Didactico.ipynb` diagnostica la calidad del maestro Bronze `andinalog_flota.csv` del grupo 06, subcaso 03B. El objetivo es identificar camiones cuya información pueda afectar los cruces con viajes, eventos y telemetría, o las comparaciones por tipo de camión y centro de distribución.

El diagnóstico **detecta, clasifica y explica**; no corrige, imputa ni elimina datos. Conserva las cuatro columnas originales y agrega un estado y un motivo por cada una. Las reglas son visibles dentro del notebook, sin catálogo ni motor externo.

## Entrada y salidas

| Elemento | Ruta relativa a `practicasNotebookColab` | Contenido |
|---|---|---|
| Bronze | `datasets/AndinaLog_03B_Bronce/andinalog_flota.csv` | Fuente original: 32 filas y cuatro columnas. |
| Notebook | `proyecto-integrador/01_diagnostico/andinalog_flota/S4_01_AndinaLog_Flota_Diagnostico_Didactico.ipynb` | Reglas y comprobaciones. |
| Diagnosticado | `proyecto-integrador/01_diagnostico/andinalog_flota/salidas/andinalog_flota_didactico_v1_diagnosticado.csv` | Las 32 filas originales, con resultados de calidad. |
| Cuarentena | `proyecto-integrador/01_diagnostico/andinalog_flota/salidas/andinalog_flota_didactico_v1_cuarentena.csv` | Subconjunto de filas con al menos un problema crítico. |

La cuarentena ya está incluida en el diagnosticado. **No se deben concatenar** los dos archivos al iniciar el tratamiento.

## Diccionario de datos y reglas de negocio

| Campo Bronze | Significado | Regla aplicada | Severidad |
|---|---|---|---|
| `camion_id` | Identificador del camión para cruces con viajes, eventos y telemetría. | Obligatorio y con patrón exacto `CAM-##`: letras mayúsculas, guion y dos dígitos. | `CRITICO` si falta o tiene formato inválido. |
| `centro_distribucion_base` | Centro base del camión. | Obligatorio; valores permitidos: `Cochabamba`, `La Paz`, `Santa Cruz`, `Oruro`, `Tarija`. | `CRITICO` si falta o está fuera de la lista confirmada. |
| `capacidad_kg` | Capacidad de carga útil declarada, en kilogramos. | Obligatoria, numérica y mayor que 0. Una cifra positiva inferior a 750 kg se señala para contrastarla con la ficha técnica del vehículo. | `CRITICO` si falta, no es numérica o no es positiva; `REVISAR` si es menor que 750 kg. |
| `tipo_camion` | Tipo operativo del vehículo. | Obligatorio; valores admitidos en este ejercicio: `Seco` y `Refrigerado`. | `CRITICO` si falta o no pertenece a la lista. |

La lista de cinco centros fue confirmada para este caso. La lista de tipos se trata como cerrada para el ejercicio porque son los dos tipos observados y propuestos para AndinaLog; debe actualizarse si la operación incorpora otro tipo. El umbral de **750 kg es orientativo**, no un mínimo legal ni una capacidad mínima universal. Existen configuraciones refrigeradas publicadas con 759 kg de carga útil y otras con capacidades mucho mayores según el modelo y la carrocería. Por ello una cifra inferior a 750 kg provoca revisión, no rechazo automático. Fuentes: [Mercedes-Benz, Sprinter refrigerado](https://conversion-world.mercedes-benz.com/en/GLOBAL/partner-produkt/3976/sprinter-coolkit-l3-h2-panel-van) y [FUSO, capacidades por configuración](https://www.fuso-trucks.com/product/canter/7-5-tonnes/).

## Unicidad y coherencia del identificador

`camion_id` funciona como clave del maestro de Flota. El notebook distingue tres situaciones:

1. **Copia exacta posterior:** los cuatro valores de la fila coinciden con una fila anterior. Se marca `CRITICO` en `camion_id` de la copia para evitar contar dos veces el mismo camión. El original se mantiene en el diagnosticado.
2. **Mismo ID con datos contradictorios:** un `camion_id` repetido presenta otros valores diferentes. Se marcan `CRITICO` todas las variantes de ese ID; el diagnóstico no elige cuál es correcta.
3. **Colisión potencial al normalizar:** dos escrituras distintas coincidirían al quitar espacios y pasar a mayúsculas. Se marca `REVISAR` para investigar; el diagnóstico no fusiona registros.

Las comprobaciones de unicidad no reemplazan la revisión referencial con viajes, eventos u otras tablas. Ese cruce puede realizarse después usando los datos tratados.

## Estructura del diagnosticado

Las cuatro columnas Bronze permanecen intactas. Se añaden las siguientes columnas:

| Grupo | Columnas | Uso |
|---|---|---|
| Trazabilidad | `fila_bronze`, `version_diagnostico`, `sha256_bronze` | Ubicar la fila original y la versión exacta del archivo diagnosticado. |
| Estado y motivo por variable | `camion_id_estado`, `camion_id_motivo`, `centro_distribucion_base_estado`, `centro_distribucion_base_motivo`, `capacidad_kg_estado`, `capacidad_kg_motivo`, `tipo_camion_estado`, `tipo_camion_motivo` | Mostrar qué campo presentó un problema y por qué. Un campo puede acumular varios motivos. |
| Resumen por fila | `cantidad_columnas_con_problemas`, `en_cuarentena`, `severidad_maxima`, `columnas_con_problemas`, `motivos_fila` | Facilitar filtros y decisiones del tratamiento posterior. |

Los estados posibles son `OK`, `REVISAR` y `CRITICO`. La severidad máxima de la fila se obtiene de sus cuatro estados; `en_cuarentena=True` si alguno es `CRITICO`. Una observación `REVISAR` no basta por sí sola para enviar la fila a cuarentena.

## Resultados de la ejecución

| Indicador | Resultado |
|---|---:|
| Filas Bronze | 32 |
| Filas diagnosticadas | 32 |
| Filas con al menos un problema | 4 |
| Filas en cuarentena diagnóstica | 4 |
| Filas sin problemas detectados | 28 |
| IDs con letras minúsculas | 2 |
| Copias exactas posteriores | 2 |

Los cuatro hallazgos se concentran en `camion_id`:

| `fila_bronze` | `camion_id` | Motivo |
|---:|---|---|
| 20 | `cam-20` | Formato distinto de `CAM-##`. |
| 30 | `cam-30` | Formato distinto de `CAM-##`. |
| 31 | `CAM-01` | Copia exacta posterior de un camión ya registrado. |
| 32 | `CAM-27` | Copia exacta posterior de un camión ya registrado. |

No se detectaron faltantes, centros fuera de la lista, tipos fuera de la lista ni capacidades no numéricas, no positivas o inferiores a 750 kg en este archivo. Esto describe **el CSV examinado** y no garantiza que futuras cargas tengan la misma calidad.

## Relación con el tratamiento

El Notebook 2 de Flota deberá leer el **diagnosticado completo**, no sumar el CSV de cuarentena. Podrá convertir `cam-20` y `cam-30` a mayúsculas si comprueba que no generan colisiones; podrá excluir las copias posteriores de `CAM-01` y `CAM-27` del Silver, manteniendo evidencia de la decisión. Si aparece un conflicto real de atributos bajo el mismo ID, deberá permanecer en cuarentena hasta su resolución. El diagnóstico no autoriza imputar capacidad, centro o tipo sin una fuente verificable.

## Validaciones y reproducción

El notebook verifica el esquema de entrada, que los cuatro campos Bronze no se modificaron, la unicidad de `fila_bronze`, la correspondencia entre `en_cuarentena` y el CSV de cuarentena, la existencia de motivos para toda fila crítica y el hash SHA-256 del archivo original. Puede ejecutarse desde la raíz del repositorio o en Colab configurando la ruta de Drive. Genera únicamente los dos CSV de salida descritos.
