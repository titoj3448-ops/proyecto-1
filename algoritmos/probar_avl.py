import sys
from pathlib import Path
from time import perf_counter
from statistics import median

# Permite ejecutar el script desde la carpeta del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from estructuras.avl import ArbolAVL
from estructuras.arbol_binario import ArbolBST
from estructuras.arbol_general import ArbolGeneral


def probar_rotaciones():
    casos = [
        ("simple_derecha", [30, 20, 10]),
        ("simple_izquierda", [10, 20, 30]),
        ("doble_izquierda_derecha", [30, 10, 20]),
        ("doble_derecha_izquierda", [10, 30, 20]),
    ]

    for tipo, claves in casos:
        arbol = ArbolAVL()

        for clave in claves:
            arbol.insertar(clave)
            assert arbol.es_avl_valido(), f"Desbalance al insertar {clave}"

        assert arbol.inorder() == [10, 20, 30]
        assert arbol.preorder() == [20, 10, 30]
        assert arbol.postorder() == [10, 30, 20]
        assert arbol.altura() == 2
        assert arbol.rotaciones[tipo] == 1
        assert arbol.total_rotaciones() == 1
        print(f"OK: {tipo} y recorridos")


def probar_busquedas():
    arbol = ArbolAVL()
    assert arbol.esta_vacio()
    assert arbol.buscar(10) is None
    assert arbol.inorder() == []
    assert arbol.altura() == 0

    arbol.insertar(20, "Canción A")
    arbol.insertar(10, "Canción B")
    arbol.insertar(30, "Canción C")

    assert arbol.buscar(10) == "Canción B"
    assert arbol.buscar(99) is None
    assert len(arbol) == 3

    # Una clave repetida actualiza el valor, no agrega un nodo.
    arbol.insertar(10, "Canción actualizada")
    assert arbol.buscar(10) == "Canción actualizada"
    assert len(arbol) == 3
    assert arbol.es_avl_valido()

    artistas = ArbolAVL()
    artistas.insertar_multiple("queen", "Don't Stop Me Now")
    artistas.insertar_multiple("queen", "Somebody to Love")
    assert artistas.buscar("queen") == [
        "Don't Stop Me Now", "Somebody to Love"
    ]
    assert len(artistas) == 1
    print("OK: búsquedas, árbol vacío y claves repetidas")


def probar_arbol_general():
    arbol = ArbolGeneral()
    assert arbol.recorrido_amplitud() == []
    assert arbol.recorrido_profundidad() == []
    assert arbol.buscar("Rock") is None

    raiz = arbol.insertar_raiz("Catálogo")
    rock = arbol.agregar_hijo("Catálogo", "Rock")
    salsa = arbol.agregar_hijo("Catálogo", "Salsa")
    queen = arbol.agregar_hijo_a(rock, "Queen")
    marc = arbol.agregar_hijo_a(salsa, "Marc Anthony")

    amplitud = [
        nodo.nombre for nodo, _ in arbol.recorrido_amplitud()
    ]
    profundidad = [
        nodo.nombre for nodo, _ in arbol.recorrido_profundidad()
    ]

    assert amplitud == [
        "Catálogo", "Rock", "Salsa", "Queen", "Marc Anthony"
    ]
    assert profundidad == [
        "Catálogo", "Rock", "Queen", "Salsa", "Marc Anthony"
    ]
    assert arbol.buscar("queen") is queen
    assert arbol.buscar_profundidad("Marc Anthony") is marc
    assert arbol.buscar("No existe") is None
    assert arbol.camino(queen) == ["Catálogo", "Rock", "Queen"]
    assert queen.padre is rock
    assert rock.padre is raiz
    assert arbol.tamanio() == 5
    assert arbol.altura() == 3

    print("OK: árbol general, búsquedas y recorridos")


def medir_busqueda(arbol, clave, repeticiones=2000):
    # Mediana de cinco mediciones; cada una repite la búsqueda.
    muestras = []
    for _ in range(5):
        inicio = perf_counter()
        for _ in range(repeticiones):
            arbol.buscar(clave)
        muestras.append((perf_counter() - inicio) / repeticiones)
    return median(muestras) * 1_000_000


def comparar_bst_avl():
    print("\nDatos insertados en orden creciente.")
    print("Altura medida en nodos; tiempos en microsegundos por búsqueda.")
    print("| N | Altura BST | Altura AVL | Comp. BST | Comp. AVL | "
          "BST µs | AVL µs |")
    print("|---|---|---|---|---|---|---|")

    # Inserción ordenada: expone la degeneración del BST frente al AVL.
    for cantidad in (10, 100, 500, 10000):
        bst = ArbolBST()
        avl = ArbolAVL()

        for clave in range(cantidad):
            bst.insertar(clave)
            avl.insertar(clave)

        assert avl.es_avl_valido()
        assert bst.inorder() == avl.inorder() == list(range(cantidad))
        assert len(bst) == len(avl) == cantidad

        objetivo = cantidad - 1
        assert bst.buscar(objetivo) == objetivo
        comparaciones_bst = bst.comparaciones
        assert avl.buscar(objetivo) == objetivo
        comparaciones_avl = avl.comparaciones

        tiempo_bst = medir_busqueda(bst, objetivo)
        tiempo_avl = medir_busqueda(avl, objetivo)

        print(
            f"| {cantidad} | {bst.altura()} | {avl.altura()} | "
            f"{comparaciones_bst} | {comparaciones_avl} | "
            f"{tiempo_bst:.3f} | {tiempo_avl:.3f} |"
        )


def main():
    probar_rotaciones()
    probar_busquedas()
    probar_arbol_general()
    comparar_bst_avl()
    print("\nTodas las verificaciones de este script pasaron.")


if __name__ == "__main__":
    main()