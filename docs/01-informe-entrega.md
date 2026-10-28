# Informe de entrega — SoundNode

**Materia:** Estructuras de Datos, Tecnicatura en Programación, UNaB.  
**Profesor:** Ángel Leonardo Bianco.  
**Equipo:** Gustavo Abel Ojeda, Natanael Contardo Ceriani y Julián Tito.  
**Fecha de preparación:** 27 de octubre de 2026.

## 1. Alcance y relación con lo solicitado

La referencia utilizada es la transcripción de la última clase proporcionada.
Entre 2:45:56 y 2:46:02 se aclara que los recorridos y caminos mínimos no son
imprescindibles en esta instancia. Entre 2:49:17 y 2:50:44 se pide heap y grafos,
con una explicación de dónde y por qué usar el grafo. Entre 2:56:06 y 2:56:26
se exige la declaración del grafo en código y se propone incorporar BFS/DFS
en lo posible. La documentación debe explicar su utilización.

Esta entrega incluye heap, dos grafos aplicados a recomendaciones, comparación
de sus relaciones, y BFS/DFS funcionales. No incorpora Dijkstra: la clase indica
que todavía no es necesario implementarlo (aproximadamente 2:37:41).
La transcripción no permite establecer una fecha calendario de vencimiento;
la fecha indicada arriba corresponde a la preparación, no al plazo de entrega.

## 2. Problema y estructuras existentes

SoundNode permite explorar un catálogo musical, buscar canciones y obtener
recomendaciones basadas en relaciones explícitas. El catálogo contiene 33 canciones.

El modelo `Cancion` conserva título, artista, género, duración y puntuación.
Los índices AVL usan claves normalizadas con `strip().lower()`; agrupan las
canciones que comparten título o artista. La búsqueda exacta localiza una clave
sin recorrer todo el catálogo. El BST se mantiene para comparar su comportamiento.

El árbol general organiza una jerarquía con raíz Catálogo, categorías amplias,
géneros, artistas y canciones. Por ejemplo, Rock y Derivados incluye Rock,
Grunge y Rock argentino. Cada nodo puede tener varios hijos y referencia a su
padre, lo que permite navegar y volver. El árbol organiza pertenencias
jerárquicas; los grafos representan relaciones entre canciones al mismo nivel.

## 3. Heap: ranking por puntuación

Se implementó un max-heap binario propio en `estructuras/heap.py`.
No se emplea `heapq` ni un ordenamiento para generar el ranking.
La representación es una lista: para un índice i, los hijos están en 2i+1 y 2i+2,
y el padre en (i-1)//2. La prioridad del padre es mayor o igual que la de sus hijos.

- Al insertar, se agrega al final y se intercambia con el padre mientras corresponda.
- Al extraer, se devuelve la raíz, se sube el último elemento y se lo baja
  intercambiándolo con el hijo de mayor prioridad.
- Para empates se conserva el orden de inserción mediante un contador.
  Así no se comparan directamente objetos Cancion.
- La opción 6 construye un heap auxiliar y extrae hasta N canciones.
  El catálogo original no se modifica.

El heap sirve como cola de prioridad: cada extracción obtiene el siguiente máximo.
No está completamente ordenado como una lista; su propiedad garantiza el máximo
solo en la raíz y la relación de prioridad entre padres e hijos.

Con este catálogo, el Top 5 es:

| Posición | Canción | Puntuación |
|---|---|---:|
| 1 | Bohemian Rhapsody | 10.0 |
| 2 | De Música Ligera | 10.0 |
| 3 | Smells Like Teen Spirit | 9.8 |
| 4 | Master of Puppets | 9.8 |
| 5 | Billie Jean | 9.7 |

## 4. Grafos: dos criterios de relación

La clase `Grafo`, en `estructuras/grafo.py`, utiliza listas de adyacencia
representadas mediante un diccionario de diccionarios. El diccionario exterior
identifica vértices y el interior conserva vecinos sin duplicados y en orden
de inserción. Los valores interiores son None porque no hay pesos.

Cada vértice corresponde al índice de una canción en el catálogo cargado.
Esto distingue canciones aunque tengan el mismo título. Los índices son locales
a la sesión: no se presentan como identificadores persistentes si se reordena el JSON.

Se construyen dos grafos simples, no dirigidos y sin pesos:

| Grafo | Cuándo se agrega una arista | Vértices | Aristas |
|---|---|---:|---:|
| Género | Las dos canciones tienen el mismo género normalizado | 33 | 57 |
| Artista | Las dos canciones tienen el mismo artista normalizado | 33 | 7 |

Los números corresponden al catálogo incluido, no a todos los catálogos posibles.
Cada relación es simétrica y se almacena en ambos extremos, pero se cuenta una
sola arista. No se admiten lazos y repetir una inserción no duplica una arista.
Las canciones sin relaciones se conservan como vértices aislados.

La opción 7 devuelve vecinos por género; la opción 8, vecinos por artista.
Las dos opciones permiten comparar la amplitud de las recomendaciones con
criterios diferentes. No se interpreta una coincidencia de género como una
medición objetiva de similitud sonora ni como una colaboración musical.

¿Por qué grafos? Separan las relaciones del catálogo y permiten consultar vecinos
y recorrer conexiones. Para estos dos criterios simples también sería posible
filtrar una lista o usar el índice AVL de artista. El grafo aporta una representación
explícita sobre la cual se pueden extender relaciones y algoritmos de recorrido;
no se afirma que sea más eficiente que el AVL para buscar por artista.

