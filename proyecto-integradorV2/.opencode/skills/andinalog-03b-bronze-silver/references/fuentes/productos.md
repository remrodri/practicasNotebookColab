# Perfil Bronze-Silver: Productos

- Granularidad esperada: un producto por `producto_id`; confirma la clave real y su unicidad.
- Trata categoria logistica, temperatura requerida, tolerancia y unidad como atributos maestros.
- Normaliza espacios, mayusculas y errores ortograficos solo mediante mapas deterministas declarados en `config`.
- No inventes categorias, unidades, temperaturas ni tolerancias ausentes.
- Celsius es canonico; Fahrenheit puede convertirse con valor original y auditoria; Kelvin no es esperado y queda como error residual.
- Valida coherencia de limites termicos y categorias con evidencia del archivo y del dominio.
- No imputes identificadores. Los duplicados conflictivos permanecen en cuarentena.
