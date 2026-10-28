"""Verificaciones funcionales: ejecutar con python algoritmos/probar_entrega.py."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from algoritmo.main import cargar_datos, construir_indices
from estructuras.heap import MaxHeap, top_canciones
from estructuras.grafo import Grafo, construir_grafos
from estructuras.arbol_general import construir_catalogo
from modelos.cancion import Cancion


class PruebasEntrega(unittest.TestCase):
    def test_heap_vacio_y_un_elemento(self):
        heap = MaxHeap()
        with self.assertRaises(IndexError):
            heap.extraer_maximo()
        heap.insertar("único", 2)
        self.assertEqual(heap.ver_maximo(), "único")
        self.assertEqual(heap.extraer_maximo(), "único")
        self.assertTrue(heap.esta_vacio())

    def test_heap_orden_y_empates(self):
        azar = random.Random(42)
        prioridades = [azar.randint(-10, 10) for _ in range(300)]
        heap = MaxHeap()
        for i, prioridad in enumerate(prioridades):
            heap.insertar(i, prioridad)
        esperado = sorted(range(len(prioridades)), key=lambda i: -prioridades[i])
        self.assertEqual([heap.extraer_maximo() for _ in prioridades], esperado)

    def test_heap_operaciones_intercaladas(self):
        heap = MaxHeap()
        heap.insertar("A", 4)
        heap.insertar("B", 2)
        self.assertEqual(heap.extraer_maximo(), "A")
        heap.insertar("C", 9)
        self.assertEqual(heap.extraer_maximo(), "C")
        self.assertEqual(heap.extraer_maximo(), "B")

    def test_top_catalogo(self):
        canciones = cargar_datos()
        esperado = sorted(canciones, key=lambda c: -c.puntuacion)
        self.assertEqual(top_canciones(canciones, 5), esperado[:5])
        self.assertEqual(top_canciones(canciones, 999), esperado)
        self.assertEqual(top_canciones(canciones, 0), [])
        self.assertEqual(top_canciones([], 5), [])
        with self.assertRaises(ValueError):
            top_canciones(canciones, -1)

    def test_aristas_y_validaciones(self):
        g = Grafo()
        for v in range(3):
            g.agregar_vertice(v)
        g.agregar_arista(0, 1)
        g.agregar_arista(0, 1)
        self.assertEqual(g.cantidad_aristas(), 1)
        self.assertTrue(g.hay_arista(1, 0))
        with self.assertRaises(ValueError):
            g.agregar_arista(0, 0)
        with self.assertRaises(KeyError):
            g.agregar_arista(0, 99)
        g.eliminar_arista(1, 0)
        self.assertFalse(g.hay_arista(0, 1))
        self.assertEqual(g.cantidad_aristas(), 0)

    def test_recorridos_ciclo_y_aislado(self):
        g = Grafo()
        for v in "ABCDEZ":
            g.agregar_vertice(v)
        for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("D", "E"), ("E", "C")]:
            g.agregar_arista(a, b)
        self.assertEqual(g.bfs("A"), list("ABCDE"))
        self.assertEqual(g.dfs("A"), list("ABDEC"))
        self.assertEqual(g.bfs("Z"), ["Z"])
        self.assertEqual(g.dfs("Z"), ["Z"])
        with self.assertRaises(KeyError):
            g.bfs("inexistente")

    def test_relaciones_y_titulos_repetidos(self):
        canciones = [Cancion("Tema", "A", "Rock"), Cancion("Tema", "B", "Rock"),
                     Cancion("Otro", "a", "Jazz"), Cancion("Solo", "C", "Pop")]
        grafos = construir_grafos(canciones)
        self.assertEqual(grafos["genero"].vecinos(0), [1])
        self.assertEqual(grafos["artista"].vecinos(0), [2])
        self.assertEqual(grafos["genero"].vecinos(3), [])
        self.assertEqual(len(grafos["genero"].vertices()), 4)

    def test_relaciones_catalogo_completo(self):
        canciones = cargar_datos()
        for criterio, grafo in construir_grafos(canciones).items():
            for i, c in enumerate(canciones):
                esperado = {j for j, otra in enumerate(canciones) if j != i and
                            getattr(c, criterio).strip().lower() == getattr(otra, criterio).strip().lower()}
                self.assertEqual(set(grafo.vecinos(i)), esperado)
                self.assertEqual(set(grafo.bfs(i)), esperado | {i})
                self.assertEqual(set(grafo.dfs(i)), esperado | {i})

    def test_indices_y_categorias(self):
        canciones = cargar_datos()
        titulo, artista = construir_indices(canciones)
        self.assertTrue(titulo.es_avl_valido())
        self.assertTrue(artista.es_avl_valido())
        for c in canciones:
            self.assertIn(c, titulo.buscar(c.titulo.strip().lower()))
            self.assertIn(c, artista.buscar(c.artista.strip().lower()))
        arbol = construir_catalogo(canciones)
        hojas = [n.dato for n, _ in arbol.recorrido_amplitud() if n.dato is not None]
        self.assertCountEqual(hojas, canciones)


if __name__ == "__main__":
    unittest.main(verbosity=2)
