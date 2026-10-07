class NodoAVL:
    """Nodo del AVL: igual que el Nodo del BST pero guarda su altura."""

    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = clave if valor is None else valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # un nodo hoja tiene altura 1

    def __repr__(self):
        return f"NodoAVL({self.clave!r}, h={self.altura})"


class AVL:
    """
    Árbol binario de búsqueda auto-balanceado.

    Mantiene la misma interfaz que ArbolBinarioBusqueda (insertar, buscar,
    insertar_multiple, buscar_por_prefijo, inorder, altura, comparaciones),
    de modo que puede reemplazarlo sin tocar el resto del programa.
    """

    def __init__(self):
        self.raiz = None
        self._tamanio = 0
        self.comparaciones = 0
        # Contador de rotaciones por tipo (sirve como evidencia en las pruebas)
        self.rotaciones = {
            "simple_derecha": 0,       # caso Izquierda-Izquierda
            "simple_izquierda": 0,     # caso Derecha-Derecha
            "izquierda_derecha": 0,    # caso Izquierda-Derecha (doble)
            "derecha_izquierda": 0,    # caso Derecha-Izquierda (doble)
        }

    # ------------------------------------------------------------------
    # Utilidades de altura y balance
    # ------------------------------------------------------------------
    def _altura_nodo(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura_nodo(nodo.izquierda),
                              self._altura_nodo(nodo.derecha))

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura_nodo(nodo.izquierda) - self._altura_nodo(nodo.derecha)

    # ------------------------------------------------------------------
    # Rotaciones
    # ------------------------------------------------------------------
    def _rotacion_derecha(self, y):
        #       y                x
        #      / \              / \
        #     x   C    ==>     A   y
        #    / \                  / \
        #   A   B                B   C
        x = y.izquierda
        y.izquierda = x.derecha
        x.derecha = y
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotacion_izquierda(self, x):
        #     x                    y
        #    / \                  / \
        #   A   y      ==>       x   C
        #      / \              / \
        #     B   C            A   B
        y = x.derecha
        x.derecha = y.izquierda
        y.izquierda = x
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _rotacion_izquierda_derecha(self, nodo):
        nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
        return self._rotacion_derecha(nodo)

    def _rotacion_derecha_izquierda(self, nodo):
        nodo.derecha = self._rotacion_derecha(nodo.derecha)
        return self._rotacion_izquierda(nodo)

    def _balancear(self, nodo):
        self._actualizar_altura(nodo)
        factor = self._factor_balance(nodo)

        if factor > 1:  # pesa de más a la izquierda
            if self._factor_balance(nodo.izquierda) < 0:
                self.rotaciones["izquierda_derecha"] += 1
                return self._rotacion_izquierda_derecha(nodo)
            self.rotaciones["simple_derecha"] += 1
            return self._rotacion_derecha(nodo)

        if factor < -1:  # pesa de más a la derecha
            if self._factor_balance(nodo.derecha) > 0:
                self.rotaciones["derecha_izquierda"] += 1
                return self._rotacion_derecha_izquierda(nodo)
            self.rotaciones["simple_izquierda"] += 1
            return self._rotacion_izquierda(nodo)

        return nodo

    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------
    def insertar(self, clave, valor=None):
        self.raiz = self._insertar_rec(self.raiz, clave, valor)

    def _insertar_rec(self, nodo, clave, valor):
        if nodo is None:
            self._tamanio += 1
            return NodoAVL(clave, valor)

        if clave == nodo.clave:
            nodo.valor = clave if valor is None else valor
            return nodo
        if clave < nodo.clave:
            nodo.izquierda = self._insertar_rec(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._insertar_rec(nodo.derecha, clave, valor)

        return self._balancear(nodo)

    def insertar_multiple(self, clave, valor):
        """Igual que en el BST: varias canciones pueden compartir clave."""
        nodo = self.buscar_nodo(clave)
        if nodo is not None:
            nodo.valor.append(valor)
            return nodo
        self.insertar(clave, [valor])
        return self.buscar_nodo(clave)

    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Recorridos y propiedades
    # ------------------------------------------------------------------
    def inorder(self, datos=False):
        resultado = []
        self._inorder_rec(self.raiz, datos, resultado)
        return resultado

    def _inorder_rec(self, nodo, datos, resultado):
        if nodo is not None:
            self._inorder_rec(nodo.izquierda, datos, resultado)
            resultado.append(nodo.valor if datos else nodo.clave)
            self._inorder_rec(nodo.derecha, datos, resultado)

    def preorder(self):
        resultado = []
        self._preorder_rec(self.raiz, resultado)
        return resultado

    def _preorder_rec(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.clave)
            self._preorder_rec(nodo.izquierda, resultado)
            self._preorder_rec(nodo.derecha, resultado)

    def altura(self):
        # O(1): la altura ya está guardada en la raíz
        return self._altura_nodo(self.raiz)

    def esta_balanceado(self):
        """Verifica que TODOS los nodos tengan factor de balance en [-1, 1]."""
        return self._balanceado_rec(self.raiz)

    def _balanceado_rec(self, nodo):
        if nodo is None:
            return True
        if abs(self._factor_balance(nodo)) > 1:
            return False
        return self._balanceado_rec(nodo.izquierda) and self._balanceado_rec(nodo.derecha)

    def esta_vacio(self):
        return self.raiz is None

    def __len__(self):
        return self._tamanio

    def __contains__(self, clave):
        return self.buscar_nodo(clave) is not None
