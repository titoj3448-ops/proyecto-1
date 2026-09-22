import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.arbol_binario import ArbolBST
from modelos.cancion import Cancion

def main():
    arbol = ArbolBST()
    
    datos = [
        Cancion("Matrix", "OST", "Soundtrack", "2:30", 9.0),
        Cancion("Inception", "Hans Zimmer", "Soundtrack", "4:22", 8.8),
        Cancion("Titanic", "Celine Dion", "Pop", "4:40", 7.8),
        Cancion("Blade Runner", "Vangelis", "Electronic", "3:40", 8.5),
        Cancion("Arrival", "Max Richter", "Ambient", "3:10", 8.4)
    ]
    
    for c in datos:
        arbol.insertar(c.titulo.lower(), c)
        
    print("Altura del árbol:", arbol.altura())
    
    print("\n--- inorder (ordenado alfabéticamente) ---")
    for e in arbol.inorder(datos=True):
        print(" ", e)
        
    print("\n--- búsquedas ---")
    encontrado = arbol.buscar("matrix")
    print("Buscar 'matrix':", encontrado)
    
    no_encontrado = arbol.buscar("zzz")
    print("Buscar 'zzz':", no_encontrado)

if __name__ == "__main__":
    main()