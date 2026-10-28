import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modelos.cancion import Cancion
from estructuras.avl import ArbolAVL
from estructuras.heap import top_canciones
from estructuras.grafo import construir_grafos
from estructuras.arbol_general import construir_catalogo


def normalizar(texto):
    return texto.strip().lower()


def cargar_datos():
    ruta_json = os.path.join(BASE_DIR, "datos", "canciones.json")

    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    canciones = []

    for dato in datos:
        duracion = dato.get("duracion", "N/A")
        puntuacion = dato.get("puntuacion", dato.get("rating", 0.0))

        cancion = Cancion(
            dato["titulo"],
            dato["artista"],
            dato["genero"],
            duracion,
            puntuacion,
        )

        canciones.append(cancion)

    return canciones


def construir_indices(canciones):
    indice_titulo = ArbolAVL()
    indice_artista = ArbolAVL()

    for cancion in canciones:
        indice_titulo.insertar_multiple(
            normalizar(cancion.titulo),
            cancion,
        )
        indice_artista.insertar_multiple(
            normalizar(cancion.artista),
            cancion,
        )

    return indice_titulo, indice_artista


def mostrar_menu():
    print("\n" + "=" * 48)
    print("       SOUNDNODE — CATÁLOGO MUSICAL")
    print("=" * 48)
    print("1. Buscar canción por título (AVL)")
    print("2. Buscar canción por artista (AVL)")
    print("3. Ver todo el catálogo de canciones")
    print("4. Filtrar por género musical")
    print("5. Explorar categorías (Árbol General)")
    print("6. Top de canciones por puntuación (Heap)")
    print("7. Recomendaciones por género (Grafo)")
    print("8. Recomendaciones por artista (Grafo)")
    print("9. Comparar grafos y recorridos BFS / DFS")
    print("0. Salir")
    print("-" * 48)


def buscar_titulo(indice_titulo):
    texto = normalizar(input("Título de la canción a buscar: "))

    if not texto:
        print("No ingresaste ningún título.")
        return

    resultados = indice_titulo.buscar(texto)
    comparaciones = indice_titulo.comparaciones

    if resultados:
        for cancion in resultados:
            print(cancion)

        print(
            f"Búsqueda exacta: {comparaciones} nodos visitados."
        )
    else:
        resultados = indice_titulo.buscar_por_prefijo(texto)

        if resultados:
            print("Coincidencias por comienzo del título:")

            for cancion in resultados:
                print(cancion)
        else:
            print("No se encontraron canciones con ese título.")

    print("Fin de resultados.")


def buscar_artista(indice_artista):
    texto = normalizar(input("Nombre del artista o banda: "))

    if not texto:
        print("No ingresaste ningún artista.")
        return

    resultados = indice_artista.buscar(texto)
    comparaciones = indice_artista.comparaciones

    if resultados:
        for cancion in resultados:
            print(cancion)

        print(
            f"Búsqueda exacta: {comparaciones} nodos visitados."
        )
    else:
        resultados = indice_artista.buscar_por_prefijo(texto)

        if resultados:
            print("Coincidencias por comienzo del nombre:")

            for cancion in resultados:
                print(cancion)
        else:
            print("No se encontraron canciones de ese artista.")

    print("Fin de resultados.")


def listar(indice_titulo):
    print("\n--- CATÁLOGO COMPLETO (ordenado por título) ---")

    if indice_titulo.esta_vacio():
        print("El catálogo está vacío.")
        return

    numero = 1

    for grupo in indice_titulo.inorder(datos=True):
        for cancion in grupo:
            print(f"{numero}. {cancion}")
            numero += 1


def filtrar(canciones):
    genero = normalizar(
        input("Género musical (ejemplo: Rock, Pop, Jazz, Salsa): ")
    )

    if not genero:
        print("No ingresaste ningún género.")
        return

    encontrados = False

    for cancion in canciones:
        if genero in normalizar(cancion.genero):
            print(cancion)
            encontrados = True

    if not encontrados:
        print("No se encontraron canciones de ese género.")


def mostrar_nivel(arbol, nodo):
    print("\n" + " > ".join(arbol.camino(nodo)))

    if nodo.es_hoja() and nodo.dato is not None:
        print(nodo.dato)
        return

    if not nodo.hijos:
        print("Esta categoría está vacía.")

    for numero, hijo in enumerate(nodo.hijos, 1):
        cantidad = arbol.contar_hojas(hijo)
        etiqueta = "canción" if cantidad == 1 else "canciones"

        print(
            f"  {numero}. {hijo.nombre} "
            f"({cantidad} {etiqueta})"
        )

    print(
        "  [número] entrar | [v] volver | "
        "[t] ver árbol de esta rama | [b] buscar nodo | [0] salir"
    )


