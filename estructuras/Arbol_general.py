from collections import deque

CATEGORIAS = {
    "Pop y Electrónica": ["Pop", "Synth-pop"],
    "Rock y Derivados": ["Rock", "Grunge", "Rock argentino"],
    "Jazz y Blues": ["Jazz", "Blues"],
    "Caribe y Relajante": ["Relajante", "Salsa"],
}


class NodoGeneral:
    __slots__ = ("nombre", "dato", "hijos", "padre")

    def __init__(self, nombre, dato=None):
        self.nombre = nombre
        self.dato = dato
        self.hijos = []
        self.padre = None

    def es_hoja(self):
        return not self.hijos

    def __repr__(self):
        return f"NodoGeneral({self.nombre!r}, hijos={len(self.hijos)})"


class ArbolGeneral:
    def __init__(self):
        self.raiz = None

    def insertar_raiz(self, nombre, dato=None):
        if self.raiz is not None:
            raise ValueError("El árbol ya tiene raíz")
        self.raiz = NodoGeneral(nombre, dato)
        return self.raiz

    def agregar_hijo(self, nombre_padre, nombre, dato=None):
        padre = self.buscar(nombre_padre)
        if padre is None:
            raise KeyError(f"No existe el nodo padre {nombre_padre!r}")
        return self.agregar_hijo_a(padre, nombre, dato)

    def agregar_hijo_a(self, padre, nombre, dato=None):
        for hermano in padre.hijos:
            if hermano.nombre.lower() == nombre.lower():
                raise ValueError(f"{padre.nombre!r} ya tiene un hijo llamado {nombre!r}")
        hijo = NodoGeneral(nombre, dato)
        hijo.padre = padre
        padre.hijos.append(hijo)
        return hijo

    def hijo_por_nombre(self, padre, nombre):
        for hijo in padre.hijos:
            if hijo.nombre.lower() == nombre.lower():
                return hijo
        return None

    def recorrido_amplitud(self):
        resultado = []
        if self.raiz is None:
            return resultado
        cola = deque([(self.raiz, 0)])
        while cola:
            nodo, nivel = cola.popleft()
            resultado.append((nodo, nivel))
            for hijo in nodo.hijos:
                cola.append((hijo, nivel + 1))
        return resultado

    def recorrido_profundidad(self):
        resultado = []
        if self.raiz is None:
            return resultado
        pila = [(self.raiz, 0)]
        while pila:
            nodo, nivel = pila.pop()
            resultado.append((nodo, nivel))
            for hijo in reversed(nodo.hijos):
                pila.append((hijo, nivel + 1))
        return resultado

    def recorrido_postorden(self):
        resultado = []

        def _rec(nodo, nivel):
            for hijo in nodo.hijos:
                _rec(hijo, nivel + 1)
            resultado.append((nodo, nivel))

        if self.raiz is not None:
            _rec(self.raiz, 0)
        return resultado

    def buscar(self, nombre):
        objetivo = nombre.strip().lower()
        if self.raiz is None:
            return None
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            if nodo.nombre.lower() == objetivo:
                return nodo
            cola.extend(nodo.hijos)
        return None

    def buscar_profundidad(self, nombre):
        objetivo = nombre.strip().lower()
        if self.raiz is None:
            return None
        pila = [self.raiz]
        while pila:
            nodo = pila.pop()
            if nodo.nombre.lower() == objetivo:
                return nodo
            pila.extend(reversed(nodo.hijos))
        return None

    def buscar_todos(self, texto):
        objetivo = texto.strip().lower()
        return [n for n, _ in self.recorrido_amplitud() if objetivo in n.nombre.lower()]

    def camino(self, nodo):
        ruta = []
        while nodo is not None:
            ruta.append(nodo.nombre)
            nodo = nodo.padre
        return list(reversed(ruta))

    def contar_hojas(self, nodo=None):
        nodo = nodo or self.raiz
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        return sum(self.contar_hojas(h) for h in nodo.hijos)

    def tamanio(self):
        return len(self.recorrido_amplitud())

    def altura(self):
        if self.raiz is None:
            return 0
        return 1 + max(nivel for _, nivel in self.recorrido_amplitud())

    def grado_maximo(self):
        return max((len(n.hijos) for n, _ in self.recorrido_amplitud()), default=0)

    def a_texto(self, nodo=None, solo_categorias=False):
        nodo = nodo or self.raiz
        lineas = []
        if nodo is None:
            return ""
        pila = [(nodo, 0)]
        while pila:
            actual, nivel = pila.pop()
            if solo_categorias and actual.es_hoja() and actual.dato is not None and nivel > 0:
                continue
            lineas.append("    " * nivel + ("└─ " if nivel else "") + actual.nombre)
            for hijo in reversed(actual.hijos):
                pila.append((hijo, nivel + 1))
        return "\n".join(lineas)


def construir_catalogo(canciones, nombre_raiz="Catálogo", categorias=None):
    categorias = CATEGORIAS if categorias is None else categorias
    macro_de = {}
    for macro, generos in categorias.items():
        for g in generos:
            macro_de[g.lower()] = macro

    arbol = ArbolGeneral()
    raiz = arbol.insertar_raiz(nombre_raiz)

    for c in canciones:
        macro = macro_de.get(c.genero.lower(), "Otros")
        nodo_macro = arbol.hijo_por_nombre(raiz, macro) or arbol.agregar_hijo_a(raiz, macro)
        nodo_genero = arbol.hijo_por_nombre(nodo_macro, c.genero) or arbol.agregar_hijo_a(nodo_macro, c.genero)
        nodo_artista = arbol.hijo_por_nombre(nodo_genero, c.artista) or arbol.agregar_hijo_a(nodo_genero, c.artista)
        try:
            arbol.agregar_hijo_a(nodo_artista, c.titulo, c)
        except ValueError:
            pass
    return arbol
