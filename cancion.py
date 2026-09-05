class Cancion:
    def __init__(self, id_cancion: int, titulo: str, artista: str, genero: str, duracion: str, puntuacion: float):
        self._id = id_cancion
        self._titulo = titulo
        self._artista = artista
        self._genero = genero
        self._duracion = duracion
        self._puntuacion = puntuacion

    @property
    def id(self):
        return self._id

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

    def __repr__(self):
        return f"[{self._id:02d}] '{self._titulo}' - {self._artista} ({self._genero}) ⭐{self._puntuacion}"