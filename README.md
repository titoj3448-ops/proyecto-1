# SoundNode

Sistema de recomendaciones de música en terminal.

## Integrantes
- Gustavo Abel Ojeda
- Natanael Contardo Ceriani
- Julian Ttito

## Cómo ejecutar
1. Clonar el repositorio
2. Ejecutar: py ui/terminal.py

## Estado
TP0: Completado
TP1: Completado

# 📝 Historial de Cambios y Decisiones de Arquitectura — SoundNode

Este documento registra la evolución del proyecto, los cambios de estructura realizados y la justificación técnica de cada decisión tomada para facilitar el mantenimiento futuro del código.

---

## 📅 Versión 1.0.0 — Entrega 1 (TP0 + TP1) — Septiembre 2026

### 1. Reestructuración de Directorios
* **Cambio:** Se organizó el código suelto de la raíz en módulos específicos (`modelos/`, `datos/`, `ui/`, `docs/`).
* **Motivo:** Cumplir con la arquitectura por capas solicitada por la cátedra y separar la interfaz de usuario de la lógica de negocio y los datos.

### 2. Migración a Persistencia JSON
* **Cambio:** Se reemplazó la importación estática desde `base_de_datos.py` por la lectura dinámica de `datos/canciones.json`.
* **Motivo:** Permitir que la base de datos de canciones crezca de forma independiente al código ejecutable de Python, facilitando la adición de nuevo contenido sin tocar la lógica del programa.

### 3. Encapsulamiento del Modelo `Cancion`
* **Cambio:** Se redefinieron los atributos de la clase `Cancion` en `modelos/cancion.py` utilizando prefijos `_` y decoradores `@property`.
* **Motivo:** Proteger el estado interno de los objetos y asegurar que las lecturas de atributos como `titulo`, `artista`, `duracion` y `puntuacion` se hagan de forma controlada.

### 4. Modularización de la Interfaz CLI
* **Cambio:** Se implementó `ui/terminal.py` para gestionar el menú interactivo, incorporando búsquedas independientes por título y por artista, filtrado por género y listado general.
* **Motivo:** Proveer una experiencia de usuario contextualizada al dominio musical y dejar aislada la entrada/salida de datos para futuras adaptaciones (ej: interfaz gráfica o web).

### 5. Corrección de Compatibilidad de Sistema de Archivos y Módulos (Windows)
* **Cambio:** Se renombraron los directorios `algoritmo ` y `estructuras ` (eliminando espacios al final de los nombres de carpeta), se reubicó `arbol_binario.py` fuera de `__pycache__` a la raíz de `estructuras/`, y se configuró `.gitignore`.
* **Motivo:** Corregir errores de clonación y desincronización de Git en Windows, garantizar la resolución limpia de importaciones de paquetes locales y evitar el seguimiento de archivos compilados `.pyc`.

---

## 🛠️ Guía de Instalación y Ejecución

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/titoj3448-ops/proyecto-1.git](https://github.com/titoj3448-ops/proyecto-1.git)
cd proyecto-1
