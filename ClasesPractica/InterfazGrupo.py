from Conexion import  Conexion
from InterfazAlumno import  InterfazAlumno

class InterfazGrupo:
    def __init__(self):
        self.conexion = Conexion()
        self.interfaz_alumno = InterfazAlumno()

    def mostrar_menu(self):
        return (
            "\n*** Menú de Administración de Grupos ***\n"
            "1. Agregar Grupo\n"
            "2. Eliminar Grupo\n"
            "3. Actualizar Grupo\n"
            "4. Mostrar Grupos\n"
            "5. Gestionar Grupos\n"
            "6. Guardar y Salir\n"
        )
    def agregar_grupo(self, nombre_grupo):
        grupo = {
            "grupo": nombre_grupo,
            "alumnos": []
        }
        self.conexion.insertar(self.conexion.coleccion_grupos, grupo)
        return f"Grupo{nombre_grupo} agregado con exito"

    def eliminar_grupo(self, nombredelgrupo):
        query = {"grupo": nombredelgrupo}
        resultado = self.conexion.eliminarTodo(self.conexion.coleccion_grupos, query)
        if resultado > 0:  # Si se eliminaron documentos
            return f"Grupo Eliminado con exito"
        return f"No se encontro ningun grupo llamado {nombredelgrupo}"

    def actualizaar_grupo(self, grupo, nuevos_datos):

        resultado = self.conexion.actualizar(self.conexion.coleccion_grupos, grupo, nuevos_datos, tipo_filtro="grupo")
        if resultado.matched_count > 0:
            return  f"Grupo {grupo} encontrado y actualizado"
        return f"No se encontro el grupo"

    def mostrar_grupos(self):
        grupos = self.conexion.findDocument(self.conexion.coleccion_grupos)

        # Verificar si hay resultados
        if not grupos:
            return "No hay grupos registrados."

        # Construir el mensaje de salida
        resultado = []
        for grupo in grupos:
            # Manejo seguro de claves para evitar errores
            nombre_grupo = grupo.get("grupo", "Nombre no disponible")
            cantidad_alumnos = len(grupo.get("alumnos", []))
            resultado.append(f"Grupo: {nombre_grupo}, Alumnos: {cantidad_alumnos}")

        return "\n".join(resultado)

    def gestion_alumnos(self, nombre_grupo, opcion_alumno, alumno_data=None, matricula=None):
        grupo = self.conexion.findDocument(self.conexion.coleccion_grupos, {"grupo": nombre_grupo})
        if not grupo:
            return  f"No se encontro el grupo {nombre_grupo}."

        grupo = grupo[0]
        if opcion_alumno =="agregar":
            grupo["alumnos"].append(alumno_data)
            self.conexion.actualizar(self.conexion.coleccion_grupos, nombre_grupo, grupo, tipo_filtro="grupo")
            return f"Alumno{alumno_data['nombres']} agregado con exito."

        elif opcion_alumno == "eliminar":
            grupo["alumnos"] = [alumno for alumno in grupo["alumnos"] if alumno["matricula"] != matricula]
            self.conexion.actualizar(self.conexion.coleccion_grupos, nombre_grupo, grupo, tipo_filtro="grupo")
            return f"Alumno con matrícula {matricula} eliminado del grupo {nombre_grupo}."

        elif opcion_alumno == "mostrar":
            if grupo["alumnos"]:
                return "\n".join(
                    [f"{i + 1}. {alumno['nombres']} {alumno['apellido_paterno']} ({alumno['matricula']})"
                     for i, alumno in enumerate(grupo["alumnos"])]
                )
            return f"El grupo {nombre_grupo} no tiene alumnos registrados."
        return "Opción de gestión de alumnos no válida."


    def ejecutar_opciones(self, opcion, *args):
        if opcion == "1":
            return self.agregar_grupo(*args)
        elif opcion == "2":
            return self.eliminar_grupo(*args)
        elif opcion == "3":
            return self.actualizaar_grupo(*args)
        elif opcion == "4":
            return self.mostrar_grupos()
        elif opcion == "5":
            return self.gestion_alumnos()
        elif opcion == "6":
            return "¡Adiós!"
        else:
            return "Opción no válida, por favor intente nuevamente."


if __name__ == "__main__":
    interfaz = InterfazGrupo()

    while True:
        print(interfaz.mostrar_menu())
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            Nombre = input("Ingresa el nombre del grupo: ")
            print(interfaz.ejecutar_opciones(opcion, Nombre))

        elif opcion == "2":
            grupo = input("Ingresa el grupo a eliminar: ")
            print(interfaz.ejecutar_opciones(opcion, grupo))

        elif opcion == "3":
            grupo = input("Ingresa el grupo a modificar: ")
            nuevos_datos = {
                "grupo": input("Nuevo grupo: ")
            }
            print(interfaz.ejecutar_opciones(opcion, grupo, nuevos_datos))

        elif opcion == "4":
            print(interfaz.ejecutar_opciones(opcion))


        elif opcion == "5":
            nombre_grupo = input("Ingresa el nombre del grupo a gestionar: ")
            print("Opciones: agregar, eliminar, mostrar")
            opcion_alumno = input("¿Qué desea hacer con los alumnos? ")
            if opcion_alumno == "agregar":
                alumno_datos = {
                    "nombres": input("Nombres del alumno: "),
                    "apellido_paterno": input("Apellido paterno: "),
                    "apellido_materno": input("Apellido materno: "),
                    "curp": input("CURP: "),
                    "matricula": input("Matrícula: ")
                }
                resultado = interfaz.gestion_alumnos(nombre_grupo, opcion_alumno, alumno_data=alumno_datos)
                print(resultado)
            elif opcion_alumno == "eliminar":
                matricula = input("Matrícula del alumno a eliminar: ")
                resultado = interfaz.gestion_alumnos(nombre_grupo, opcion_alumno, matricula=matricula)
                print(resultado)
            elif opcion_alumno == "mostrar":
                resultado = interfaz.gestion_alumnos(nombre_grupo, opcion_alumno)
                print(resultado)
            else:
                print("Opción no válida.")

        elif opcion=="6":
            resultado = interfaz.ejecutar_opciones(opcion)
            break

        else:
            print("Opcion no valida, elige un numero del 1-5: ")
