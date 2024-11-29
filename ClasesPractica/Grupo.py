import json
from Alumno import Alumno
from Arreglo import Arreglo

class Grupo(Arreglo):
    def __init__(self, nombre_grupo):
        super().__init__()
        self.nombre = nombre_grupo
        self.alumnos= Alumno()

    def agregar_alumno(self, alumno):
        if isinstance(alumno, Alumno):
            self.agregar(alumno)
        else:
            raise TypeError("Solo se pueden agregar objetos de tipo Alumno")

    def mostrar_grupo(self):
        info_grupo = f"Grupo: {self.nombre}\n"
        info_alumnos = "\n".join(
            f"Nombre: {alumno.Nombres}, Apellido Paterno: {alumno.Apellido_paterno}, "
            f"Apellido Materno: {alumno.Apellido_materno}, CURP: {alumno.CURP}, "
            f"Matrícula: {alumno.Matricula}"
            for alumno in self.elementos
        )
        return info_grupo + info_alumnos


    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "grupo": self.nombre,
            "alumnos": [alumno.to_dict() for alumno in self.elementos]
        }

    def guardar_en_json(self, archivo='Grupos.json'):
        with open(archivo, 'w') as file:
            json.dump([grupo.to_dict() for grupo in self.elementos], file, indent=4)

    def leer_json(self, archivo='Grupos.json'):
        self.elementos = []
        with open(archivo, 'r') as file:
            leido = json.load(file)
        return  self.hacer_objetos_grupo_desde_datos(leido)

    def hacer_objetos_grupo_desde_datos(self, leido):
        grupos = []
        for grupo_datos in leido:
            grupo = Grupo(grupo_datos.get("grupo"))

            alumnos_datos = grupo_datos.get("alumnos")
            alumnos = grupo.alumnos.hacer_objetos_alumno_desde_datos(alumnos_datos)

            for alumno in alumnos:
                grupo.agregar_alumno(alumno)

            grupos.append(grupo)
            self.agregar(grupo)
        return grupos

if __name__ == "__main__":
    alumno1 = Alumno("Daniel", "Sanchez", "Perez", "SAPE30342HGLRDRO9", 41806389)
    alumno2 = Alumno("Ana", "Lopez", "Martinez", "LOMA20422FGTDMN99", 41806400)

    alumno3 = Alumno("Marco", "Sanchez", "Perez", "SAPE30342HGLRDRO9", 41806389)
    alumno4 = Alumno("Francisco", "Lopez", "Martinez", "LOMA20422FGTDMN99", 41806400)

    grupoA = Grupo("Grupo A")
    grupoA.agregar_alumno(alumno1)
    grupoA.agregar_alumno(alumno2)

    grupoB = Grupo("Grupo B")
    grupoB.agregar_alumno(alumno3)
    grupoB.agregar_alumno(alumno4)

    lista_grupos = Grupo("Lista de Grupos")
    lista_grupos.agregar(grupoA)
    lista_grupos.agregar(grupoB)

    lista_grupos.guardar_en_json()

    grupos_leidos = lista_grupos.leer_json()

    for grupo in grupos_leidos:
        print(grupo.mostrar_grupo())