Elegimos adyacencias porque permiten recorrer solo los vecinos existentes.
Una matriz necesitaría V² posiciones incluso donde no hay relación. Sin embargo,
cada grupo de igual género o artista forma un subgrafo completo; si un grupo crece
mucho, estas adyacencias también pueden ocupar espacio cuadrático.

## 5. BFS y DFS

La opción 9 compara ambos grafos desde la misma canción.

**BFS (anchura):** usa una cola `deque`; marca al descubrir y visita por niveles.
**DFS (profundidad):** usa una pila de iteradores; profundiza antes de continuar
con otros vecinos, sin depender de la recursión de Python.
Ambos mantienen un conjunto de visitados para evitar repeticiones en ciclos.
Devuelven solo los vértices alcanzables desde el inicio, incluyéndolo.
No incluyen automáticamente otras componentes desconectadas.

En estos grafos, cada criterio de igualdad forma grupos completos. Por eso todos
los integrantes del mismo grupo ya son vecinos directos y los órdenes BFS/DFS
pueden coincidir. La prueba con un grafo ramificado y un ciclo demuestra que las
implementaciones tienen comportamientos distintos cuando la topología lo permite.
Un recorrido es un orden de visita; no se presenta como un camino que una cada
par de elementos consecutivos ni como una enumeración de todos los caminos.

BFS no optimiza pesos. No se implementa camino mínimo en esta entrega. Como
extensión futura, se podría aplicar BFS para contar saltos en un grafo sin pesos,
o Dijkstra si se agregaran costos no negativos con significado musical explícito.

## 6. Complejidades de las implementaciones

V: vértices; E: aristas; n: canciones; k: cantidad solicitada para el ranking;
u: claves únicas en un índice; r: resultados de una búsqueda.

| Operación | Tiempo | Observación |
|---|---|---|
| Buscar clave exacta en AVL | O(log u) | Mostrar r resultados agrega O(r) |
| Buscar en BST degenerado | O(u) | Depende del orden de inserción |
| Recorrer árbol general | O(nodos del árbol) | Cada nodo se visita una vez |
| Insertar / extraer en heap | O(log n) | Reacomoda un camino de la altura |
| Consultar máximo del heap | O(1) | Lee la raíz |
| Construir el heap de esta versión | O(n log n) | Inserciones sucesivas |
| Top k completo | O(n log n + min(k,n) log n) | Incluye construir el heap |
| Agregar / consultar arista | O(1) promedio | Diccionarios hash |
| Listar vecinos | O(grado del vértice) | Devuelve una copia de sus claves |
| Construir los dos grafos | O(n²) comparaciones | Compara cada par una vez por criterio |
| BFS / DFS | O(V + E) | Cota para el grafo; solo exploran lo alcanzable |
| Contar aristas | O(V) | Suma tamaños de diccionarios de vecinos |

Memoria: heap O(n), grafos O(V + E), visitados/cola/pila de recorridos O(V).
La tabla trata las comparaciones de cadenas como de costo acotado; para cadenas
arbitrariamente largas también influye su longitud. Las operaciones hash tienen
las cotas indicadas en promedio, no como garantía absoluta de peor caso.
Se podría mejorar la construcción del heap a O(n) con heapify, pero no es lo
implementado. No se atribuye esa cota a la construcción actual.

## 7. Validación y evidencia

Se ejecutaron nueve pruebas automáticas en `algoritmos/probar_entrega.py`:
heap vacío, un elemento, empates, prioridades negativas, inserciones/extracciones
intercaladas, Top k frente a un ordenamiento de referencia, validación de aristas,
simetría, ciclos, vértices aislados, títulos repetidos y relaciones del catálogo.
También verifican que los índices AVL y las hojas del árbol general conserven
las canciones cargadas.

El script anterior `algoritmos/probar_avl.py` pasó sus verificaciones de cuatro
rotaciones, búsquedas, repetidos y árbol general. Comparó BST/AVL con datos
crecientes para 10, 100, 500 y 10.000 elementos. Con 10.000, las alturas fueron
10.000 y 14, y las comparaciones de búsqueda fueron 10.000 y 14 respectivamente.
Los tiempos medidos en este entorno figuran en `resultados_pruebas.txt`; no son
mediciones realizadas en la computadora del estudiante.

Se probaron las opciones 1 a 9 del menú con una sesión automatizada, una entrada
inválida del ranking y los tres puntos de entrada. La salida está en
`salida_demo.txt`. La validación se realizó con Python 3.12 en Linux; los comandos
para Windows usan `py`, pero no se realizó una ejecución nativa en Windows.

## 8. Límites y pendientes

- Catálogo estático en JSON; sin edición o guardado interactivo de canciones.
- Recomendación por coincidencia exacta normalizada de género/artista.
- Sin reproducción de audio, API de Spotify ni aprendizaje automático.
- Sin Dijkstra, caminos mínimos o conexiones de colaboración entre artistas.
- Los criterios de relación pueden producir grupos densos; construirlos por
  comparación de pares no es una solución destinada a millones de canciones.
- La propuesta inicial contiene ideas futuras; el alcance implementado es el
  que describen este informe y el menú actual.
