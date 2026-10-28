# Guía breve para explicar SoundNode

## Demostración sugerida

1. Ejecutar `py main.py` desde la carpeta extraída.
2. Opción 1: escribir `bohemian rhapsody`. Mostrar la búsqueda AVL.
3. Opción 5: usar `t` para mostrar la jerarquía y `0` para volver.
4. Opción 6: pedir `5`. Explicar que se extraen máximos de un heap auxiliar.
5. Opción 7: escribir `bohemian`, seleccionar `1`. Mostrar otras canciones Rock.
6. Opción 8: repetir la selección para comparar las del mismo artista.
7. Opción 9: repetir la selección para mostrar aristas, BFS y DFS.
8. Ejecutar `py algoritmos/probar_entrega.py` para mostrar las nueve pruebas.

## Preguntas que conviene poder responder

**¿Para qué usan AVL?** Para localizar títulos y artistas con altura balanceada.
Los duplicados de una clave se guardan juntos; buscar la clave y mostrar todas
sus canciones son costos diferentes.

**¿Para qué usan el árbol general?** Para organizar el catálogo en categorías,
géneros, artistas y canciones, y permitir navegar entre niveles.

**¿Para qué usan heap?** Para sacar repetidamente la canción de mayor puntuación.
La raíz es el máximo. Insertar sube el nuevo elemento; extraer baja el que reemplaza
la raíz. Los empates respetan el orden del catálogo.

**¿Qué es un vértice?** Una canción, identificada por su posición en el catálogo.
**¿Qué es una arista?** Una relación por género o por artista, según el grafo.
**¿Por qué no dirigido?** Compartir artista o género es una relación simétrica.
**¿Por qué sin pesos?** Solo modelamos si existe o no la relación.

**¿Por qué dos grafos?** Para comparar qué cambia al elegir distinto criterio.
Con los datos actuales hay 57 aristas por género y 7 por artista.

**¿Qué diferencia hay entre BFS y DFS?** BFS usa cola y visita por niveles;
DFS usa pila y profundiza. Ambos evitan volver a visitar un vértice.
En grupos completos pueden dar el mismo orden; las pruebas incluyen un grafo
con ramificaciones en el que los órdenes difieren.

**¿Qué pasa si no hay canciones relacionadas?** La canción permanece como
vértice aislado; sus vecinos son una lista vacía y el recorrido incluye solo el inicio.

**¿Qué falta?** Los caminos mínimos no se implementaron en esta etapa.
Las relaciones son reglas explícitas, no recomendaciones aprendidas del usuario.

Antes de entregar, abrir el proyecto en tu computadora, recorrer el menú y
practicar estas respuestas con tus palabras. Esta guía no reemplaza entender el código.
