# SoundNode

Sistema de recomendaciones de música en terminal.

## Integrantes

* Gustavo Abel Ojeda
* Natanael Contardo Ceriani
* Julian Ttito

## Cómo ejecutar

1. Clonar el repositorio
2. Ejecutar: `py ui/terminal.py`
3. Probar BST: `py algoritmos/probar_bst.py`
4. Benchmark tiempos: `py algoritmos/comparar_busquedas.py`

## Estado

TP0: Completado | TP1: Completado | TP2: Completado | TP3: Completado

# 📝 Historial de Cambios y Decisiones de Arquitectura — SoundNode

Este documento registra la evolución del proyecto, los cambios de estructura realizados y la justificación técnica de cada decisión tomada para facilitar el mantenimiento futuro del código.

---

## 📅 Versión 1.2.0 — Entrega 3 (TP3 - Árbol Binario de Búsqueda) — Septiembre 2026

### 1. Implementación de la Estructura Árbol BST
* **Cambio:** Se crearon las clases `NodoBST` y `ArbolBST` en `estructuras/arbol_binario.py` implementando inserción ordenada, búsqueda por clave y recorridos jerárquicos (`inorder`, `preorder`, `postorder`).
* **Motivo:** Optimizar las búsquedas en el catálogo pasando de una complejidad lineal O(n) a una complejidad logarítmica O(log n).

### 2. Creación del Módulo de Pruebas Unitarias del BST
* **Cambio:** Se desarrolló el script ejecutable `algoritmos/probar_bst.py` que instancia el árbol, inserta canciones del catálogo, calcula la altura y prueba búsquedas.
* **Motivo:** Verificar el correcto funcionamiento lógico de la estructura antes de integrarla al flujo general y facilitar la evaluación por parte del docente.

### 3. Medición y Comparación de Tiempos Reales (Benchmarking)
* **Cambio:** Se implementó el benchmark en `algoritmos/comparar_busquedas.py` que evalúa el rendimiento de tres algoritmos de búsqueda (Secuencial, Binaria y Árbol BST) sobre volúmenes escalables de datos (100 a 100.000 elementos) midiendo tiempos en ms.
* **Motivo:** Comparar de forma empírica y real el tiempo de ejecución de cada algoritmo en la computadora de desarrollo.

### 4. Organización del Módulo de Algoritmos
* **Cambio:** Se movieron los scripts de pruebas dentro de `algoritmos/` y se configuró la adición dinámica del directorio raíz al `sys.path`.
* **Motivo:** Mantener la separación de responsabilidades y resolver errores de importación (`ModuleNotFoundError`) al ejecutar scripts desde subcarpetas en Windows.

### 5. Documentación de Análisis de Complejidad
* **Cambio:** Se creó el informe técnico en `docs/07-analisis-tp3.md` con la tabla de tiempos reales de ejecución, capturas/salidas de terminal y el análisis de complejidad teórica de cada algoritmo.
* **Motivo:** Documentar las conclusiones requeridas en la consigna de la Entrega 3.

---

## 📅 Versión 1.0.0 — Entrega 1 (TP0 + TP1) — Septiembre 2026

### 1. Reestructuración de Directorios
* **Cambio:** Se organizó el código suelto de la raíz en módulos específicos (`modelos/`, `datos/`, `ui/`, `docs/`).
* **Motivo:** Cumplir con la arquitectura por capas solicitada por la cátedra y separar la interfaz de usuario de la lógica de negocio y los datos.

### 2. Migración a Persistencia JSON
* **Cambio:** Se reemplazó la importación estática desde `base_de_datos.py` por la lectura dinámica de `datos/canciones.json`.
* **Motivo:** Permitir que la base de datos de canciones crezca de forma independiente al código ejecutable de Python, facilitando la adición de nuevo contenido sin tocar la lógica del programa.

### 3. Encapsulamiento del Modelo Cancion
* **Cambio:** Se redefinieron los atributos de la clase `Cancion` en `modelos/cancion.py` utilizando prefijos `_` y decoradores `@property`.
* **Motivo:** Proteger el estado interno de los objetos y asegurar que las lecturas de atributos como `titulo`, `artista`, `duracion` y `puntuacion` se hagan de forma controlada.

### 4. Modularización de la Interfaz CLI
* **Cambio:** Se implementó `ui/terminal.py` para gestionar el menú interactivo, incorporando búsquedas independientes por título y por artista, filtrado por género y listado general.
* **Motivo:** Proveer una experiencia de usuario contextualizada al dominio musical y dejar aislada la entrada/salida de datos para futuras adaptaciones (ej: interfaz gráfica o web).

### 5. Corrección de Compatibilidad de Sistema de Archivos y Módulos (Windows)
* **Cambio:** Se renombraron los directorios `algoritmo` y `estructuras` (eliminando espacios al final de los nombres de carpeta), se reubicó `arbol_binario.py` fuera de `__pycache__` a la raíz de `estructuras/`, y se configuró `.gitignore`.
* **Motivo:** Corregir errores de clonación y desincronización de Git en Windows, garantizar la resolución limpia de importaciones de paquetes locales y evitar el seguimiento de archivos compilados `.pyc`.