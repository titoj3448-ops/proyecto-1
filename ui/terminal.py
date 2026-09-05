import json
import sys
import os

# Agrega la carpeta raíz al path de Python para encontrar 'modelos'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modelos.cancion import Cancion

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

def buscar_titulo(canciones):
    texto = input("Título de la canción a buscar: ").lower()
    encontrados = False
    for c in canciones:
        if texto in c.titulo.lower():
            print(c)
            encontrados = True
    if not encontrados:
        print("No se encontraron canciones con ese título.")
    print("Fin de resultados.")

def buscar_artista(canciones):
    texto = input("Nombre del artista o banda: ").lower()
    encontrados = False
    for c in canciones:
        if texto in c.artista.lower():
            print(c)
            encontrados = True
    if not encontrados:
        print("No se encontraron canciones de ese artista.")
    print("Fin de resultados.")

def listar(canciones):
    print("\n--- CATÁLOGO COMPLETO ---")
    for i, c in enumerate(canciones, 1):
        print(f"{i}. {c}")

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
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()
        if opcion == "1":
            buscar_titulo(canciones)
        elif opcion == "2":
            buscar_artista(canciones)
        elif opcion == "3":
            listar(canciones)
        elif opcion == "4":
            filtrar(canciones)
        elif opcion == "0":
            print("¡Gracias por usar SoundNode!")
            break

if __name__ == "__main__":
    main()
