import json
from Arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombres=None, apellido_paterno=None, apellido_materno=None, curp=None, matricula=None):
        super().__init__()
        self.Nombres = nombres if nombres else ""
        self.Apellido_paterno = apellido_paterno if apellido_paterno else ""
        self.Apellido_materno = apellido_materno if apellido_materno else ""
        self.CURP = curp if curp else ""
        self.Matricula = matricula if matricula else ""

    def mostrar(self):
        return (f"Nombre: {self.Nombres}, Apellido Paterno: {self.Apellido_paterno}, "
                f"Apellido Materno: {self.Apellido_materno}, CURP: {self.CURP}, "
                f"Matrícula: {self.Matricula}")

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "nombres": self.Nombres,
            "apellido_paterno": self.Apellido_paterno,
            "apellido_materno": self.Apellido_materno,
            "curp": self.CURP,
            "matricula": self.Matricula
        }

    def guardar_en_json(self, archivo='Alumnos.json'):
        lista_alumnos_json = [alumno.to_dict() for alumno in self.obtener_elementos()]
        with open(archivo, 'w') as file:
            json.dump(lista_alumnos_json, file, indent=4)

    def leer_json(self, archivo='Alumnos.json'):

            with open(archivo, 'r') as file:
                leido = json.load(file)
            alumnos = self.hacer_objetos_alumno_desde_datos(leido)
            return alumnos


    def hacer_objetos_alumno_desde_datos(self, leido):
        alumnos = []
        for alumno_datos in leido:
            alumno = Alumno(
                nombres=alumno_datos.get("nombres"),
                apellido_paterno=alumno_datos.get("apellido_paterno"),
                apellido_materno=alumno_datos.get("apellido_materno"),
                curp=alumno_datos.get("curp"),
                matricula=alumno_datos.get("matricula"),
            )
            alumnos.append(alumno)
            self.agregar(alumno)
        return alumnos


if __name__ == "__main__":
    lista_alumnos = Alumno()

    lista_alumnos.leer_json()


    json_leido= lista_alumnos.leer_json()



    for alumno in json_leido:
        print(alumno.mostrar())
