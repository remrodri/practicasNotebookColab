# Perfil Bronze-Silver: Flota Eventos JSON

- Declara granularidad del objeto padre y de cada evento hijo antes de aplanar.
- Reporta objetos padre, eventos hijos, padres sin eventos y registros resultantes.
- Conserva trazabilidad del objeto, posicion del arreglo y clave padre; crea identificadores tecnicos solo si son necesarios y deterministas.
- Diferencia valor `N/D`, ausencia y cero. No conviertas ausencia o no aplicabilidad en cero.
- Normaliza booleanos y categorias solo desde conjuntos reconocidos.
- Interpreta timestamps sin zona como `America/La_Paz` y conviértelos a UTC; conserva fechas calendario sin desplazamiento.
- Audita duplicados al nivel de evento y referencias a la flota Silver.
- Adapta la conciliacion al cambio de granularidad: no exijas igualdad simple entre objetos JSON y filas aplanadas.
