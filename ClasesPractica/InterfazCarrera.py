from Conexion import  Conexion
from InterfazGrupo import  InterfazGrupo

class InterfazCarrera:

    def __init__(self):
        self.conexion = Conexion()
        self.interfaz_grupo = InterfazGrupo()

    def mostrar_menu(self):
        return (
            "\n*** Menú de Administración de Carreras ***\n"
            "1. Agregar Carrera\n"
            "2. Eliminar Carrera\n"
            "3. Actualizar Carrera\n"
            "4. Mostrar Carreras\n"
            "5. Gestionar Grupos\n"
            "6. Agregar Alumno a Grupo\n"  # Nueva opción para agregar alumno a grupo
            "7. Guardar y Salir\n"
        )

    def agregar_carrera(self, nombre_carrera):
        carrera = {
            "nombre": nombre_carrera,
            "grupos": []
        }
        self.conexion.insertar(self.conexion.coleccion_carreras, carrera)
        return f"Carrera '{nombre_carrera}' agregada con éxito."

    def eliminar_carrera(self, nombre_carrera):
        carrera = self.conexion.findDocument(self.conexion.coleccion_carreras, {"nombre": nombre_carrera})
        if not carrera:
            return f"La carrera '{nombre_carrera}' ya no existe."

        # Suponiendo que hay una función para eliminar la carrera
        self.conexion.eliminarTodo(self.conexion.coleccion_carreras, {"nombre": nombre_carrera})
        return f"La carrera '{nombre_carrera}' ha sido eliminada con éxito."

    def mostrar_carrera(self):
        # Realiza la consulta para obtener las carreras
        carreras = self.conexion.findDocument(self.conexion.coleccion_carreras)

        # Verifica si la consulta devolvió resultados
        if not carreras:
            return "No hay carreras registradas."

        # Si existen carreras, procesamos cada una de ellas
        resultado = []
        for carrera in carreras:
            nombre = carrera.get("nombre", "Nombre no disponible")  # Obtiene el nombre de la carrera
            cantidad_grupos = len(carrera.get("grupos", []))  # Cuenta la cantidad de grupos en la carrera
            resultado.append(f"Carrera: {nombre}, Grupos: {cantidad_grupos}")

        # Retorna el resultado formateado
        return "\n".join(resultado)

    def actualizar_carrera(self, nombre_carrera, nuevos_datos):
        # Aquí ya puedes utilizar nombre_carrera y nuevos_datos
        carrera = self.conexion.findDocument(self.conexion.coleccion_carreras, {"nombre": nombre_carrera})
        if not carrera:
            return f"La carrera '{nombre_carrera}' no existe."

        # Realizar la actualización
        carrera[0]["nombre"] = nuevos_datos["nombre"]  # Actualizar el nombre
        self.conexion.actualizar(self.conexion.coleccion_carreras, {"nombre": nombre_carrera}, carrera[0])
        return f"La carrera '{nombre_carrera}' ha sido actualizada a '{nuevos_datos['nombre']}'"

    def gestionar_grupps(self, nombre_carrera, opcion_grupo, grupo_datos=None):
        carrera = self.conexion.findDocument(self.conexion.coleccion_carreras, {"nombre": nombre_carrera})
        if not carrera:
            return f"No se encontro la carrera {nombre_carrera}."
        carrera = carrera[0]

        if opcion_grupo == "agregar":
            grupo_nombre = grupo_datos.get("grupo")  # Extraemos el nombre del grupo
            if grupo_nombre:
                # Creamos el grupo como un diccionario
                nuevo_grupo = {
                    "nombre": grupo_nombre,
                    "alumnos": []  # Lista vacía de alumnos por defecto
                }

                if nuevo_grupo not in carrera["grupos"]:
                    carrera["grupos"].append(nuevo_grupo)
                    # Actualizar la carrera usando el nombre como filtro
                    self.conexion.actualizar(
                        self.conexion.coleccion_carreras, nombre_carrera, carrera, tipo_filtro="nombre"
                    )
                    return f"Grupo '{grupo_nombre}' agregado con éxito a la carrera '{nombre_carrera}'."
                else:
                    return f"El grupo '{grupo_nombre}' ya existe en la carrera '{nombre_carrera}'."
            else:
                return "No se proporcionó un nombre de grupo válido."




        elif opcion_grupo == "eliminar":
            # Verificar si se proporciona un nombre de grupo válido
            grupo = grupo_datos.get("grupo")  # Suponiendo que 'grupo' es el nombre del grupo
            if not grupo:
                return "El nombre del grupo no puede estar vacío."
            # Verificar si el grupo existe en la carrera
            if grupo not in carrera["grupos"]:
                return f"El grupo '{grupo}' no existe en la carrera '{nombre_carrera}'."
            # Eliminar el grupo de la lista de grupos
            carrera["grupos"].remove(grupo)
            # Actualizar la carrera en la base de datos
            self.conexion.actualizar(
                self.conexion.coleccion_carreras, {"nombre": nombre_carrera}, carrera
            )

            return f"Grupo '{grupo}' eliminado de la carrera '{nombre_carrera}'."


        elif opcion_grupo == "mostrar":
            # Mostrar todos los grupos de la carrera
            if carrera["grupos"]:
                return "\n".join([f"{i + 1}. {grupo}" for i, grupo in enumerate(carrera["grupos"])])
            return f"La carrera '{nombre_carrera}' no tiene grupos registrados."

        return "Opción de gestión de grupos no válida."

    def agregar_alumno_a_grupo(self, nombre_carrera, nombre_grupo, alumno_datos):
        carrera = self.conexion.findDocument(self.conexion.coleccion_carreras, {"nombre": nombre_carrera})
        if not carrera:
            return f"La carrera '{nombre_carrera}' no existe."
        carrera = carrera[0]

        grupo_encontrado = None
        for grupo in carrera["grupos"]:
            if grupo["nombre"] == nombre_grupo:
                grupo_encontrado = grupo
                break

        if not grupo_encontrado:
            return f"El grupo '{nombre_grupo}' no existe en la carrera '{nombre_carrera}'."

        # Asegúrate de que la lista de alumnos sea una lista válida.
        if "alumnos" not in grupo_encontrado:
            grupo_encontrado["alumnos"] = []

        # Evita duplicados
        for alumno in grupo_encontrado["alumnos"]:
            if alumno["matricula"] == alumno_datos["matricula"]:
                return f"El alumno con matrícula '{alumno_datos['matricula']}' ya está en el grupo '{nombre_grupo}'."

        # Agrega el alumno
        grupo_encontrado["alumnos"].append(alumno_datos)

        # Aquí se debe actualizar la base de datos después de realizar los cambios
        self.conexion.actualizar(self.conexion.coleccion_carreras, {"nombre": nombre_carrera}, carrera)
        return f"El alumno '{alumno_datos['nombres']} {alumno_datos['apellido_paterno']} {alumno_datos['apellido_materno']}' ha sido agregado al grupo '{nombre_grupo}' de la carrera '{nombre_carrera}'."

    def ejecutar_opciones(self, opcion, nombre=None, nuevos_datos=None, *args):
        if opcion == "1":  # Agregar carrera
            if nombre:  # Verifica si el nombre fue proporcionado
                return self.agregar_carrera(nombre)
            else:
                return "No se ha proporcionado el nombre de la carrera."

        elif opcion == "2":
            return self.eliminar_carrera(nombre)

        elif opcion == "3":
            return self.actualizar_carrera(nombre, nuevos_datos)  # Solo pasamos nombre y nuevos_datos

        elif opcion == "4":  # Mostrar carreras
            return self.mostrar_carrera()

        elif opcion == "5":
            return self.gestionar_grupos(*args)

        elif opcion == "6":
            carrera = input("Nombre de la carrera: ")
            grupo = input("Nombre del grupo: ")

            # Pedir los datos del alumno
            nombres = input("Nombre(s) del alumno: ")
            apellido_paterno = input("Apellido paterno: ")
            apellido_materno = input("Apellido materno: ")
            curp = input("CURP del alumno: ")
            matricula = input("Matrícula del alumno: ")

            alumno_datos = {
                "nombres": nombres,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "curp": curp,
                "matricula": matricula
            }

            print(self.agregar_alumno_a_grupo(carrera, grupo, alumno_datos))

        elif opcion == "7":
            return "¡Adiós!"
        else:
            return "Opción no válida, por favor intente nuevamente."


