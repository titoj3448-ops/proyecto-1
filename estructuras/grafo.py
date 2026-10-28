"""Grafo simple no dirigido, sin pesos, con listas de adyacencia.

Se usan diccionarios para conservar el orden y evitar aristas repetidas.
"""
from collections import deque


class Grafo:
    def __init__(self):
        self._adyacencia = {}

    def agregar_vertice(self, vertice):
        self._adyacencia.setdefault(vertice, {})

    def _validar(self, vertice):
        if vertice not in self._adyacencia:
            raise KeyError(f"Vértice inexistente: {vertice}")

    def agregar_arista(self, origen, destino):
        self._validar(origen)
        self._validar(destino)
        if origen == destino:
            raise ValueError("Este grafo no admite lazos")
        self._adyacencia[origen][destino] = None
        self._adyacencia[destino][origen] = None

    def eliminar_arista(self, origen, destino):
        self._validar(origen)
        self._validar(destino)
        self._adyacencia[origen].pop(destino, None)
        self._adyacencia[destino].pop(origen, None)

    def hay_arista(self, origen, destino):
        self._validar(origen)
        self._validar(destino)
        return destino in self._adyacencia[origen]

    def vertices(self):
        return list(self._adyacencia)

    def vecinos(self, vertice):
        self._validar(vertice)
        return list(self._adyacencia[vertice])

    def cantidad_aristas(self):
        return sum(len(vecinos) for vecinos in self._adyacencia.values()) // 2

    def bfs(self, inicio):
        """Recorre la componente alcanzable por niveles."""
        self._validar(inicio)
        visitados = {inicio}
        cola = deque([inicio])
        recorrido = []
        while cola:
            actual = cola.popleft()
            recorrido.append(actual)
            for vecino in self._adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        return recorrido

    def dfs(self, inicio):
        """Recorrido en profundidad, con pila de iteradores y sin recursión."""
        self._validar(inicio)
        visitados = {inicio}
        recorrido = [inicio]
        pila = [iter(self._adyacencia[inicio])]
        while pila:
            try:
                vecino = next(pila[-1])
            except StopIteration:
                pila.pop()
                continue
            if vecino not in visitados:
                visitados.add(vecino)
                recorrido.append(vecino)
                pila.append(iter(self._adyacencia[vecino]))
        return recorrido


def construir_grafos(canciones):
    """Dos criterios comparables: mismo género y mismo artista.

    Cada índice del catálogo es un vértice único, aunque se repita un título.
    """
    grafos = {"genero": Grafo(), "artista": Grafo()}
    for grafo in grafos.values():
        for indice in range(len(canciones)):
            grafo.agregar_vertice(indice)
    for i, primera in enumerate(canciones):
        for j in range(i + 1, len(canciones)):
            segunda = canciones[j]
            for criterio, grafo in grafos.items():
                a = getattr(primera, criterio).strip().lower()
                b = getattr(segunda, criterio).strip().lower()
                if a == b:
                    grafo.agregar_arista(i, j)
    return grafos
