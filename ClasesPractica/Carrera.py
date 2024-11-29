import json
from Grupo import Grupo
from Alumno import Alumno
from Arreglo import Arreglo

class Carrera(Arreglo):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.alumnos = Alumno()

    def agregar_grupo(self, grupo):
        if isinstance(grupo, Grupo):
            self.agregar(grupo)
        else:
            raise TypeError("Solo se agregan objetos de tipo Grupo")

    def mostrar_carrera(self):
        info_carrera = f"Carrera: {self.nombre}\n"
        info_grupos = "\n".join(grupo1.mostrar_grupo() for grupo1 in self.elementos)
        return info_carrera + info_grupos

    def to_dict(self):
        return {
            "nombre_carrera": self.nombre,
            "grupos": [grupo.to_dict() for grupo in self.elementos]
        }

    def __repr__(self):
        return f"Carrera({self.nombre}, {len(self.elementos)} grupos)"

    def guardar_en_json(self, archivo='carreras.json'):
        carreras_json = [carrera.to_dict() for carrera in self.elementos]
        with open(archivo, 'w') as file:
            json.dump(carreras_json, file, indent=4)

    def leer_json(self, archivo='carreras.json'):  # Asegúrate de usar el mismo archivo
        with open(archivo, 'r') as file:
            leido = json.load(file)
        return self.hacer_objetos_grupo_desde_datos(leido)

    def hacer_objetos_grupo_desde_datos(self, leido):
        carreras = []
        for carrera_datos in leido:
            carrera = Carrera(carrera_datos.get("nombre_carrera"))
            for grupo_datos in carrera_datos.get("grupos", []):
                grupo = Grupo(grupo_datos.get("grupo"))
                
                alumnos_datos = grupo_datos.get("alumnos")
                alumnos = grupo.alumnos.hacer_objetos_alumno_desde_datos(alumnos_datos)

                for alumno in alumnos:
                    grupo.agregar_alumno(alumno)

                carrera.agregar_grupo(grupo)
            carreras.append(carrera)
        return carreras

if __name__ == "__main__":

    alumno1 = Alumno("Daniel", "Sanchez", "Perez", "SAPE30342HGLRDRO9", 41806389)
    alumno2 = Alumno("Ana", "Lopez", "Martinez", "LOMA20422FGTDMN99", 41806400)

    grupo1 = Grupo("Grupo 7A")
    grupo2 = Grupo("Grupo 7B")

    carrera1 = Carrera("Ingenieria en TIC's")
    carrera2 = Carrera("Ingenieria Mecatrónica")

    lista_carreras = Carrera("Lista de Carreras")
    lista_carreras.agregar(carrera1)
    lista_carreras.agregar(carrera2)

    grupo1.agregar_alumno(alumno1)
    grupo2.agregar_alumno(alumno2)

    carrera1.agregar_grupo(grupo1)
    carrera2.agregar_grupo(grupo2)

    lista_carreras.guardar_en_json()

    carreras_leidas = lista_carreras.leer_json()

    for carrera in carreras_leidas:
        print(carrera.mostrar_carrera())
