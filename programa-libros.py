# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha
import sqlite3
from datetime import datetime

# Crear conexión a la base de datos
conexion = sqlite3.connect('libreria.db')
cursor = conexion.cursor()

# clase principal

class Libreria:
    def __init__(self):
        self.conexion = sqlite3.connect('libreria.db')
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
                                id INTEGER PRIMARY KEY,
                                isbn TEXT,
                                titulo TEXT,
                                autor TEXT,
                                genero TEXT,
                                precio REAL,
                                cant_disponible INTEGER,
                                fecha_registro TEXT)''')
        self.conexion.commit()

    def cargar_libro(self, id, isbn, titulo, autor, genero, precio, cant_disponible):
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''INSERT INTO libros VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (id, isbn, titulo, autor, genero, precio, cant_disponible, fecha_registro))
        self.conexion.commit()
        print("Libro cargado exitosamente.")

    def modificar_precio(self, id, nuevo_precio):
        self.cursor.execute('''UPDATE libros SET precio = ? WHERE id = ?''', (nuevo_precio, id))
        self.conexion.commit()
        print("Precio del libro modificado exitosamente.")

    def borrar_libro(self, id):
        self.cursor.execute('''DELETE FROM libros WHERE id = ?''', (id,))
        self.conexion.commit()
        print("Libro borrado exitosamente.")

    def cargar_disponibilidad(self, id, incremento):
        self.cursor.execute('''SELECT cant_disponible FROM libros WHERE id = ?''', (id,))
        cantidad_actual = self.cursor.fetchone()[0]
        nueva_cantidad = cantidad_actual + incremento
        self.cursor.execute('''UPDATE libros SET cant_disponible = ? WHERE id = ?''', (nueva_cantidad, id))
        self.conexion.commit()
        print("Disponibilidad cargada exitosamente.")

    def listar_libros_ordenados(self):
        self.cursor.execute('''SELECT * FROM libros ORDER BY titulo ASC''')
        libros = self.cursor.fetchall()
        for libro in libros:
            print(libro)

    def registrar_venta(self, libro_id, cantidad):
        self.cursor.execute('''SELECT cant_disponible FROM libros WHERE id = ?''', (libro_id,))
        cantidad_disponible = self.cursor.fetchone()[0]
        if cantidad <= cantidad_disponible:
            nueva_cantidad = cantidad_disponible - cantidad
            self.cursor.execute('''UPDATE libros SET cant_disponible = ? WHERE id = ?''', (nueva_cantidad, libro_id))
            self.conexion.commit()
            print("Venta registrada exitosamente.")
        else:
            print("No hay suficiente cantidad disponible para realizar la venta.")

    def actualizar_precios(self, porcentaje_aumento):
        self.cursor.execute('''UPDATE libros SET precio = precio * (1 + ? / 100)''', (porcentaje_aumento,))
        self.conexion.commit()
        print("Precios actualizados exitosamente.")

    def mostrar_registros_anteriores(self, fecha_limite):
        self.cursor.execute('''SELECT * FROM libros WHERE fecha_registro < ?''', (fecha_limite,))
        registros = self.cursor.fetchall()
        for registro in registros:
            print(registro)
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

