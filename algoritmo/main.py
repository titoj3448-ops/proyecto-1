import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modelos.cancion import Cancion
from estructuras.Avl import ArbolAVL
from estructuras.Arbol_general import construir_catalogo


def normalizar(texto):
    return texto.strip().lower()


def cargar_datos():
    ruta_json = os.path.join(BASE_DIR, "datos", "canciones.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    canciones = []
    for d in datos:
        duracion = d.get("duracion", "N/A")
        puntuacion = d.get("puntuacion", d.get("rating", 0.0))
        canciones.append(Cancion(d["titulo"], d["artista"], d["genero"], duracion, puntuacion))
    return canciones


def construir_indices(canciones):
    indice_titulo = ArbolAVL()
    indice_artista = ArbolAVL()
    for c in canciones:
        indice_titulo.insertar_multiple(normalizar(c.titulo), c)
        indice_artista.insertar_multiple(normalizar(c.artista), c)
    return indice_titulo, indice_artista


def mostrar_menu():
    print("=" * 40)
    print("      🎵 SOUNDNODE — CATÁLOGO MUSICAL 🎵")
    print("=" * 40)
    print("1. Buscar canción por título (AVL)")
    print("2. Buscar canción por artista (AVL)")
    print("3. Ver todo el catálogo de canciones")
    print("4. Filtrar por género musical")
    print("5. Explorar categorías")
    print("0. Salir")
    print("-" * 40)


def buscar_titulo(indice_titulo):
    texto = normalizar(input("Título de la canción a buscar: "))
    if not texto:
        print("No ingresaste ningún título.")
        return

    exacto = indice_titulo.buscar(texto)
    comparaciones = indice_titulo.comparaciones

    if exacto:
        for c in exacto:
            print(c)
        print(f"(encontrado en {comparaciones} comparaciones)")
    else:
        parciales = indice_titulo.buscar_por_prefijo(texto)
        if parciales:
            for c in parciales:
                print(c)
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
        for c in resultados:
            print(c)
        print(f"(encontrado en {comparaciones} comparaciones)")
    else:
        resultados = indice_artista.buscar_por_prefijo(texto)
        if resultados:
            for c in resultados:
                print(c)
        else:
            print("No se encontraron canciones de ese artista.")
    print("Fin de resultados.")


def listar(indice_titulo):
    print("\n--- CATÁLOGO COMPLETO (ordenado por título) ---")
    i = 1
    for grupo in indice_titulo.inorder(datos=True):
        for c in grupo:
            print(f"{i}. {c}")
            i += 1


def filtrar(canciones):
    genero = input("Género musical (ej: Rock, Pop, Grunge, jazz, salsa, relajante, blues): ").lower()
    encontrados = False
    for c in canciones:
        if genero in c.genero.lower():
            print(c)
            encontrados = True
    if not encontrados:
        print("No se encontraron canciones de ese género.")


def mostrar_nivel(arbol, nodo):
    print("\n" + " > ".join(arbol.camino(nodo)))
    if nodo.es_hoja() and nodo.dato is not None:
        print(nodo.dato)
        return
    for i, hijo in enumerate(nodo.hijos, 1):
        cantidad = arbol.contar_hojas(hijo)
        print(f"  {i}. {hijo.nombre} ({cantidad} {'canción' if cantidad == 1 else 'canciones'})")
    print("  [número] entrar | [v] volver | [t] ver árbol de esta rama | [b] buscar nodo | [0] salir")


def explorar_categorias(arbol):
    actual = arbol.raiz
    while True:
        mostrar_nivel(arbol, actual)
        if actual.es_hoja() and actual.dato is not None:
            actual = actual.padre
            continue
        opcion = input("Explorar: ").strip().lower()
        if opcion == "0":
            return
        if opcion == "v":
            if actual.padre is not None:
                actual = actual.padre
            else:
                print("Ya estás en la raíz.")
        elif opcion == "t":
            print(arbol.a_texto(actual))
        elif opcion == "b":
            texto = input("Nombre (o parte) a buscar: ")
            coincidencias = arbol.buscar_todos(texto) if texto.strip() else []
            if not coincidencias:
                print("No se encontró ningún nodo.")
                continue
            for i, n in enumerate(coincidencias, 1):
                print(f"  {i}. {' > '.join(arbol.camino(n))}")
            eleccion = input("Ir a (número, Enter para cancelar): ").strip()
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(coincidencias):
                actual = coincidencias[int(eleccion) - 1]
        elif opcion.isdigit() and 1 <= int(opcion) <= len(actual.hijos):
            actual = actual.hijos[int(opcion) - 1]
        else:
            print("Opción inválida.")


def main():
    canciones = cargar_datos()
    indice_titulo, indice_artista = construir_indices(canciones)
    arbol_categorias = construir_catalogo(canciones)
    print(f"Catálogo cargado: {len(canciones)} canciones | "
          f"altura AVL de títulos: {indice_titulo.altura()} | "
          f"rotaciones realizadas: {indice_titulo.total_rotaciones()}")

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
        elif opcion == "0":
            print("¡Gracias por usar SoundNode!")
            break


if __name__ == "__main__":
    main()
