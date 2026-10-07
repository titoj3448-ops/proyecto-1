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

# Análisis TP4 + TP5 — AVL y Árbol General

**Proyecto:** SoundNode — Sistema de recomendaciones de música en terminal
**Integrantes:** Gustavo Abel Ojeda · Natanael Contardo Ceriani · Julian Ttito

---

## 1. ¿Qué resolvimos?

En esta etapa incorporamos dos estructuras de datos que resuelven problemas distintos dentro de SoundNode:

| Estructura | Problema que resuelve | Dónde se usa |
|---|---|---|
| **AVL** | Que las búsquedas por título y por artista sean siempre rápidas (O(log n)) incluso si el catálogo se carga ordenado | Opciones "1. Buscar canción por título" y "2. Buscar canción por artista" |
| **Árbol General** | Representar la jerarquía de géneros musicales (Rock → Grunge, Rock argentino, etc.) | Opción "5. Explorar categorías (árbol de géneros)" |

El AVL **reemplaza** al BST del TP3 en los dos índices (`indice_titulo` e `indice_artista`) sin cambiar el resto del programa, porque mantiene la misma interfaz (`insertar_multiple`, `buscar`, `buscar_por_prefijo`, `inorder`, `altura`, `comparaciones`).

---

## 2. TP4 — Árbol AVL

### 2.1 ¿Por qué AVL y no un BST común?

En el TP3 construimos un BST (`ArbolBinarioBusqueda`) y funcionó bien con los datos en el orden del JSON. El problema es que **su forma depende del orden de inserción**: si el catálogo se carga ordenado alfabéticamente (algo muy normal si viene de una base de datos con `ORDER BY titulo`), cada nodo nuevo queda a la derecha del anterior y el árbol se convierte en una lista enlazada, con búsqueda O(n).

Lo comprobamos con nuestro propio catálogo de 33 canciones: con los títulos ordenados alfabéticamente, el BST llega a **altura 33** (una cadena) y el AVL se queda en **altura 6**. El AVL resuelve esto con rotaciones automáticas que mantienen la altura en O(log n) sin importar el orden de inserción.

### 2.2 Rotaciones implementadas

| Tipo | Caso | Cuándo se aplica | Método |
|---|---|---|---|
| Rotación simple derecha | Izquierda-Izquierda | Factor de balance > 1 y el hijo izquierdo pesa a la izquierda (o está equilibrado) | `_rotacion_derecha` |
| Rotación simple izquierda | Derecha-Derecha | Factor de balance < -1 y el hijo derecho pesa a la derecha (o está equilibrado) | `_rotacion_izquierda` |
| Rotación doble izquierda-derecha | Izquierda-Derecha | Factor de balance > 1 pero el hijo izquierdo pesa a la derecha | `_rotacion_izquierda_derecha` |
| Rotación doble derecha-izquierda | Derecha-Izquierda | Factor de balance < -1 pero el hijo derecho pesa a la izquierda | `_rotacion_derecha_izquierda` |

El **factor de balance** de un nodo es `altura(hijo izquierdo) - altura(hijo derecho)`. Cada nodo guarda su altura (`NodoAVL.altura`), así que calcularlo es O(1). Después de cada inserción, `_balancear` recalcula la altura del nodo y, si el factor se sale de [-1, 1], aplica la rotación que corresponda. Además, el AVL cuenta cuántas rotaciones de cada tipo hizo (`avl.rotaciones`), lo que nos sirve como evidencia en las pruebas.

### 2.3 Casos de desbalance generados

Hicimos dos pruebas en `algoritmos/probar_avl.py`.

**a) Los 4 casos de rotación, con 3 claves cada uno.** En los cuatro casos el árbol termina con la misma forma (20 en la raíz, 10 y 30 como hijos), pero llegando por distintas rotaciones:

| Caso | Inserción | Rotación aplicada |
|---|---|---|
| Izquierda-Izquierda | 30, 20, 10 | `simple_derecha` |
| Derecha-Derecha | 10, 20, 30 | `simple_izquierda` |
| Izquierda-Derecha | 30, 10, 20 | `izquierda_derecha` |
| Derecha-Izquierda | 10, 30, 20 | `derecha_izquierda` |

**b) Datos de prueba ordenados** (el escenario que rompe un BST común):

```
A, B, C, D, E, F, G, H, I, J   (10 elementos en orden)
```

Con datos estrictamente crecientes solo aparece el caso Derecha-Derecha: el AVL hizo **6 rotaciones simples a la izquierda** y ninguna doble. Las rotaciones dobles necesitan un "zigzag" en la inserción, por eso las probamos aparte en el punto (a).