def explorar_categorias(arbol):
    if arbol.raiz is None:
        print("No hay categorías para explorar.")
        return

    actual = arbol.raiz

    while True:
        mostrar_nivel(arbol, actual)

        if actual.es_hoja() and actual.dato is not None:
            if actual.padre is None:
                return

            actual = actual.padre
            continue

        opcion = input("Explorar: ").strip().lower()

        if opcion == "0":
            return

        elif opcion == "v":
            if actual.padre is not None:
                actual = actual.padre
            else:
                print("Ya estás en la raíz.")

        elif opcion == "t":
            print(arbol.a_texto(actual))

        elif opcion == "b":
            texto = input("Nombre (o parte) a buscar: ").strip()

            if not texto:
                print("No ingresaste ningún nombre.")
                continue

            coincidencias = arbol.buscar_todos(texto)

            if not coincidencias:
                print("No se encontró ningún nodo.")
                continue

            for numero, nodo in enumerate(coincidencias, 1):
                ruta = " > ".join(arbol.camino(nodo))
                print(f"  {numero}. {ruta}")

            eleccion = input(
                "Ir a (número, Enter para cancelar): "
            ).strip()

            if not eleccion:
                continue

            try:
                numero = int(eleccion)
            except ValueError:
                print("Ingresá un número válido.")
                continue

            if 1 <= numero <= len(coincidencias):
                actual = coincidencias[numero - 1]
            else:
                print("El número está fuera de las opciones.")

        else:
            try:
                numero = int(opcion)
            except ValueError:
                print("Opción inválida.")
                continue

            if 1 <= numero <= len(actual.hijos):
                actual = actual.hijos[numero - 1]
            else:
                print("Opción inválida.")


def mostrar_top(canciones):
    try:
        cantidad = int(input("¿Cuántas canciones querés ver?: "))
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print("Ingresá un entero mayor que cero.")
        return
    for numero, cancion in enumerate(top_canciones(canciones, cantidad), 1):
        print(f"{numero}. {cancion}")


def elegir_cancion(canciones):
    texto = normalizar(input("Título o parte del título (Enter para cancelar): "))
    if not texto:
        return None
    opciones = [i for i, c in enumerate(canciones) if texto in normalizar(c.titulo)]
    if not opciones:
        print("No se encontraron canciones.")
        return None
    for numero, indice in enumerate(opciones, 1):
        print(f"{numero}. {canciones[indice]}")
    try:
        numero = int(input("Elegí el número de canción (0 cancela): "))
    except ValueError:
        print("Ingresá un número válido.")
        return None
    if numero == 0:
        return None
    if not 1 <= numero <= len(opciones):
        print("Número fuera de rango.")
        return None
    return opciones[numero - 1]


def recomendar(canciones, grafo, criterio):
    indice = elegir_cancion(canciones)
    if indice is None:
        return
    vecinos = grafo.vecinos(indice)
    print(f"Relacionadas por {criterio}: {len(vecinos)} canciones.")
    if not vecinos:
        print("Esta canción no tiene vecinas según este criterio.")
    for vecino in vecinos:
        print(canciones[vecino])


def comparar_grafos(canciones, grafos):
    indice = elegir_cancion(canciones)
    if indice is None:
        return
    for criterio, grafo in grafos.items():
        print(f"\nGrafo por {criterio}: {len(grafo.vertices())} vértices, "
              f"{grafo.cantidad_aristas()} aristas")
        print(f"Vecinos de la canción elegida: {len(grafo.vecinos(indice))}")
        for nombre, recorrido in (("BFS", grafo.bfs(indice)), ("DFS", grafo.dfs(indice))):
            print(f"{nombre}: {len(recorrido)} canciones alcanzables (incluye el inicio)")
            for paso, vertice in enumerate(recorrido, 1):
                print(f"  {paso}. {canciones[vertice]}")


def main():
    canciones = cargar_datos()

    indice_titulo, indice_artista = construir_indices(canciones)
    arbol_categorias = construir_catalogo(canciones)
    grafos = construir_grafos(canciones)

    print(
        f"Catálogo cargado: {len(canciones)} canciones | "
        f"altura AVL de títulos: {indice_titulo.altura()} | "
        f"rebalanceos por rotación: "
        f"{indice_titulo.total_rotaciones()}"
    )

    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            buscar_titulo(indice_titulo)

        elif opcion == "2":
            buscar_artista(indice_artista)

        elif opcion == "3":
            listar(indice_titulo)

        elif opcion == "4":
            filtrar(canciones)

        elif opcion == "5":
            explorar_categorias(arbol_categorias)

        elif opcion == "6":
            mostrar_top(canciones)

        elif opcion in ("7", "8"):
            criterio = "genero" if opcion == "7" else "artista"
            recomendar(canciones, grafos[criterio], criterio)

        elif opcion == "9":
            comparar_grafos(canciones, grafos)

        elif opcion == "0":
            print("¡Gracias por usar SoundNode!")
            break

        else:
            print("Opción inválida. Elegí una opción del menú.")


if __name__ == "__main__":
    main()