class Arreglo:

    def __init__(self):
        self.elementos = []

    def agregar(self, elemento):
        self.elementos.append(elemento)

    def eliminar(self, index):
        if 0 <= index < len(self.elementos):
            del self.elementos[index]

    def editar(self, index, nuevo_elemento):
        if 0 <= index < len(self.elementos):
            self.elementos[index] = nuevo_elemento

    def obtener_elementos(self):
        return self.elementos

    def __len__(self):
        return len(self.elementos)

    def __repr__(self):
        return str(self.elementos)

    def __iter__(self):
        return iter(self.elementos)

    def mostrar_elementos(self):
        return str(self.elementos)
