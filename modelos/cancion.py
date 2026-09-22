class Cancion:
    def __init__(self, titulo, artista, genero, duracion="N/A", puntuacion=0.0):
        self._titulo = titulo
        self._artista = artista
        self._genero = genero
        self._duracion = duracion
        self._puntuacion = puntuacion

    def __str__(self):
        titulo_limpio = self._titulo.strip("'")
        return f"'{titulo_limpio}' - {self._artista} ({self._genero}) [{self._duracion}] ⭐{self._puntuacion}"

    def __repr__(self):
        return f"Cancion({self._titulo!r}, {self._artista!r})"

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        return self._artista

    @property
    def genero(self):
        return self._genero

    @property
    def duracion(self):
        return self._duracion

    @property
    def puntuacion(self):
        return self._puntuacion