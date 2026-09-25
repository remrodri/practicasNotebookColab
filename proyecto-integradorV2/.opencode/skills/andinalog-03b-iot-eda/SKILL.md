---
name: andinalog-03b-iot-eda
description: Genera o revisa el notebook ejecutado y el informe del EDA obligatorio de la tabla Gold predictiva IoT de AndinaLog 03B, con controles estructurales y graficos Seaborn definidos por el docente. Usar despues de construir y auditar Gold.
---

# AndinaLog 03B EDA de Gold IoT

Analiza Gold sin redefinir sus variables ni modificar la entrada. Usa [references/contrato.md](references/contrato.md) como lista minima.

## Entregables

1. Notebook EDA `.ipynb` ejecutado con tablas y graficos visibles.
2. Informe `.md` consistente con los resultados actuales.

## Flujo

1. Lee Gold y declara que una fila representa una lectura.
2. Muestra filas, columnas, duplicados, faltantes, tipos y estadisticas descriptivas.
3. Verifica unicidad y que Gold no haya multiplicado registros.
4. Separa faltantes esperados por rezagos o ventanas no evaluables de errores inesperados.
5. Analiza balance del objetivo sobre ventanas evaluables.
6. Produce todos los graficos obligatorios con etiquetas, unidades y tamaños legibles.
7. Interpreta patrones descriptivos sin afirmar causalidad ni anticipar rendimiento.
8. Registra limitaciones, poblacion analizada y reproducibilidad.

## Reglas

- No reconstruyas la etiqueta ni cambies Gold dentro del EDA.
- No ocultes clases, nulos ni extremos sin explicar el filtro.
- Cada afirmacion del informe debe corresponder a una salida ejecutada.
