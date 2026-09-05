import json
from cancion import Cancion
from catalogo import Catalogo

def cargar_catalogo_desde_json(ruta_archivo="canciones.json"):
    catalogo = Catalogo()
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for item in datos:
                cancion = Cancion(
                    id_cancion=item["id"],
                    titulo=item["titulo"],
                    artista=item["artista"],
                    genero=item["genero"],
                    duracion=item["duracion"],
                    puntuacion=item["puntuacion"]
                )
                catalogo.agregar_cancion(cancion)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
    return catalogo

def menu():
    catalogo = cargar_catalogo_desde_json()
    
    while True:
        print("\n========================================")
        print("      🎵 SOUNDNODE — CATALOGO 🎵")
        print("========================================")
        print("1. Listar todas las canciones")
        print("2. Buscar por título o artista")
        print("3. Filtrar por género")
        print("4. Ver Top canciones mejor puntuadas")
        print("0. Salir")
        print("----------------------------------------")
        
        opcion = input("Opción: ").strip()

        if opcion == "1":
            print("\n--- TODAS LAS CANCIONES ---")
            for c in catalogo.obtener_todas():
                print(c)

        elif opcion == "2":
            query = input("\nIngrese título o artista a buscar: ")
            resultados = catalogo.buscar(query)
            print(f"\n--- Resultados ({len(resultados)}) ---")
            for c in resultados:
                print(c)

        elif opcion == "3":
            genero = input("\nIngrese género (ej: Rock argentino, Pop, Synth-pop): ")
            resultados = catalogo.filtrar_por_genero(genero)
            print(f"\n--- Canciones de {genero} ({len(resultados)}) ---")
            for c in resultados:
                print(c)

        elif opcion == "4":
            print("\n--- TOP CANCIONES MEJOR PUNTUADAS ---")
            for c in catalogo.obtener_top_puntuadas(5):
                print(c)

        elif opcion == "0":
            print("\n¡Gracias por usar SoundNode!")
            break

        else:
            print("\nOpción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()