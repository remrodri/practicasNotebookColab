# Contrato de ingesta — WMS Orders — AndinaLog 03B v2

Fecha: 2026-09-22. Responsable: Grupo 06.

| Elemento | Acuerdo |
|---|---|
| Fuente | `andinalog_wms_orders.csv` |
| Granularidad | Una orden despachada |
| Formato | CSV UTF-8, 14 columnas Bronze |
| Tiempo | `fecha_despacho` sin zona explícita se interpreta como hora de Bolivia |
| Claves | `order_id`, `cliente_id`, `producto_id`, `camion_id`, `chofer_id` |
| Catálogos | Cinco centros; Productos y Flota Silver v2; chofer por identificador Bronze |
| Cantidades | Solicitada positiva; entregada no negativa y no superior a solicitada |
| Tiempos | Prometido positivo; real no negativo |
| OTIF | `otif_on_time`, `otif_in_full` y `otif` deben ser binarios; OTIF coincide con la conjunción de sus componentes |
| Diagnóstico | Conserva Bronze y añade `_en_cuarentena` y `_motivo` por campo; no modifica datos |
| Tratamiento | Normaliza claves y fechas recuperables; convierte únicamente el texto inequívoco `cincuenta` a 50 con bandera de auditoría y no imputa cantidad entregada desde OTIF |
| Salidas | Diagnosticado, cuarentena y reporte; Silver, cuarentena final y reporte |

Las variables de entrega real y OTIF ocurren después del despacho. No deben utilizarse como predictoras del modelo térmico previo al resultado.

