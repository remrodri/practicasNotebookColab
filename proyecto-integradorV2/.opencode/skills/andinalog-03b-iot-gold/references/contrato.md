# Contrato de Gold predictivo IoT

Una fila representa una lectura. Conserva identificador de viaje u orden, timestamp UTC, temperatura actual, humedad actual y desviacion termica actual.

Deriva temperatura anterior, variacion de temperatura durante los ultimos 30 minutos, `desviacion_proximos_60min_flag` y `ventana_objetivo_evaluable`.

La etiqueta vale uno si existe al menos una desviacion en `(t, t+60 min]` dentro de la misma entidad. Vale cero solo cuando existe cobertura suficiente y no ocurre una desviacion. Sin cobertura completa, el objetivo queda nulo.

Define en `config` el metodo de variacion y la tolerancia de cobertura según la frecuencia observada. Prefiere busqueda temporal dentro de la entidad frente a desplazamiento fijo por filas.

Controla filas Silver frente a Gold, unicidad de lectura, orden temporal, ausencia de cruces entre entidades, distribución del objetivo y ausencia de variables futuras entre predictores.
