from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Conexion:
    def __init__(self, db_name = 'UTT',):
        # Conexión al cliente de MongoDB
        self.cliente = MongoClient("mongodb://localhost:27017/")
        self.db = self.cliente[db_name]
        self.coleccion = self.db["Alumnos"]
        self.coleccion_grupos = self.db["Grupos"]
        self.coleccion_carreras = self.db["Carreras"]

    def insertar(self, coleccion, datos):
        if isinstance(datos, dict):
            resultado = coleccion.insert_one(datos)
            return resultado.inserted_id
        elif isinstance(datos, list) and all(isinstance(item, dict) for item in datos):
            resultado = coleccion.insert_many(datos)
            return resultado.inserted_ids
        else:
            raise ValueError("El dato debe ser un diccionario o una lista de diccionarios")

    def findDocument(self, coleccion, query={}):
        if coleccion is None:
            raise ValueError("La coleccion no puede ser None")
        resultado = coleccion.find(query)
        return list(resultado)

    def eliminarTodo(self, coleccion, query={}):
        resultado = coleccion.delete_many(query)
        return resultado.deleted_count

    def actualizar(self, coleccion, query, nuevos_valores):
        try:
            print("Actualizando con los siguientes valores:")
            print(f"Query: {query}")
            print(f"Nuevos valores: {nuevos_valores}")
            coleccion.update_one(query, {"$set": nuevos_valores})
        except Exception as e:
            print(f"Error al actualizar: {e}")

    def ping(self):
        try:
            # Realiza un comando 'ping' para verificar la conexión
            self.cliente.admin.command('ping')
            print("Conexión exitosa a MongoDB.")
            return True
        except ConnectionFailure:
            print("Error: No se pudo conectar a MongoDB.")
            return False


