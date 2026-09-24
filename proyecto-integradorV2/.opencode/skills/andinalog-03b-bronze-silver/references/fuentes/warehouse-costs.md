# Perfil Bronze-Silver: Warehouse Costs

- Declara granularidad por centro y periodo, y verifica unicidad a ese nivel.
- Trata el periodo como periodo calendario; no lo desplaces por zona horaria.
- Valida centros contra Cochabamba, La Paz, Santa Cruz, Oruro y Tarija.
- Declara la moneda observada; usa BOB solo si el archivo o la documentacion la respaldan.
- Convierte costos y rotacion a numericos conservando originales y motivos de fallo.
- Recupera una rotacion ausente solo cuando exista una unica correspondencia inequívoca para la misma entidad y periodo. En particular, una segunda fila de Tarija puede heredar el valor de la fila equivalente solo si todos los atributos de identidad coinciden y no hay conflicto.
- No reemplaces costos o rotacion faltantes con cero, promedio o estadisticas globales.
- Duplicados conflictivos permanecen en cuarentena; duplicados exactos se resuelven con trazabilidad.
