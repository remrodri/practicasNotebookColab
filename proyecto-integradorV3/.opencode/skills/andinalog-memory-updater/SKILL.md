---
name: andinalog-memory-updater
description: Actualiza la memoria compacta de AndinaLog 03B al cerrar una sesión, dataset, notebook, auditoría o decisión.
---

# Actualización de memoria

Lee `MEMORY.md` y el fragmento específico antes de escribir.

## Qué conservar

- Resultado comprobado.
- Decisión vigente y motivo.
- Archivo o dataset afectado.
- Hallazgo pendiente.
- Dependencia relevante.
- Próximo paso concreto.
- Fecha de actualización.

## Qué eliminar

No copies conversaciones, código, tablas extensas, intentos fallidos ya resueltos ni explicaciones duplicadas.

## Límite

Cada archivo de `.opencode/memory` y `MEMORY.md` debe tener 50 líneas o menos. Si alcanza el límite, resume y mueve decisiones permanentes a `decisions.md`. Crea una memoria de sesión solo cuando aporte contexto que no esté registrado en otra parte.

## Cierre

Comprueba el número de líneas de todos los archivos de memoria y actualiza el índice únicamente si cambió el estado global.
