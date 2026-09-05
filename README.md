# 🎵 SoundNode — Sistema de Recomendaciones de Música

> **Estructura de Datos 2026** — Trabajo Práctico Integrador  
> **Universidad Nacional de Almirante Brown (UNAB)**

---

## 📌 Descripción del Proyecto

**SoundNode** es una aplicación de terminal desarrollada en Python que permite almacenar, buscar, filtrar y recomendar canciones a partir de relaciones de género, artistas y calificaciones.

El objetivo principal es aplicar estructuras de datos fundamentales (listas, árboles binarios, AVL, árboles generales, heaps y grafos) para optimizar la gestión y las consultas dentro de un dataset musical real.

---

## 🚀 Características y Funcionalidades (TP1)

- **POO / Encapsulamiento:** Representación del dominio mediante la clase `Cancion` con atributos protegidos.
- **Carga desde JSON:** Persistencia e importación de canciones desde archivo `canciones.json`.
- **Búsqueda eficiente:** Búsqueda secuencial por título de canción o artista.
- **Filtrado por género:** Filtro dinámico de temas según su estilo musical.
- **Rankings:** Obtención del Top de canciones mejor valoradas.
- **Interfaz de consola:** Menú interactivo CLI usable por cualquier usuario.

---

## 📂 Estructura del Repositorio

```text
proyecto-1/
├── 00-propuesta.md     # Documento de propuesta inicial y diagrama UML (TP0)
├── README.md           # Descripción e instrucciones de ejecución
├── canciones.json      # Dataset en formato JSON
├── cancion.py          # Clase del modelo de dominio (POO)
├── catalogo.py         # Lógica de almacenamiento, búsqueda y filtrado
└── main.py             # Punto de entrada y menú en consola (CLI)