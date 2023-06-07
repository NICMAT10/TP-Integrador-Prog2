# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha
import sqlite3
from datetime import datetime

# Crear conexión a la base de datos
conexion = sqlite3.connect('libreria.db')
cursor = conexion.cursor()

# clase principal

class Libreria:
    def ejecutar_menu(self):
        opcion = None
        while opcion != '0':
            print("\n--- MENÚ ---")
            print("1. Cargar Libros")
            print("2. Modificar precio de un libro")
            print("3. Borrar un libro")
            print("4. Cargar disponibilidad")
            print("5. Listado de Libros")
            print("6. Ventas")
            print("7. Actualizar Precios")
            print("8. Mostrar todos los registros anteriores a una fecha en específico")
            print("0. Salir")

            opcion = input("Ingrese una opción: ")

            if opcion == '1':
                id = input("Ingrese el ID del libro: ")
                isbn = input("Ingrese el ISBN del libro: ")
                titulo = input("Ingrese el título del libro: ")
                autor = input("Ingrese el autor del libro: ")
                genero = input("Ingrese el género del libro: ")
                precio = float(input("Ingrese el precio del libro: "))
                cant_disponible = int(input("Ingrese la cantidad disponible del libro: "))
                self.cargar_libro(id, isbn, titulo, autor, genero, precio, cant_disponible)
            elif opcion == '2':
                id = input("Ingrese el ID del libro: ")
                nuevo_precio = float(input("Ingrese el nuevo precio del libro: "))
                self.modificar_precio(id, nuevo_precio)
            elif opcion == '3':
                id = input("Ingrese el ID del libro: ")
                self.borrar_libro(id)
            elif opcion == '4':
                id = input("Ingrese el ID del libro: ")
                incremento = int(input("Ingrese el incremento de disponibilidad: "))
                self.cargar_disponibilidad(id, incremento)
            elif opcion == '5':
                self.listar_libros_ordenados()
            elif opcion == '6':
                libro_id = input("Ingrese el ID del libro vendido: ")
                cantidad = int(input("Ingrese la cantidad vendida: "))
                self.registrar_venta(libro_id, cantidad)
            elif opcion == '7':
                porcentaje_aumento = float(input("Ingrese el porcentaje de aumento de precios: "))
                self.actualizar_precios(porcentaje_aumento)
            elif opcion == '8':
                fecha_limite = input("Ingrese la fecha límite (formato: 'YYYY-MM-DD'): ")
                self.mostrar_registros_anteriores(fecha_limite)
            elif opcion == '0':
                print("Saliendo del programa...")
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

