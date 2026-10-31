# SoundNode — guía de uso y estructuras

## Ejemplo de uso

Desde la carpeta del proyecto, ejecutar `py main.py` (Windows) o
`python3 main.py` (Linux/macOS).

| Paso | Entrada | Resultado |
|---|---|---|
| Buscar por título | Opción 1, `bohemian rhapsody` | Canción encontrada mediante el índice AVL |
| Explorar categorías | Opción 5, luego `t` | Jerarquía del catálogo; `0` vuelve al menú |
| Consultar ranking | Opción 6, cantidad `5` | Las cinco canciones con mayor puntuación |
| Relacionar por género | Opción 7, `bohemian`, selección `1` | Canciones que comparten el género Rock |
| Relacionar por artista | Opción 8, misma canción | Canciones del catálogo que comparten el artista |
| Comparar recorridos | Opción 9, misma canción | Vértices, aristas y recorridos BFS/DFS de ambos grafos |

La búsqueda usada para seleccionar una canción en las opciones 7 a 9 permite
escribir parte del título. Si aparecen varias coincidencias, se elige una por
su número. Una canción sin vecinas no produce recomendaciones con ese criterio.

## Función de cada estructura

### AVL: búsqueda por título y artista

Los índices AVL localizan claves manteniendo una altura balanceada.
Las canciones que comparten una clave se guardan juntas. Localizar la clave
cuesta O(log u), donde u es la cantidad de claves únicas; mostrar sus resultados
agrega un costo proporcional a la cantidad de canciones encontradas.

### Árbol general: categorías

Organiza el catálogo en categorías, géneros, artistas y canciones. Cada nodo
puede tener varios hijos y una referencia a su padre, lo que permite entrar
a una categoría y regresar al nivel anterior.

### Heap: ranking

El max-heap mantiene la canción de mayor prioridad en la raíz. La inserción
reacomoda el elemento hacia arriba y la extracción reacomoda el reemplazo de
la raíz hacia abajo. Los empates respetan el orden de carga del catálogo.
El ranking se obtiene extrayendo máximos de un heap auxiliar.

### Grafos: relaciones entre canciones

Cada vértice identifica una canción por su posición en el catálogo.
Una arista conecta canciones del mismo género o del mismo artista, según el
grafo elegido. Son relaciones simétricas, por lo que los grafos son no dirigidos.
No tienen pesos: cada arista indica únicamente la existencia de una relación.

Con el catálogo incluido, ambos grafos tienen 33 vértices. El de género tiene
57 aristas y el de artista tiene 7. Una canción sin relaciones permanece como
vértice aislado.

### BFS y DFS: recorridos

BFS utiliza una cola y visita por niveles. DFS utiliza una pila y profundiza
antes de continuar por otros vecinos. Ambos registran los vértices visitados
para evitar repeticiones y recorren solo la componente alcanzable desde el inicio.

Los grupos de igual género o artista son completos: sus canciones están
conectadas entre sí. Por eso BFS y DFS pueden producir el mismo orden en estos
datos. Las pruebas también incluyen un grafo con ramificaciones y un ciclo,
en el que los órdenes son diferentes.

## Verificación

Las pruebas de heap, grafos e integración se ejecutan con:

```bash
py algoritmos/probar_entrega.py
```

El script contiene nueve pruebas. Los resultados registrados se encuentran en
[resultados_pruebas.txt](resultados_pruebas.txt), y una sesión del menú está en
[salida_demo.txt](salida_demo.txt).

## Alcance

Las recomendaciones se basan en coincidencias de género o artista. No se usa
aprendizaje automático ni se reproduce audio. Los caminos mínimos no están
implementados en esta etapa.
