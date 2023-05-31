# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha
import sqlite3

#clase principal

class programa():
    def menu(self):
        while True:
            print("\nMenú de opciones:\n")
            print("1-Cargar libros")
            print("2-Modificar datos")
            print("3-Borrar un libro")
            print("4-Cargar disponibilidad")
            print("5-Listado de libros")
            print("6-Crear nueva tabla. Ingresar libro")
            print("7-Actualizar precio")
            print("8-Mostrar registros hasta fecha indicada")
            print("0-Salir del programa")
            opcion = int(input("\nIngrese una opción:\n"))
            
            if opcion == 1: # pide los datos para luego guardarlos en las columnas correspondientes de la tabla "Libros"
                titulo = str(input("Ingrese marca: "))
                autor = str(input("Ingrese autor: "))
                genero = str(input("Ingrese el genero: "))
                precio = float(input("Ingrese el precio: "))
                cantidad = int(input("Ingrese stock del producto: "))
                fecha_ultimo_precio = int(input("Ingrese la fecha del ultimo precio: "))
                cargarLibros(titulo,autor,genero,precio,cantidad,fecha_ultimo_precio)
                
            
            elif opcion == 0: # permite romper con el loop del while y se sale del programa
                print("Fin del programa, gracias por utilizar nuestro software :).")
                break