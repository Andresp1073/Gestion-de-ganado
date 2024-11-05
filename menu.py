import mysql.connector
from ganadero import Ganadero
from encargado import Encargado

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ranchmaster_db"
    )

def obtener_contraseña_rol(rol, connection, cursor):
    query = "SELECT contraseña FROM usuarios WHERE rol = %s"
    cursor.execute(query, (rol,))
    result = cursor.fetchone()
    return result[0] if result else None



def main():
    intentos = 3

    while intentos > 0:
        print("-----SISTEMA DE GESTION DE GANADO RANCHMASTER----")
        print("Seleccione su rol:")
        print("1. Ganadero")
        print("2. Encargado")
        print("3. Salir")
        rol_opcion = input("Ingrese el número de su rol: ")

        if rol_opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            return

        rol = "ganadero" if rol_opcion == "1" else "encargado" if rol_opcion == "2" else None
        if not rol:
            print("Opción de rol inválida. Inténtelo de nuevo.")
            continue

        contraseña = input("Ingrese su contraseña: ")
        connection = obtener_conexion()
        cursor = connection.cursor()
        contraseña_almacenada = obtener_contraseña_rol(rol, connection, cursor)

        if contraseña_almacenada and contraseña == contraseña_almacenada:
            id_usuario = 1 if rol == "ganadero" else 2
            db = Ganadero("ganadero", contraseña) if rol == "ganadero" else Encargado("encargado", contraseña)
            db.id_usuario = id_usuario
            print(f"Inicio de sesión exitoso como {db.role}.")
            

            if rol == "ganadero":
                resultado = db.menu_ganadero()
                if resultado == "regresar":
                    continue
            elif rol == "encargado":
                db.menu_encargado()
                continue
            break
        else:
            intentos -= 1
            print(f"Contraseña incorrecta. Intentos restantes: {intentos}")
            if intentos == 0:
                print("Error al iniciar sesión. Intente más tarde.")
                return
    

if __name__ == "__main__":
    main()  