"""Max-heap binario propio: mayor puntuación, primero.

Los empates conservan el orden de inserción. No usa heapq ni sorted.
"""


class MaxHeap:
    def __init__(self):
        self._datos = []
        self._orden = 0

    def __len__(self):
        return len(self._datos)

    def esta_vacio(self):
        return not self._datos

    def insertar(self, valor, prioridad):
        # El contador evita comparar los objetos Cancion en los empates.
        entrada = (prioridad, -self._orden, valor)
        self._orden += 1
        self._datos.append(entrada)
        actual = len(self._datos) - 1
        while actual > 0:
            padre = (actual - 1) // 2
            if self._datos[padre][:2] >= self._datos[actual][:2]:
                break
            self._datos[padre], self._datos[actual] = self._datos[actual], self._datos[padre]
            actual = padre

    def ver_maximo(self):
        if self.esta_vacio():
            raise IndexError("El heap está vacío")
        return self._datos[0][2]

    def extraer_maximo(self):
        maximo = self.ver_maximo()
        ultimo = self._datos.pop()
        if self._datos:
            self._datos[0] = ultimo
            actual = 0
            while True:
                mayor = actual
                for hijo in (2 * actual + 1, 2 * actual + 2):
                    if hijo < len(self._datos) and self._datos[hijo][:2] > self._datos[mayor][:2]:
                        mayor = hijo
                if mayor == actual:
                    break
                self._datos[actual], self._datos[mayor] = self._datos[mayor], self._datos[actual]
                actual = mayor
        return maximo


def top_canciones(canciones, cantidad=5):
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa")
    heap = MaxHeap()
    for cancion in canciones:
        heap.insertar(cancion, cancion.puntuacion)
    return [heap.extraer_maximo() for _ in range(min(cantidad, len(heap)))]