### 2.4 Comparación BST vs AVL

Resultados reales medidos en la computadora de desarrollo (`py algoritmos/comparar_bst_avl.py`). Se insertan claves en orden ascendente y se busca la **última** clave insertada (peor caso del BST). El tiempo de búsqueda es el promedio de 200 repeticiones.

| Métrica | BST común | AVL |
|---|---|---|
| Altura con 10 datos ordenados | **10** | **4** |
| Altura con 10.000 datos ordenados | 10.000 | 14 |
| Comparaciones al buscar entre 10.000 datos ordenados | 10.000 | 14 |
| Búsqueda con 10.000 datos ordenados | **0,58788 ms** | **0,00089 ms** |
| Complejidad peor caso búsqueda | O(n) | O(log n) |
| Complejidad promedio inserción | O(log n) | O(log n) |

Evolución según el tamaño (salida completa del script):

| N | Altura BST | Altura AVL | Comp. BST | Comp. AVL | Búsq. BST (ms) | Búsq. AVL (ms) | Insertar todo BST (ms) | Insertar todo AVL (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 10 | 4 | 10 | 4 | 0,00099 | 0,00048 | 0,02 | 0,05 |
| 100 | 100 | 7 | 100 | 7 | 0,00751 | 0,00046 | 0,43 | 0,61 |
| 1.000 | 1.000 | 10 | 1.000 | 10 | 0,05465 | 0,00063 | 21,62 | 4,62 |
| 10.000 | 10.000 | 14 | 10.000 | 14 | 0,58788 | 0,00089 | 2200,86 | 60,88 |

**Justificación:** insertar 10 elementos ordenados genera un BST de altura 10 (una cadena), mientras que el AVL tiene altura 4, que es el mínimo posible para 10 nodos. Con 10.000 datos el BST necesita 10.000 comparaciones por búsqueda contra 14 del AVL (unas **660 veces más rápido** en tiempo). La diferencia se nota todavía más al **construir** el índice: 2,2 segundos el BST contra 0,06 s el AVL, porque cada inserción en el BST degenerado recorre toda la cadena (O(n²) en total).

Dos observaciones honestas sobre la tabla:

- Con pocos datos (10) el BST inserta más rápido que el AVL (0,02 ms contra 0,05 ms), porque el AVL paga el costo extra de recalcular alturas y rotar. El AVL empieza a convenir recién cuando el árbol crece o cuando no controlamos el orden de carga.
- Las alturas del AVL (4, 7, 10, 14) coinciden con ⌈log₂(n+1)⌉, o sea, está prácticamente en el mínimo teórico.

### 2.5 Prueba del AVL

Salida de `py algoritmos/probar_avl.py`:

```
=== 1. Las 4 rotaciones (3 claves cada una) ===
  Izquierda-Izquierda    insertar [30, 20, 10] -> raíz=20, preorder=[20, 10, 30], rotación={'simple_derecha': 1}
  Derecha-Derecha        insertar [10, 20, 30] -> raíz=20, preorder=[20, 10, 30], rotación={'simple_izquierda': 1}
  Izquierda-Derecha      insertar [30, 10, 20] -> raíz=20, preorder=[20, 10, 30], rotación={'izquierda_derecha': 1}
  Derecha-Izquierda      insertar [10, 30, 20] -> raíz=20, preorder=[20, 10, 30], rotación={'derecha_izquierda': 1}

=== 2. Datos ordenados A..J: BST vs AVL ===
Altura BST : 10
Altura AVL : 4
Rotaciones AVL: {'simple_derecha': 0, 'simple_izquierda': 6, 'izquierda_derecha': 0, 'derecha_izquierda': 0} | total = 6
Raíz del AVL: D
Preorder AVL: ['D', 'B', 'A', 'C', 'H', 'F', 'E', 'G', 'I', 'J']
Inorder  AVL: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
¿AVL balanceado?: True
Buscar 'F': 6 (3 comparaciones)
Buscar 'Z': None

=== 3. Catálogo real de SoundNode (títulos) ===
Canciones: 33 | claves únicas: 33
Altura BST (orden del JSON): 10
Altura AVL                 : 6
¿AVL balanceado?: True
Buscar 'bohemian rhapsody': 'Bohemian Rhapsody' - Queen (Rock) [5:55] ⭐10.0 (3 comparaciones)
Buscar 'zzz': None
Prefijo 'the': ['The Thrill Is Gone', 'The Trooper']

--- Mismo catálogo, ordenado alfabéticamente antes de insertar ---
Altura BST: 33 | Altura AVL: 6
```

Resumen de lo que demuestra:

- **Altura del AVL: 4** para los 10 elementos ordenados (el BST dio 10).
- El inorder devuelve las claves ordenadas, así que el AVL sigue cumpliendo la propiedad de BST después de rotar.
- `esta_balanceado()` verifica que **todos** los nodos tengan factor de balance entre -1 y 1.
- Con el catálogo real, el AVL queda en altura 6, que es el mínimo posible para 33 nodos (2⁵ = 32 < 33), tanto con el orden del JSON como con los títulos ordenados.

### 2.6 Código del AVL

Archivo: `estructuras/avl.py`

- `NodoAVL`: nodo con `clave`, `valor`, hijos izquierdo/derecho y `altura`.
- `AVL`: árbol con inserción balanceada, búsqueda, búsqueda por prefijo y recorridos.
- Rotaciones: `_rotacion_izquierda`, `_rotacion_derecha`, `_rotacion_izquierda_derecha`, `_rotacion_derecha_izquierda`, más `_balancear` que decide cuál aplicar.
- Utilidades: `esta_balanceado()` (verificación para pruebas) y el contador `rotaciones`.

Fragmento central:

```python
def _balancear(self, nodo):
    self._actualizar_altura(nodo)
    factor = self._factor_balance(nodo)

    if factor > 1:  # pesa de más a la izquierda
        if self._factor_balance(nodo.izquierda) < 0:
            return self._rotacion_izquierda_derecha(nodo)
        return self._rotacion_derecha(nodo)

    if factor < -1:  # pesa de más a la derecha
        if self._factor_balance(nodo.derecha) > 0:
            return self._rotacion_derecha_izquierda(nodo)
        return self._rotacion_izquierda(nodo)

    return nodo
```

---

## 3. TP5 — Árbol General (N-ario)

### 3.1 ¿Qué es un árbol general?

A diferencia del árbol binario, donde cada nodo tiene como máximo 2 hijos, en un árbol general cada nodo puede tener **cualquier cantidad de hijos** (una lista `hijos`). Eso lo hace ideal para representar jerarquías naturales como los géneros musicales.

### 3.2 Jerarquía elegida del dominio

Armamos la jerarquía a partir de los **géneros reales** que aparecen en `datos/canciones.json` (los 9 géneros del catálogo están representados):

```
Música
├── Rock
│   ├── Grunge
│   └── Rock argentino
├── Pop
│   └── Synth-pop
├── Jazz
├── Blues
├── Salsa
└── Relajante
```

10 nodos, altura 3, 7 hojas.

**¿Por qué esta jerarquía?**

- Los géneros son una clasificación natural del dominio musical (el subgénero "es un tipo de" género).
- Permite explorar el catálogo por categorías: al elegir **Rock** se incluyen también sus subgéneros Grunge y Rock argentino (11 canciones), y al elegir **Música** se obtiene el catálogo completo (33 canciones).
- Se conecta con el AVL: **el AVL busca por título o artista, el árbol general organiza por categoría**.
- Reemplaza un truco frágil del código anterior: el filtro por género (`genero in c.genero.lower()`) funcionaba para "rock" solo porque el texto "rock" está contenido en "rock argentino", pero "grunge" nunca habría aparecido bajo "rock". El árbol hace explícita la relación.

### 3.3 Recorridos implementados

| Recorrido | Descripción | Complejidad |
|---|---|---|
| Amplitud (BFS) | Nivel por nivel, de arriba hacia abajo (con `deque`) | O(n) |
| Profundidad preorder | Nodo → hijos (de izquierda a derecha) | O(n) |
| Profundidad postorder | Hijos → nodo | O(n) |

Los tres aceptan un parámetro `desde=` para recorrer solo un subárbol; así obtenemos "Rock y todos sus descendientes" para filtrar canciones.

### 3.4 Prueba del árbol general

Salida de `py algoritmos/probar_arbol_general.py`:

```
=== Estructura ===
Música
├── Rock
│   ├── Grunge
│   └── Rock argentino
├── Pop
│   └── Synth-pop
├── Jazz
├── Blues
├── Salsa
└── Relajante

Nodos: 10 | Altura: 3 | Hojas: ['Grunge', 'Rock argentino', 'Synth-pop', 'Jazz', 'Blues', 'Salsa', 'Relajante']

=== Recorridos ===
Amplitud (BFS)      : ['Música', 'Rock', 'Pop', 'Jazz', 'Blues', 'Salsa', 'Relajante', 'Grunge', 'Rock argentino', 'Synth-pop']
Preorder (DFS)      : ['Música', 'Rock', 'Grunge', 'Rock argentino', 'Pop', 'Synth-pop', 'Jazz', 'Blues', 'Salsa', 'Relajante']
Postorder (DFS)     : ['Grunge', 'Rock argentino', 'Rock', 'Synth-pop', 'Pop', 'Jazz', 'Blues', 'Salsa', 'Relajante', 'Música']

=== Búsqueda ===
buscar('grunge') -> NodoGeneral('Grunge', hijos=0) | camino: Música > Rock > Grunge
buscar('Salsa') -> NodoGeneral('Salsa', hijos=0) | camino: Música > Salsa
buscar('Reggaeton') -> None | camino: no existe

=== Subárbol de 'Rock' ===
Preorder desde Rock: ['Rock', 'Grunge', 'Rock argentino']
Agregar hijo a un padre inexistente: None
```

Cómo leer los recorridos: BFS muestra primero los géneros principales y después los subgéneros; preorder agrupa cada género con sus subgéneros inmediatamente después; postorder lista primero los subgéneros y recién al final su género padre.

### 3.5 Código del árbol general

Archivo: `estructuras/arbol_general.py`

- `NodoGeneral`: nodo con `dato` y lista de `hijos`.
- `ArbolGeneral`: árbol con inserción, búsqueda y recorridos.
- Métodos: `insertar_raiz`, `agregar_hijo`, `buscar`, `amplitud`, `profundidad_preorder`, `profundidad_postorder`, y extras que usa la interfaz: `camino_hasta`, `altura`, `hojas`, `mostrar`.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde queda cada estructura?

```
┌────────────────────────────────────────────────────────────┐
│                   Interfaz de terminal                     │
│                     (algoritmo/main.py)                    │
├───────────────┬───────────────┬──────────────┬─────────────┤
│  Opción 1:    │  Opción 2:    │ Opciones 3-4:│  Opción 5:  │
│  Buscar       │  Buscar       │ Catálogo /   │  Explorar   │
│  por título   │  por artista  │ Filtrar      │  categorías │
│               │               │              │             │
│  usa: AVL     │  usa: AVL     │ usa: AVL     │  usa: Árbol │
│  (títulos)    │  (artistas)   │ (inorder) /  │  General    │
│               │               │ lista        │  (géneros)  │
└───────────────┴───────────────┴──────────────┴─────────────┘
```

La opción 3 (listar el catálogo ordenado) también usa el AVL, a través de su recorrido inorder.

### 4.2 Código de integración en `algoritmo/main.py`

**Import:**

```python
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
```

**Inicialización** (los dos índices pasan de BST a AVL y se agrega el árbol de géneros):

```python
def construir_indices(canciones):
    # TP4: índices AVL (auto-balanceados) para títulos y artistas
    indice_titulo = AVL()
    indice_artista = AVL()
    for c in canciones:
        indice_titulo.insertar_multiple(normalizar(c.titulo), c)
        indice_artista.insertar_multiple(normalizar(c.artista), c)
    return indice_titulo, indice_artista

def main():
    canciones = cargar_datos()
    indice_titulo, indice_artista = construir_indices(canciones)
    arbol_generos = construir_arbol_generos()
```

**Opción "Buscar"** (el código de `buscar_titulo` no cambió, porque el AVL tiene la misma interfaz que el BST):

```python
exacto = indice_titulo.buscar(texto)
comparaciones = indice_titulo.comparaciones
```

**Opción "Explorar categorías":**

```python
def explorar_categorias(arbol_generos, canciones):
    print(arbol_generos.mostrar())
    print("\nCategorías por amplitud:")
    for categoria in arbol_generos.amplitud():
        print(f"  - {categoria}")

    texto = input("\nElegí una categoría para ver sus canciones: ").strip()
    nodo = arbol_generos.buscar(texto)
    if nodo is None:
        print("Esa categoría no existe en la jerarquía.")
        return

    # La categoría elegida + todos sus descendientes
    generos = {g.lower() for g in arbol_generos.profundidad_preorder(desde=nodo)}
    encontrados = [c for c in canciones if c.genero.lower() in generos]
    for c in encontrados:
        print(c)
```

Ejemplo de ejecución real eligiendo "rock":

```
Ruta: Música > Rock
Géneros incluidos: Rock, Grunge, Rock argentino

'Smells Like Teen Spirit' - Nirvana (Grunge) [5:01] ⭐9.8
'Bohemian Rhapsody' - Queen (Rock) [5:55] ⭐10.0
'De Música Ligera' - Soda Stereo (Rock argentino) [5:01] ⭐10.0
...
Total: 11 canciones.
```

---

## 5. Análisis de complejidad

| Operación | AVL | Árbol General |
|---|---|---|
| Inserción | O(log n) | O(1) si ya tenemos el nodo padre; **O(n)** con `agregar_hijo(nombre_padre, ...)` porque primero busca al padre |
| Búsqueda | O(log n) | O(n) (recorrido por niveles hasta encontrar el dato) |
| Recorrido inorder | O(n) | — (no aplica; usa preorder/postorder) |
| Recorrido amplitud | O(n) | O(n) |
| Altura (peor caso) | O(log n) | O(n) (árbol degenerado: cada nodo con un solo hijo) |

### ¿Por qué el AVL es O(log n)?

El AVL mantiene el factor de balance entre -1 y +1 en cada nodo. Esto garantiza que la altura sea siempre proporcional a log₂(n). Lo medimos: con 1.000 nodos la altura es 10 y con 10.000 es 14, mientras que el BST degenerado tiene altura 1.000 y 10.000 respectivamente.

### ¿Por qué el árbol general no se auto-balancea?

Porque no tiene criterio de ordenamiento: su estructura refleja una jerarquía natural (un subgénero pertenece a un género), no un orden alfabético o numérico. Reordenar los nodos para "balancear" destruiría el significado. El costo de búsqueda O(n) es aceptable porque la cantidad de categorías suele ser pequeña (en SoundNode son 10; en un sistema real, decenas, no miles).

---

## 6. Conclusión

- El AVL garantiza búsquedas eficientes sin importar el orden de inserción, resolviendo el problema principal del BST. En nuestras mediciones, con 10.000 claves ordenadas la búsqueda pasó de 10.000 comparaciones a 14.
- El árbol general permite organizar el dominio en una jerarquía de géneros que mejora la experiencia al explorar el catálogo (elegir "Rock" trae también Grunge y Rock argentino).
- Ambas estructuras se complementan: el AVL resuelve la búsqueda eficiente por clave (título/artista) y el árbol general organiza la navegación por categorías.
- Ninguna de las dos se usó "por cumplir": el AVL resuelve un problema real y medible (el desbalance del BST con datos ordenados) y el árbol general resuelve otro (jerarquizar géneros, que antes dependía de un filtro por texto frágil).

---

## 7. Errores o dudas que tuvimos

1. **`RecursionError` en `altura()` del BST con datos ordenados.** Al armar el benchmark con 2.000 o más claves ordenadas, `ArbolBST.altura()` falló por el límite de recursión de Python (~1.000 niveles), porque con datos ordenados el árbol es una cadena. Es otra consecuencia práctica del desbalance. **Solución:** en el script de comparación usamos una función de altura iterativa (por niveles) para el BST. En el AVL no ocurre, porque su altura máxima es ~14 para 10.000 datos y además se guarda en cada nodo.
2. **`insertar_multiple` en el AVL.** En el BST, `insertar` devolvía el nodo nuevo; en el AVL la inserción es recursiva y los nodos pueden cambiar de lugar al rotar, así que el nodo insertado puede no ser el que devuelve la recursión. **Solución:** `insertar` actualiza la raíz y `insertar_multiple` vuelve a buscar el nodo con `buscar_nodo` después de insertar.
3. **Mayúsculas en el nombre del JSON.** El archivo está guardado como `datos/Canciones.json` pero el código lo abre como `datos/canciones.json`. En Windows funciona (no distingue mayúsculas), pero en Linux/macOS daría `FileNotFoundError`. Los scripts de prueba nuevos prueban ambos nombres; queda pendiente unificar el nombre del archivo.
4. **Rotaciones dobles con datos ordenados.** Al principio esperábamos ver los 4 tipos de rotación con A..J, pero con datos estrictamente crecientes solo aparece la simple izquierda. **Solución:** agregamos la prueba de 3 claves por caso para demostrar las cuatro.
5. **Imports desde subcarpetas (heredado del TP3).** Ejecutar scripts desde `algoritmos/` daba `ModuleNotFoundError`; los scripts nuevos reutilizan la solución del TP3 (agregar la raíz del proyecto a `sys.path`).

---

## 8. Datos y evidencia

- Script de prueba del AVL: `algoritmos/probar_avl.py`
- Script de prueba del árbol general: `algoritmos/probar_arbol_general.py`
- Script de comparación BST vs AVL: `algoritmos/comparar_bst_avl.py`
- Código: `estructuras/avl.py`, `estructuras/arbol_general.py`, integración en `algoritmo/main.py`
- Capturas de la terminal: `docs/capturas/`

Comandos para reproducir:

```
py algoritmos/probar_avl.py
py algoritmos/probar_arbol_general.py
py algoritmos/comparar_bst_avl.py
py algoritmo/main.py
```

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
