class NodoAVL:
    __slots__ = ("clave", "valor", "izquierda", "derecha", "altura")

    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = clave if valor is None else valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

    def __repr__(self):
        return f"NodoAVL({self.clave!r}, h={self.altura})"


class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self._tamanio = 0
        self.comparaciones = 0
        self.rotaciones = {
            "simple_derecha": 0,
            "simple_izquierda": 0,
            "doble_izquierda_derecha": 0,
            "doble_derecha_izquierda": 0,
        }

    @staticmethod
    def _h(nodo):
        return nodo.altura if nodo else 0

    def _actualizar(self, nodo):
        nodo.altura = 1 + max(self._h(nodo.izquierda), self._h(nodo.derecha))

    def factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._h(nodo.izquierda) - self._h(nodo.derecha)

    def _girar_derecha(self, y):
        x = y.izquierda
        y.izquierda = x.derecha
        x.derecha = y
        self._actualizar(y)
        self._actualizar(x)
        return x

    def _girar_izquierda(self, x):
        y = x.derecha
        x.derecha = y.izquierda
        y.izquierda = x
        self._actualizar(x)
        self._actualizar(y)
        return y

    def rotacion_simple_derecha(self, nodo):
        self.rotaciones["simple_derecha"] += 1
        return self._girar_derecha(nodo)

    def rotacion_simple_izquierda(self, nodo):
        self.rotaciones["simple_izquierda"] += 1
        return self._girar_izquierda(nodo)

    def rotacion_doble_izquierda_derecha(self, nodo):
        self.rotaciones["doble_izquierda_derecha"] += 1
        nodo.izquierda = self._girar_izquierda(nodo.izquierda)
        return self._girar_derecha(nodo)

    def rotacion_doble_derecha_izquierda(self, nodo):
        self.rotaciones["doble_derecha_izquierda"] += 1
        nodo.derecha = self._girar_derecha(nodo.derecha)
        return self._girar_izquierda(nodo)

    def total_rotaciones(self):
        return sum(self.rotaciones.values())

    def _rebalancear(self, nodo):
        self._actualizar(nodo)
        balance = self.factor_balance(nodo)

        if balance > 1:
            if self.factor_balance(nodo.izquierda) >= 0:
                return self.rotacion_simple_derecha(nodo)
            return self.rotacion_doble_izquierda_derecha(nodo)

        if balance < -1:
            if self.factor_balance(nodo.derecha) <= 0:
                return self.rotacion_simple_izquierda(nodo)
            return self.rotacion_doble_derecha_izquierda(nodo)

        return nodo

    def insertar(self, clave, valor=None):
        self._ultimo = None
        self.raiz = self._insertar(self.raiz, clave, valor)
        return self._ultimo

    def _insertar(self, nodo, clave, valor):
        if nodo is None:
            nuevo = NodoAVL(clave, valor)
            self._tamanio += 1
            self._ultimo = nuevo
            return nuevo

        if clave == nodo.clave:
            nodo.valor = clave if valor is None else valor
            self._ultimo = nodo
            return nodo

        if clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, valor)

        return self._rebalancear(nodo)

    def insertar_multiple(self, clave, valor):
        nodo = self.buscar_nodo(clave)
        if nodo is not None:
            nodo.valor.append(valor)
            return nodo
        return self.insertar(clave, [valor])

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

    def buscar_por_prefijo(self, prefijo):
        resultado = []
        tope = prefijo + "\uffff"

        def _rec(nodo):
            if nodo is None:
                return
            if nodo.clave >= prefijo:
                _rec(nodo.izquierda)
            if nodo.clave.startswith(prefijo):
                if isinstance(nodo.valor, list):
                    resultado.extend(nodo.valor)
                else:
                    resultado.append(nodo.valor)
            if nodo.clave <= tope:
                _rec(nodo.derecha)

        _rec(self.raiz)
        return resultado

    def inorder(self, datos=False):
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
        resultado = []

        def _rec(nodo):
            if nodo is None:
                return
            _rec(nodo.izquierda)
            _rec(nodo.derecha)
            resultado.append(nodo.valor if datos else nodo.clave)

        _rec(self.raiz)
        return resultado

    def altura(self):
        return self._h(self.raiz)

    def esta_vacio(self):
        return self.raiz is None

    def es_avl_valido(self):
        def _rec(nodo):
            if nodo is None:
                return True, 0, None, None
            ok_i, h_i, min_i, max_i = _rec(nodo.izquierda)
            ok_d, h_d, min_d, max_d = _rec(nodo.derecha)
            if not (ok_i and ok_d):
                return False, 0, None, None
            if max_i is not None and not max_i < nodo.clave:
                return False, 0, None, None
            if min_d is not None and not nodo.clave < min_d:
                return False, 0, None, None
            if abs(h_i - h_d) > 1:
                return False, 0, None, None
            h = 1 + max(h_i, h_d)
            if nodo.altura != h:
                return False, 0, None, None
            minimo = min_i if min_i is not None else nodo.clave
            maximo = max_d if max_d is not None else nodo.clave
            return True, h, minimo, maximo

        return _rec(self.raiz)[0]

    def __len__(self):
        return self._tamanio

    def __contains__(self, clave):
        return self.buscar_nodo(clave) is not None


def construir_avl_desde(elementos, clave_func=None):
    arbol = ArbolAVL()
    for elemento in elementos:
        clave = elemento if clave_func is None else clave_func(elemento)
        arbol.insertar(clave, elemento)
    return arbol
