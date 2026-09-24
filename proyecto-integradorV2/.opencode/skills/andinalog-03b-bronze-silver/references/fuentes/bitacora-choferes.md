# Perfil Bronze-Silver: Bitacora de Choferes TXT

- Declara codificacion, separador o expresion de parseo, lineas fisicas, registros logicos y lineas descartadas con causa.
- Conserva el numero de linea y, si aplica, posicion o bloque de origen.
- No uses un modelo generativo para clasificar cada fila. Usa diccionarios o reglas deterministas declaradas en `config`.
- No imputes conductor, viaje, camion ni timestamp cuando sean ambiguos.
- Interpreta timestamps sin zona como `America/La_Paz` y conviértelos a UTC.
- Minimiza texto libre y datos personales en Silver e informes; evita reproducir nombres, documentos, telefonos o correos.
- Si se usa para prediccion, conserva solo informacion disponible antes del instante objetivo y evita fuga temporal.
- Adapta la conciliacion entre lineas fisicas y registros logicos; documenta continuaciones, encabezados y lineas no parseables.
