# Matriz de transformaciones — WMS Orders v2

| Variable | Entrada | Regla o acción | Salida y bandera | Prueba |
|---|---|---|---|---|
| Claves | Texto Bronze | Quitar espacios y convertir a mayúsculas si no crea conflicto | `*_tratado`, acciones y motivos | Formatos canónicos y cobertura referencial |
| `fecha_despacho` | ISO o DD/MM/AAAA | Interpretar como hora de Bolivia; normalizar formato local | `fecha_despacho_bolivia_tratada`, `fecha_normalizada` | 20 normalizadas; 4 imposibles en cuarentena |
| `cantidad_solicitada` | Número o texto | Convertir `cincuenta` a 50; exigir entero positivo | `cantidad_solicitada_tratado` | 15 convertidas y marcadas; 13 mantienen otra contradicción |
| `cantidad_entregada` | Número o vacío | Validar rango; conservar vacío sin imputar desde OTIF | `cantidad_entregada_tratado`, `cantidad_entregada_ausente` | 80 ausentes marcadas |
| Tiempos | Horas | Prometido positivo y real no negativo | columnas tratadas | 15 tiempos reales negativos en cuarentena |
| OTIF | 0 o 1 | Validar dominio y coherencia de componentes | valores tratados, `apta_kpi_otif` | 7.388 filas aptas |
| Duplicados | Fila completa | Conservar primera y excluir copia posterior | `decision_tratamiento` | 50 copias excluidas |
| Población final | 7.550 filas | Particionar sin pérdida | Silver y cuarentena final | 7.468 + 82 = 7.550 |

