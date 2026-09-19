"""Comparación de tiempos reales: secuencial vs binaria vs árbol (TP3).

Es la versión del script de medición del TP2 con la columna "árbol" agregada.
Uso:  python algoritmos/comparar_busquedas.py
"""

import os
import random
import sys
from time import perf_counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estructuras.arbol_binario import ArbolBinarioBusqueda

TAMANIOS = [100, 1_000, 10_000, 100_000]
REPETICIONES = 500  # cantidad de búsquedas por medición


# ----------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------
def busqueda_secuencial(lista, objetivo):
    for i, valor in enumerate(lista):
        if valor == objetivo:
            return i
    return -1


def busqueda_binaria(lista, objetivo):
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == objetivo:
            return medio
        if lista[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


# ----------------------------------------------------------------------
# Medición
# ----------------------------------------------------------------------
def medir(funcion, objetivos):
    inicio = perf_counter()
    for objetivo in objetivos:
        funcion(objetivo)
    return (perf_counter() - inicio) / len(objetivos) * 1_000_000  # microsegundos


def main():
    random.seed(42)
    print(f"{REPETICIONES} búsquedas por caso. Tiempos en microsegundos (µs) por búsqueda.\n")

    cabecera = f"| {'N':>7} | {'Secuencial':>12} | {'Binaria':>10} | {'Árbol':>10} | {'Altura':>6} |"
    print(cabecera)
    print("|" + "-" * 9 + "|" + "-" * 14 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 8 + "|")

    for n in TAMANIOS:
        lista_ordenada = list(range(n))

        # el árbol se arma con los datos mezclados para que quede balanceado
        mezclados = lista_ordenada[:]
        random.shuffle(mezclados)
        arbol = ArbolBinarioBusqueda()
        for clave in mezclados:
            arbol.insertar(clave)

        objetivos = [random.randrange(n) for _ in range(REPETICIONES)]

        t_sec = medir(lambda o: busqueda_secuencial(lista_ordenada, o), objetivos)
        t_bin = medir(lambda o: busqueda_binaria(lista_ordenada, o), objetivos)
        t_arb = medir(arbol.buscar, objetivos)

        print(f"| {n:>7} | {t_sec:>12.2f} | {t_bin:>10.2f} | "
              f"{t_arb:>10.2f} | {arbol.altura():>6} |")

    print("\nNota: el tiempo del árbol no incluye la construcción (se arma una sola "
          "vez al iniciar la app).")


if __name__ == "__main__":
    main()
