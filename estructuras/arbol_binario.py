class Nodo:
    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = clave if valor is None else valor
        self.izquierda = None
        self.derecha = None

    def __repr__(self):
        return f"Nodo({self.clave!r})"


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None
        self._tamanio = 0
        self.comparaciones = 0

    def insertar(self, clave, valor=None):
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

    def buscar_nodo(self, clave):
        self.comparaciones = 0
        actual = self.raiz
        while actual is not None:
            self.comparaciones += 1
            if clave == actual.clave:
                return actual
            actual = actual.izquierda if clave < actual.clave else actual.derecha
        return None

    def buscar(self, clave):
        nodo = self.buscar_nodo(clave)
        return nodo.valor if nodo else None

    def insertar_multiple(self, clave, valor):
        nodo = self.buscar_nodo(clave)
        if nodo is not None:
            nodo.valor.append(valor)
            return nodo
        return self.insertar(clave, [valor])

    def buscar_por_prefijo(self, prefijo):
        resultado = []
        self._buscar_prefijo_rec(self.raiz, prefijo, resultado)
        return resultado

    def _buscar_prefijo_rec(self, nodo, prefijo, resultado):
        if nodo is None:
            return

        if nodo.clave >= prefijo:
            self._buscar_prefijo_rec(nodo.izquierda, prefijo, resultado)

        if nodo.clave.startswith(prefijo):
            if isinstance(nodo.valor, list):
                resultado.extend(nodo.valor)
            else:
                resultado.append(nodo.valor)

            self._buscar_prefijo_rec(nodo.derecha, prefijo, resultado)
        elif nodo.clave < prefijo:
            self._buscar_prefijo_rec(nodo.derecha, prefijo, resultado)

    def inorder(self, datos=False):
        resultado = []
        self._inorder_rec(self.raiz, datos, resultado)
        return resultado

    def _inorder_rec(self, nodo, datos, resultado):
        if nodo is not None:
            self._inorder_rec(nodo.izquierda, datos, resultado)
            resultado.append(nodo.valor if datos else nodo.clave)
            self._inorder_rec(nodo.derecha, datos, resultado)

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierda), self._altura_rec(nodo.derecha))

    def esta_vacio(self):
        return self.raiz is None

    def __len__(self):
        return self._tamanio

    def __contains__(self, clave):
        return self.buscar_nodo(clave) is not None

# Alias para mantener compatibilidad con las pruebas
ArbolBST = ArbolBinarioBusqueda