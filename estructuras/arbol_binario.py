"""Árbol Binario de Búsqueda (BST) - TP3.

Cada nodo guarda un par (clave, valor):
    - clave: lo que se compara y ordena (id, dni, nombre, etc.)
    - valor: el dato completo asociado (dict, objeto, etc.)

Si no se pasa valor, el valor es la propia clave.
"""


class Nodo:
    __slots__ = ("clave", "valor", "izquierda", "derecha")

    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = clave if valor is None else valor
        self.izquierda = None
        self.derecha = None

    def __repr__(self):
        return f"Nodo({self.clave!r})"


class ArbolBinarioBusqueda:
    """BST con inserción y búsqueda iterativas y tres recorridos."""

    def __init__(self):
        self.raiz = None
        self._tamanio = 0
        self.comparaciones = 0  # contador de la última operación

    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------
    def insertar(self, clave, valor=None):
        """Inserta la clave. Si ya existe, actualiza el valor."""
        nuevo = Nodo(clave, valor)

        if self.raiz is None:
            self.raiz = nuevo
            self._tamanio += 1
            return nuevo

        actual = self.raiz
        while True:
            if clave == actual.clave:
                actual.valor = nuevo.valor
                return actual
            if clave < actual.clave:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    self._tamanio += 1
                    return nuevo
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    self._tamanio += 1
                    return nuevo
                actual = actual.derecha

    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
    def buscar_nodo(self, clave):
        """Devuelve el Nodo con esa clave, o None. Cuenta comparaciones."""
        self.comparaciones = 0
        actual = self.raiz
        while actual is not None:
            self.comparaciones += 1
            if clave == actual.clave:
                return actual
            actual = actual.izquierda if clave < actual.clave else actual.derecha
        return None

    def buscar(self, clave):
        """Devuelve el valor asociado a la clave, o None si no está."""
        nodo = self.buscar_nodo(clave)
        return nodo.valor if nodo else None


    def insertar_multiple(self, clave, valor):
        """Inserta permitiendo claves repetidas: el valor del nodo es una lista.

        Sirve cuando dos canciones comparten título, o un artista tiene varias
        canciones. No recorre la lista: baja por el árbol en O(log n).
        """
        nodo = self.buscar_nodo(clave)
        if nodo is not None:
            nodo.valor.append(valor)
            return nodo
        return self.insertar(clave, [valor])

    def buscar_por_prefijo(self, prefijo):
        """Devuelve los valores de todas las claves que empiezan con `prefijo`.

        Recorre solo las ramas que pueden contener coincidencias: si la clave del
        nodo es menor que el prefijo, todo su subárbol izquierdo se descarta.
        Costo O(log n + k), con k = cantidad de resultados.
        """
        resultado = []
        tope = prefijo + "\uffff"

        def _rec(nodo):
            if nodo is None:
                return
            if nodo.clave >= prefijo:
                _rec(nodo.izquierda)
            if nodo.clave.startswith(prefijo):
                valor = nodo.valor
                resultado.extend(valor) if isinstance(valor, list) else resultado.append(valor)
            if nodo.clave <= tope:
                _rec(nodo.derecha)

        _rec(self.raiz)
        return resultado

    # ------------------------------------------------------------------
    # Recorridos (devuelven listas de claves, o de nodos si datos=True)
    # ------------------------------------------------------------------
    def inorder(self, datos=False):
        """Izquierda - Raíz - Derecha  ->  claves ordenadas de menor a mayor."""
        resultado = []

        def _rec(nodo):
            if nodo is None:
                return
            _rec(nodo.izquierda)
            resultado.append(nodo.valor if datos else nodo.clave)
            _rec(nodo.derecha)

        _rec(self.raiz)
        return resultado

    def preorder(self, datos=False):
        """Raíz - Izquierda - Derecha  ->  sirve para copiar/serializar el árbol."""
        resultado = []

        def _rec(nodo):
            if nodo is None:
                return
            resultado.append(nodo.valor if datos else nodo.clave)
            _rec(nodo.izquierda)
            _rec(nodo.derecha)

        _rec(self.raiz)
        return resultado

    def postorder(self, datos=False):
        """Izquierda - Derecha - Raíz  ->  sirve para liberar/borrar el árbol."""
        resultado = []

        def _rec(nodo):
            if nodo is None:
                return
            _rec(nodo.izquierda)
            _rec(nodo.derecha)
            resultado.append(nodo.valor if datos else nodo.clave)

        _rec(self.raiz)
        return resultado

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def altura(self, nodo="__raiz__"):
        """Altura del árbol (árbol vacío = 0)."""
        if nodo == "__raiz__":
            nodo = self.raiz
        if nodo is None:
            return 0
        return 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def esta_vacio(self):
        return self.raiz is None

    def __len__(self):
        return self._tamanio

    def __contains__(self, clave):
        return self.buscar_nodo(clave) is not None


def construir_desde(elementos, clave_func=None):
    """Arma un BST a partir de una lista.

    clave_func: función que extrae la clave de cada elemento.
                Ej: lambda p: p["id"]   o   lambda p: p.nombre.lower()
    """
    arbol = ArbolBinarioBusqueda()
    for elemento in elementos:
        clave = elemento if clave_func is None else clave_func(elemento)
        arbol.insertar(clave, elemento)
    return arbol
