# Perfil Bronze-Silver: WMS Orders

- Declara la granularidad real: orden, viaje o linea de orden, según las columnas presentes.
- Valida unicidad de la clave al nivel declarado y secuencia coherente de fechas.
- No imputes identificadores de orden, viaje, producto, lote o camion.
- Convierte palabras numericas inequívocas, por ejemplo `cincuenta` a `50`, mediante diccionario cerrado, conservando original, bandera, metodo y motivo.
- Valida cantidades como numericas y no negativas según su semantica; evita asumir unidades no documentadas.
- Comprueba referencias con Productos y Flota cuando estén disponibles. Distingue error bloqueante de falta informativa para enriquecimiento.
- Calcula indicadores logísticos, como OTIF, solo si sus campos y definiciones están presentes y documentados.
