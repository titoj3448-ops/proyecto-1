import json
import sys
import os

# Agrega la carpeta raíz al path de Python para encontrar 'modelos'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modelos.cancion import Cancion
from estructuras.arbol_binario import ArbolBinarioBusqueda


def normalizar(texto):
    """Clave canónica: sin espacios sobrantes y en minúsculas."""
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
    """Arma los dos BST una sola vez, al iniciar la aplicación.

    Se usa insertar_multiple porque puede haber títulos repetidos y, sobre todo,
    varios temas del mismo artista: cada nodo guarda una lista de canciones.
    """
    indice_titulo = ArbolBinarioBusqueda()
    indice_artista = ArbolBinarioBusqueda()
    for c in canciones:
        indice_titulo.insertar_multiple(normalizar(c.titulo), c)
        indice_artista.insertar_multiple(normalizar(c.artista), c)
    return indice_titulo, indice_artista


def mostrar_menu():
    print("=" * 40)
    print("      🎵 SOUNDNODE — CATÁLOGO MUSICAL 🎵")
    print("=" * 40)
    print("1. Buscar canción por título")
    print("2. Buscar canción por artista")
    print("3. Ver todo el catálogo de canciones")
    print("4. Filtrar por género musical")
    print("0. Salir")
    print("-" * 40)


def buscar_titulo(indice_titulo):
    """Búsqueda por título usando el árbol binario (no recorre la lista)."""
    texto = normalizar(input("Título de la canción a buscar: "))
    if not texto:
        print("No ingresaste ningún título.")
        return

    # 1) coincidencia exacta: baja por el árbol, O(log n)
    exacto = indice_titulo.buscar(texto)
    comparaciones = indice_titulo.comparaciones

    if exacto:
        for c in exacto:
            print(c)
        print(f"(encontrado en {comparaciones} comparaciones)")
    else:
        # 2) si no hay exacta, se buscan los títulos que empiezan con ese texto,
        #    podando las ramas del árbol que no pueden contener coincidencias
        parciales = indice_titulo.buscar_por_prefijo(texto)
        if parciales:
            for c in parciales:
                print(c)
        else:
            print("No se encontraron canciones con ese título.")
    print("Fin de resultados.")


def buscar_artista(indice_artista):
    """Búsqueda por artista usando el árbol binario."""
    texto = normalizar(input("Nombre del artista o banda: "))
    if not texto:
        print("No ingresaste ningún artista.")
        return

    resultados = indice_artista.buscar(texto) or indice_artista.buscar_por_prefijo(texto)
    if resultados:
        for c in resultados:
            print(c)
    else:
        print("No se encontraron canciones de ese artista.")
    print("Fin de resultados.")


def listar(indice_titulo):
    """El recorrido inorder devuelve el catálogo ordenado por título."""
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


def main():
    canciones = cargar_datos()
    indice_titulo, indice_artista = construir_indices(canciones)
    print(f"Catálogo cargado: {len(canciones)} canciones | "
          f"altura del árbol de títulos: {indice_titulo.altura()}")

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
        elif opcion == "0":
            print("¡Gracias por usar SoundNode!")
            break


if __name__ == "__main__":
    main()