# Perfil Bronze-Silver: HR Drivers

- Declara la granularidad por conductor y verifica unicidad de un identificador no personal.
- Minimiza datos personales: nombres, documentos, telefonos, correos y direcciones no deben aparecer en informes ni salidas analiticas visibles sin necesidad demostrada.
- No imputes identificadores ni datos personales.
- Conserva fechas calendario laborales sin desplazamiento de zona; convierte solo timestamps reales.
- Estados laborales, certificaciones y experiencia son atributos del dominio y no errores de calidad por su valor valido.
- No uses estos datos para sancionar conductores ni afirmes causalidad entre atributos laborales y eventos.
- Considera esta fuente contextual o excluida de Gold si el producto no demuestra una necesidad analitica y proporcional.
