import json
import sys
import os

# Agregamos la carpeta raíz al path para importar modelos y estructuras
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from modelos.cancion import Cancion
from estructuras.arbol_binario import ArbolBinarioBusqueda


def normalizar(texto):
    return texto.strip().lower()


def cargar_datos():
    ruta_json = os.path.join(BASE_DIR, "datos", "canciones.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    canciones = []
    for d in datos:
        duracion = d.get("duracion", "N/A")
        puntuacion = d.get("puntuacion", 0.0)
        canciones.append(Cancion(d["titulo"], d["artista"], d["genero"], duracion, puntuacion))
    return canciones


def construir_indices(canciones):
    # Armamos los árboles binarios para títulos y artistas
    indice_titulo = ArbolBinarioBusqueda()
    indice_artista = ArbolBinarioBusqueda()

    for c in canciones:
        indice_titulo.insertar_multiple(normalizar(c.titulo), c)
        indice_artista.insertar_multiple(normalizar(c.artista), c)

    return indice_titulo, indice_artista


def mostrar_menu():
    print("\n" + "=" * 40)
    print("      🎵 SOUNDNODE — CATÁLOGO MUSICAL 🎵")
    print("=" * 40)
    print("1. Buscar canción por título")
    print("2. Buscar canción por artista")
    print("3. Ver todo el catálogo de canciones")
    print("4. Filtrar por género musical")
    print("0. Salir")
    print("-" * 40)


def buscar_titulo(indice_titulo):
    texto = normalizar(input("Título de la canción a buscar: "))
    if not texto:
        print("No ingresaste ningún título.")
        return

    # Busco primero coincidencia exacta en el árbol
    exacto = indice_titulo.buscar(texto)
    comparaciones = indice_titulo.comparaciones

    if exacto:
        for c in exacto:
            print(c)
        print(f"(Encontrado en {comparaciones} comparaciones)")
    else:
        # Si no está exacto, busco por prefijo
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
    if not resultados:
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
    genero = input("Género musical (ej: Rock, Pop, Grunge, Jazz): ").lower()
    encontrados = False
    print()
    for c in canciones:
        if genero in c.genero.lower():
            print(c)
            encontrados = True
    if not encontrados:
        print("No se encontraron canciones de ese género.")


def main():
    canciones = cargar_datos()
    indice_titulo, indice_artista = construir_indices(canciones)
    print(f"Catálogo cargado: {len(canciones)} canciones | Altura del árbol: {indice_titulo.altura()}")

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
            print("\n¡Gracias por usar SoundNode!")
            break


if __name__ == "__main__":
    main()