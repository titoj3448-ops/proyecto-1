from cancion import Cancion

class Catalogo:
    def __init__(self):
        self._canciones = []

    def agregar_cancion(self, cancion: Cancion):
        self._canciones.append(cancion)

    def obtener_todas(self):
        return self._canciones

    # Operación 1: Buscar por Título o Artista
    def buscar(self, texto: str):
        texto = texto.lower()
        return [c for c in self._canciones if texto in c.titulo.lower() or texto in c.artista.lower()]

    # Operación 2: Filtrar por Género
    def filtrar_por_genero(self, genero: str):
        genero = genero.lower()
        return [c for c in self._canciones if c.genero.lower() == genero]

    # Operación 3: Listar Top por Puntuación
    def obtener_top_puntuadas(self, limite: int = 5):
        return sorted(self._canciones, key=lambda c: c.puntuacion, reverse=True)[:limite]