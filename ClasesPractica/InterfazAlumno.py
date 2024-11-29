from Conexion import Conexion
from Alumno import Alumno

class InterfazAlumno:
    def __init__(self):
        self.conexion = Conexion()

    def mostrar_menu(self):
        return (
            "\n*** Menú de Administración de Alumnos ***\n"
            "1. Agregar Alumno\n"
            "2. Eliminar Alumno\n"
            "3. Actualizar Alumno\n"
            "4. Mostrar Alumnos\n"
            "5. Guardar y Salir\n"
        )

    def agregar_alumno(self, nombres, apellido_paterno, apellido_materno, curp, matricula):
        # Crear un objeto Alumno
        alumno = Alumno(nombres, apellido_paterno, apellido_materno, curp, matricula)
        alumno_data = alumno.to_dict()  # Convertir a diccionario
        self.conexion.insertar(self.conexion.coleccion, alumno_data)  # Insertar en la base de datos
        return f"Alumno {nombres} {apellido_paterno} {apellido_materno} agregado con éxito."

    def eliminar_alumno(self, matricula):
        query = {"matricula": matricula}  # Filtro por matrícula
        resultado = self.conexion.coleccion.delete_one(query)  # Eliminar un documento
        if resultado.deleted_count > 0:
            return f"Alumno con matrícula {matricula} eliminado con éxito."
        return f"No se encontró un alumno con matrícula {matricula}."

    def actualizar_alumno(self, matricula, nuevos_datos):
        # Actualizar el alumno por matrícula
        resultado = self.conexion.actualizar(self.conexion.coleccion, matricula, nuevos_datos, tipo_filtro="matricula")

        if resultado.matched_count > 0:
            return f"Alumno con matrícula {matricula} encontrado y actualizado"
        return f"No se encontró el alumno con matrícula {matricula}"

    def mostrar_alumnos(self):
        alumnos = self.conexion.findDocument(self.conexion.coleccion, {})  # Consulta todos los alumnos
        if alumnos:
            return "\n".join([f"Nombre: {alumno['nombres']}, Apellido Paterno: {alumno['apellido_paterno']}, "
                              f"Apellido Materno: {alumno['apellido_materno']}, CURP: {alumno['curp']}, "
                              f"Matrícula: {alumno['matricula']}" for alumno in alumnos])
        return "No hay alumnos registrados."

    def ejecutar_opciones(self, opcion, *args):
        if opcion == "1":
            return self.agregar_alumno(*args)
        elif opcion == "2":
            return self.eliminar_alumno(*args)
        elif opcion == "3":
            return self.actualizar_alumno(*args)
        elif opcion == "4":
            return self.mostrar_alumnos()
        elif opcion == "5":
            return "¡Adiós!"
        else:
            return "Opción no válida, por favor intente nuevamente."


if __name__ == "__main__":
    interfaz = InterfazAlumno()

    while True:
        print(interfaz.mostrar_menu())
        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Agregar Alumno
            nombres = input("Ingrese los nombres del alumno: ")
            apellido_paterno = input("Ingrese el apellido paterno del alumno: ")
            apellido_materno = input("Ingrese el apellido materno del alumno: ")
            curp = input("Ingrese la CURP del alumno: ")
            matricula = input("Ingrese la matrícula del alumno: ")
            print(interfaz.ejecutar_opciones(opcion, nombres, apellido_paterno, apellido_materno, curp, matricula))

        elif opcion == "2":  # Eliminar Alumno
            matricula = input("Ingrese la matrícula del alumno a eliminar: ")
            print(interfaz.ejecutar_opciones(opcion, matricula))

        elif opcion == "3":  # Actualizar Alumno
            matricula = input("Ingrese la matrícula del alumno a actualizar: ")
            nuevos_datos = {
                "nombres": input("Nuevo nombre: "),
                "apellido_paterno": input("Nuevo apellido paterno: "),
                "apellido_materno": input("Nuevo apellido materno: "),
                "curp": input("Nueva CURP: "),
                "matricula": input("Nueva matrícula: ")
            }
            print(interfaz.ejecutar_opciones(opcion, matricula, nuevos_datos))

        elif opcion == "4":  # Mostrar Alumnos
            print(interfaz.ejecutar_opciones(opcion))

        elif opcion == "5":  # Guardar y salir
            print(interfaz.ejecutar_opciones(opcion))
            break

        else:
            print("Opción no válida, por favor intente nuevamente.")
