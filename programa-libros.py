# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha
import sqlite3
from datetime import datetime


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

            try:
                if opcion == '1':
                    isbn = int(input("Ingrese el ISBN del libro: "))
                    titulo = str(input("Ingrese el título del libro: "))
                    autor = str(input("Ingrese el autor del libro: "))
                    genero = str(input("Ingrese el género del libro: "))
                    precio = float(input("Ingrese el precio del libro: "))
                    cant_disponible = int(input("Ingrese la cantidad disponible del libro: "))
                    self.cargar_libro(isbn, titulo, autor, genero, precio, cant_disponible)
                elif opcion == '2':
                    id = input("Ingrese el ID del libro: ")
                    nuevo_precio = float(input("Ingrese el nuevo precio del libro: "))
                    confirmacion = input("¿Está seguro que desea modificar el precio? (S/N): ")
                    if confirmacion.upper() == 'S':
                        self.modificar_precio(id, nuevo_precio)
                elif opcion == '3':
                    id = int(input("Ingrese el ID del libro: "))
                    confirmacion = input("¿Está seguro que desea borrar el libro? (S/N): ")
                    if confirmacion.upper() == 'S':
                        self.borrar_libro(id)
                elif opcion == '4':
                    id = input("Ingrese el ID del libro: ")
                    incremento = int(input("Ingrese el incremento de disponibilidad: "))
                    self.cargar_disponibilidad(id, incremento)
                elif opcion == '5':
                    print("Ordenar por 1-ID")
                    print("Ordenar por 2-Autor")
                    print("Ordenar por 3-Titulo")
                    eleccion = int(input("Seleccione una opcion: "))
                    if eleccion == 1:
                        self.mostrar_libros_id()
                    elif eleccion == 2:
                        self.mostrar_libros_autor()
                    elif eleccion == 3:
                        self.mostrar_libros_titulo()
                    else:
                        print("Opción inválida. Por favor, seleccione una opción válida.")
                elif opcion == '6':
                    libro_id = int(input("Ingrese el ID del libro vendido: "))
                    cantidad = int(input("Ingrese la cantidad vendida: "))
                    self.registrar_venta(libro_id, cantidad)
                elif opcion == '7':
                    porcentaje_aumento = float(input("Ingrese el porcentaje de aumento de precios: "))
                    confirmacion = input("¿Está seguro que desea actualizar los precios? (S/N): ")
                    if confirmacion.upper() == 'S':
                        self.actualizar_precios(porcentaje_aumento)
                elif opcion == '8':
                    fecha_limite = input("Ingrese la fecha límite (formato: 'YYYY-MM-DD'): ")
                    self.mostrar_registros_anteriores(fecha_limite)
                elif opcion == '0':
                    print("Saliendo del programa, gracias por usar nuestro Software...")
                else:
                    print("Opción inválida. Por favor, seleccione una opción válida.")
            except Exception as e:
                print("Error:", str(e))

    def crear_tablas(self):
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Libros (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ISBN TEXT UNIQUE,
                    Titulo TEXT,
                    Autor TEXT,
                    Genero TEXT,
                    Precio REAL,
                    FechaUltimoPrecio DATE,
                    CantDisponible INTEGER
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Ventas (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LibroID INTEGER,
                    FechaVenta DATE,
                    Cantidad INTEGER,
                    FOREIGN KEY (LibroID) REFERENCES Libros(ID)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS RegistrosAnteriores (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LibroID INTEGER,
                    FechaRegistro DATE,
                    PrecioAnterior REAL,
                    FOREIGN KEY (LibroID) REFERENCES Libros(ID)
                )
            ''')

            conexion.commit()
            print("Tablas creadas exitosamente.")
        except sqlite3.Error as e:
            print("Error al crear las tablas:", str(e))
#Carga completa de los Libros
    def cargar_libro(self,isbn, titulo, autor, genero, precio, cant_disponible):
        try:
            cursor.execute('INSERT INTO Libros ( ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, CantDisponible) VALUES (?, ?, ?, ?, ?, ?, ?)',(isbn, titulo, autor, genero, precio, datetime.now().strftime("%Y-%m-%d"), cant_disponible))
            conexion.commit()
            print("¡Libro cargado exitosamente!")
        except sqlite3.IntegrityError:
            print("El ISBN ingresado ya existe. Por favor, ingrese un ISBN único.")
#Modificar los precios de los Libros 
    def modificar_precio(self, id_libro, nuevo_precio):
        try:
            cursor.execute("SELECT * FROM Libros WHERE ID = ?", (id_libro,))
            libro = cursor.fetchone()
            if libro:
                self.insertar_registro_historico(id_libro)
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("UPDATE Libros SET Precio = ?, FechaUltimoPrecio = ? WHERE ID = ?", (nuevo_precio, fecha_actual, id_libro))
                conexion.commit()
                print("Precio del libro modificado exitosamente.")
            else:
                print("No se encontró un libro con el ID especificado.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
#Borrar Libros  
    def borrar_libro(self, id_libro):
        try:
            cursor.execute("SELECT * FROM Libros WHERE ID = ?", (id_libro,))
            libro = cursor.fetchone()
            if libro:
                cursor.execute("DELETE FROM Libros WHERE ID = ?", (id_libro,))
                conexion.commit()
                print("Libro borrado exitosamente.")
            else:
                print("No se encontró un libro con el ID especificado.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
#Incrementar el stock de los libros
    def cargar_disponibilidad(self, id_libro, incremento):
        try:
            cursor.execute("SELECT * FROM Libros WHERE ID = ?", (id_libro,))
            libro = cursor.fetchone()
            if libro:
                nueva_cantidad = libro[7] + incremento
                cursor.execute("UPDATE Libros SET CantDisponible = ? WHERE ID = ?", (nueva_cantidad, id_libro))
                conexion.commit()
                print("Disponibilidad del libro actualizada exitosamente.")
            else:
                print("No se encontró un libro con el ID especificado.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
#Ordenar los Libros 
    def mostrar_libros_id(self):
        try:
            cursor.execute("SELECT * FROM Libros ORDER BY ID")
            libros = cursor.fetchall()
            if libros:
                print("\n--- Listado de Libros por ID ---")
                for libro in libros:
                    print(f"ID: {libro[0]}, ISBN: {libro[1]}, Título: {libro[2]}, Autor: {libro[3]}, Precio: {libro[5]}, Cantidad Disponible: {libro[7]}")
            else:
                print("No hay libros disponibles.")
        except sqlite3.Error as e:
            print("Error al mostrar los libros por ID:", str(e))

    def mostrar_libros_autor(self):
        try:
            cursor.execute("SELECT * FROM Libros ORDER BY Autor")
            libros = cursor.fetchall()
            if libros:
                print("\n--- Listado de Libros por Autor ---")
                for libro in libros:
                    print(f"Autor: {libro[3]},ID: {libro[0]}, ISBN: {libro[1]}, Título: {libro[2]}, Precio: {libro[5]}, Cantidad Disponible: {libro[7]}")
            else:
                print("No hay libros disponibles.")
        except sqlite3.Error as e:
            print("Error al mostrar los libros por autor:", str(e))

    def mostrar_libros_titulo(self):
        try:
            cursor.execute("SELECT * FROM Libros ORDER BY Titulo")
            libros = cursor.fetchall()
            if libros:
                print("\n--- Listado de Libros por Título ---")
                for libro in libros:
                    print(f"Título: {libro[2]},ID: {libro[0]}, ISBN: {libro[1]}, Autor: {libro[3]}, Precio: {libro[5]}, Cantidad Disponible: {libro[7]}")
            else:
                print("No hay libros disponibles.")
        except sqlite3.Error as e:
            print("Error al mostrar los libros por título:", str(e))
#Registro de ventas de Libros
    def registrar_venta(self, id_libro, cantidad):
        try:
            cursor.execute("SELECT * FROM Libros WHERE ID = ?", (id_libro,))
            libro = cursor.fetchone()
            if libro:
                if libro[7] >= cantidad:
                    fecha_actual = datetime.now().strftime('%Y-%m-%d')
                    cursor.execute("INSERT INTO Ventas (LibroID, FechaVenta, Cantidad) VALUES (?, ?, ?)", (id_libro, fecha_actual, cantidad))
                    nueva_cantidad = libro[7] - cantidad
                    cursor.execute("UPDATE Libros SET CantDisponible = ? WHERE ID = ?", (nueva_cantidad, id_libro))
                    conexion.commit()
                    print(f"LibroID:{id_libro} - Cantidad:{cantidad} - FechaVenta:{fecha_actual}")
                    print("Venta registrada exitosamente.")
                else:
                    print("No hay suficiente cantidad disponible del libro.")
            else:
                print("No se encontró un libro con el ID especificado.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
            
#Actualizar los precios de los Libros  
    def actualizar_precios(self,porcentaje_aumento):
        try:
            cursor.execute("SELECT * FROM Libros")
            libros = cursor.fetchall()
            if libros:
                for libro in libros:
                    nuevo_precio = libro[5] * (1 + (porcentaje_aumento / 100))
                    fecha_actual = datetime.now().strftime('%Y-%m-%d')
                    cursor.execute("UPDATE Libros SET Precio = ?, FechaUltimoPrecio = ? WHERE ID = ?", (nuevo_precio, fecha_actual, libro[0]))
                    conexion.commit()
                    print("Precios actualizados exitosamente.")
            else:
                print("No hay libros disponibles.")
        except sqlite3.Error as e:
            print("Error al actualizar los precios:", str(e))
#Registros Anteriores
    def insertar_registro_historico(self, id_libro):
        try:
            cursor.execute("SELECT * FROM Libros WHERE ID = ?", (id_libro,))
            libro = cursor.fetchone()
            if libro:
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("INSERT INTO RegistrosAnteriores (LibroID, FechaRegistro, PrecioAnterior) VALUES (?, ?, ?)", (id_libro, fecha_actual, libro[5]))
                conexion.commit()
        except ValueError:
            print("El porcentaje de aumento ingresado no es válido. Por favor, ingrese un valor numérico.")


    def mostrar_registros_anteriores(self, fecha_limite):
        try:
            cursor.execute("SELECT * FROM RegistrosAnteriores WHERE FechaRegistro <= ?", (fecha_limite,))
            registros = cursor.fetchall()
            if registros:
                print("\n--- Registros Anteriores ---")
                for registro in registros:
                    cursor.execute("SELECT * FROM Libros WHERE ID = ?", (registro[1],))
                    libro = cursor.fetchone()
                    if libro:
                        print(f"ID: {libro[0]}, Título: {libro[2]}, Fecha Registro: {registro[2]}, Precio Anterior: {registro[3]}")
            else:
                print("No hay registros anteriores a la fecha especificada.")
        except ValueError:
            print("La fecha ingresada no es válida. Por favor, ingrese una fecha en formato 'YYYY-MM-DD'.")


# Crear objeto Libreria y ejecutar menú
libreria = Libreria()
libreria.crear_tablas()
libreria.ejecutar_menu()

# Cerrar conexión a la base de datos
conexion.close()


