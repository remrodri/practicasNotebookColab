# Perfil Bronze-Silver: Flota

- Granularidad esperada: un camion por identificador; confirma clave y unicidad.
- Centros esperados del caso: Cochabamba, La Paz, Santa Cruz, Oruro y Tarija.
- Tipos operativos conocidos: Seco y Refrigerado. Normaliza variantes inequívocas mediante mapa auditable.
- Valida capacidad como numero positivo y plausibilidad con el conjunto observado y documentacion disponible; no impongas un minimo arbitrario.
- Conserva una sola copia de duplicados exactos con trazabilidad; duplicados conflictivos quedan en cuarentena.
- No imputes identificadores, centro, tipo ni capacidad cuando exista ambigüedad.
- Las compatibilidades producto-camion se evalúan al integrar fuentes y no convierten por sí solas una fila maestra valida en error.