if __name__ == "__main__":
    interfaz = InterfazCarrera()

    while True:
        print(interfaz.mostrar_menu())
        opcion = input("Elige una opción: ")

        if opcion == "1":  # Opción para agregar carrera
            nombre_carrera = input("Ingrese el nombre de la carrera: ")
            if nombre_carrera:
                print(interfaz.ejecutar_opciones("1", nombre_carrera))  # Pasamos nombre_carrera directamente
            else:
                print("Debe proporcionar un nombre para la carrera.")

        elif opcion == "2":
            nombre = input("Nombre de la carrera a eliminar: ")
            print(interfaz.ejecutar_opciones("2", nombre))


        elif opcion == "3":
            nombre = input("Nombre de la carrera a modificar: ")
            nuevos_datos = {"nombre": input("Nuevo nombre: ")}
            print(interfaz.ejecutar_opciones("3", nombre, nuevos_datos))


        elif opcion == "4":  # Mostrar carreras
            print(interfaz.ejecutar_opciones("4"))  # No es necesario pasar el nombre

        elif opcion == "5":
            carrera = input("Nombre de la carrera a gestionar: ")
            print("Opciones: agregar, eliminar, mostrar")
            opcion_grupo = input("¿Qué desea hacer con los grupos? ")
            if opcion_grupo == "agregar":
                grupo_datos = {
                    "grupo": input("Nombre del grupo: ")
                }
                print(interfaz.gestionar_grupps(carrera, opcion_grupo, grupo_datos))
            elif opcion_grupo == "eliminar":
                grupo_datos = {
                    "grupo": input("Nombre del grupo a eliminar: ")
                }
                print(interfaz.gestionar_grupps(carrera, opcion_grupo, grupo_datos))
            elif opcion_grupo == "mostrar":
                print(interfaz.gestionar_grupps(carrera, opcion_grupo))
            else:
                print("Opción no válida.")

        elif opcion == "6":
            # Ingreso de los datos necesarios
            carrera = input("Nombre de la carrera: ")
            grupo = input("Nombre del grupo: ")
            # Pedir los datos del alumno
            nombres = input("Nombre(s) del alumno: ")
            apellido_paterno = input("Apellido paterno: ")
            apellido_materno = input("Apellido materno: ")
            curp = input("CURP del alumno: ")
            matricula = input("Matrícula del alumno: ")
            # Crear el diccionario del alumno
            alumno_datos = {
                "nombres": nombres,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "curp": curp,
                "matricula": matricula
            }
        # Llamar a la función para agregar el alumno al grupo
            print(interfaz.agregar_alumno_a_grupo(carrera, grupo, alumno_datos))

        elif opcion == "6":
            print("¡Adiós!")
            break

        else:
            print("Opción no válida, elige un número del 1 al 6.")
