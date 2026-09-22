import time
import random
import sys
import os

# Agrega el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.arbol_binario import ArbolBST
from modelos.cancion import Cancion

def busqueda_secuencial(lista, clave):
    for elemento in lista:
        if elemento.titulo.lower() == clave:
            return elemento
    return None

def busqueda_binaria(lista, clave):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        actual = lista[medio].titulo.lower()
        if actual == clave:
            return lista[medio]
        elif actual < clave:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None

def medir_tiempos():
    tamanios = [100, 1000, 10000, 100000]
    
    print(f"{'N Elementos':<12} | {'Secuencial (ms)':<16} | {'Binaria (ms)':<14} | {'Árbol BST (ms)':<14}")
    print("-" * 65)

    for n in tamanios:
        datos = [Cancion(f"Cancion_{i}", f"Artista_{i}", "Genero", "3:00", 8.0) for i in range(n)]
        datos_ordenados = sorted(datos, key=lambda x: x.titulo.lower())
        
        arbol = ArbolBST()
        for c in datos:
            arbol.insertar(c.titulo.lower(), c)
            
        clave_buscar = f"cancion_{n - 1}"

        # 1. Secuencial
        t0 = time.perf_counter()
        busqueda_secuencial(datos, clave_buscar)
        t_sec = (time.perf_counter() - t0) * 1000

        # 2. Binaria
        t0 = time.perf_counter()
        busqueda_binaria(datos_ordenados, clave_buscar)
        t_bin = (time.perf_counter() - t0) * 1000

        # 3. Árbol BST
        t0 = time.perf_counter()
        arbol.buscar(clave_buscar)
        t_bst = (time.perf_counter() - t0) * 1000

        print(f"{n:<12} | {t_sec:<16.4f} | {t_bin:<14.4f} | {t_bst:<14.4f}")

if __name__ == "__main__":
    medir_tiempos()