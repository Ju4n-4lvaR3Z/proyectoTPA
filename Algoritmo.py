

class ArbolBinario:
   
    def __init__(self,Elemento):
        # Stores the root of the tree
        self.raiz = None
        # Links to the left and right children
        self.hi = None
        self.hd = None
        self.aux = None
        self.Elemento=Elemento
        self.volcado = []
        self.hojas = []
        self.grado = []
        self.cola = []
        self.colaAux = []

# Crea un árbol con solo la raíz si no es nula. Si es nulo, cree un árbol vacío en el que ambos hijos sean árboles vacíos.
    def ArbolBinario(self,ob):
        self.__init__()
        raiz = ob
        if raiz is not None:
            hi = hd = ArbolBinario()

# Nota: Python no tiene tipos explícitos como Java, por lo que '<Elemento>' no es necesario en el código Python.
    def construir(left_tree, root, right_tree,BinaryTree):
    # Si la raíz es nula, crea un árbol vacío.
        if root is None:
            root = None
            right = left = None
        else:
            root = root
        # Si algún hijo es nulo, establezca un árbol vacío.
        if left_tree is None:
            left = BinaryTree()
        else:
            left = left_tree
        if right_tree is None:
            right = BinaryTree()
        else:
            right = right_tree
# This code is written in Java

# Construye un arbol con solo la raiz y las consideraciones anteriores
    def construir(self, ob,Elemento):
        self.construir(ArbolBinario<Elemento>(), ob, ArbolBinario<Elemento>())

# Construye un arbol vacio
    def construir(self):
        self.raiz = None
        self.hi = None
        self.hd = None

# Devuelve la raiz o None si es vacio
    def raiz(self):
     return self.raiz

# Devuelve el hijo izquierdo o None si es vacio
    def hi(self):
        return self.hi

# Devuelve el hijo derecho o None si es vacio
    def hd(self):
        return self.hd

# Decide si el arbol esta vacio; falso en caso contrario
    def esVacio(self):
        return self.raiz == None
# Framework/Technology Stack: N/A

# OTRAS OPERACIONES

# Muestra el arbol
    def __str__(self):
        return "\n" + self.__str__(0)

# Muestra el arbol con una sangría de espacios
# y un recorrido "raiz-izquierda-derecha"
    def __str__(self, espacios):
        linea = ""
        for x in range(espacios+1):
         linea += " "
    
        if self.esVacio():
         linea += "vacio" + self.__class__
        else:
            linea += self.raiz().__str__() + self.__class__
        if not self.esHoja():
            linea += "\n  " + self.hi().__str__(espacios+2)
            linea += "\n  " + self.hd().__str__(espacios+2)
    
        return linea
# True si es hoja, false si no lo es  
    def es_hoja(self):
     return not self.es_vacio() and self.hi().es_vacio() and self.hd().es_vacio()

# True si dos árboles son iguales, false en caso contrario  
    def equals(self, arbol,):
        igual = False
        if isinstance(arbol, ArbolBinario):
            a = arbol
        igual = a == self or (self.es_vacio() and a.es_vacio())
        if not igual:
            if (not self.es_vacio() and a.es_vacio()) or (self.es_vacio() and not a.es_vacio()):
                igual = False
            else:  # ninguno es vacio
                igual = a.raiz().equals(self.raiz()) and a.hi().equals(self.hi()) and a.hd().equals(self.hd())
        return igual

# Devuelve la altura: longitud de la rama mas larga  
    def altura(self):
        i = 0
        if not self.es_vacio():
            i = max(self.hd().altura(), self.hi().altura()) + 1
        return i

# Devuelve la prundidad: longitud desde la raiz hasta el elemento parámetro
# es el nivel. La raiz tiene nivel 0  
    def profundidad(self, a):
        prof = -1
        if not self.es_vacio():
            if self.raiz().equals(a):
                prof = 0
            else:
                prof = self.hi().profundidad(a)
                if prof != -1:
                    prof += 1
                else:
                    prof = self.hd().profundidad(a)
                    if prof != -1:
                        prof += 1
        return prof
# Devuelve la profundidad: longitud desde la raíz hasta el árbol de parámetros
# es el nivel. La raíz tiene nivel 0.
    def profundidad(self,arbol,esVacio,hd,hi):
        prof = -1
        if not esVacio():
            if self.equals(arbol):
                prof = 0
            else:
                prof = hi().profundidad(arbol)
            if prof != -1:
                prof += 1
            else:
                prof = hd().profundidad(arbol)
                if prof != -1:
                    prof += 1
        return prof

# Devuelve el primer árbol, con un recorrido "raíz-izquierda-derecha",
# que tiene el elemento parámetro como raíz
# Si no se encuentra, devuelve un árbol vacío
    def localiza(self,raiz,ob,esVacio,hd,hi):
        aux = ArbolBinario()
        if not esVacio():
            if raiz().equals(ob):
                aux = self
            else:
                aux = hi().localiza(ob)
                if aux.esVacio():
                    aux = hd().localiza(ob)
        return aux    
   # Verdadero si el elemento pertenece, falso de lo contrario
    def pertenece(self, elemento):
        return not self.localiza(elemento).esVacio()

# Devuelve el primer árbol, con un recorrido "raíz-izquierda-derecha",
# que tiene el elemento parámetro como hijo
# Si no se encuentra, devuelve un árbol vacío
    def padre(self, ob):
        aux = ArbolBinario()
        if not self.esVacio():
            if ((not self.hi().esVacio()) and (ob == self.hi().raiz())) or ((not self.hd().esVacio()) and (ob == self.hd().raiz())):
                aux = self
        else:
            aux = self.hi().padre(ob)
            if aux.esVacio():
                aux = self.hd().padre(ob)
        return aux