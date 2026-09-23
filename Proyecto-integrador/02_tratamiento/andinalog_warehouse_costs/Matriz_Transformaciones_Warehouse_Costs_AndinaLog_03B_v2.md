# Matriz de transformaciones — Warehouse Costs v2

| Variable | Regla | Salida | Prueba |
|---|---|---|---|
| Centro | Validar catálogo de cinco centros | `centro_distribucion_tratado` | Cinco centros Silver |
| Periodo | Exigir `AAAA-MM` | `periodo_mes_tratado` | Un periodo válido |
| Rotación | Numérica y positiva; no imputar copia excluida | `rotacion_stock_dias_tratado` | Cinco valores completos Silver |
| Pérdida por merma | BOB no negativo | `perdida_mermas_bob_tratado` | Cinco valores válidos |
| Costo mensual | BOB no negativo | `costo_almacenamiento_mensual_bob_tratado` | Cinco valores válidos |
| Clave centro-periodo | Conservar primera completa | Decisión y motivo final | 5 Silver + 1 cuarentena = 6 |
