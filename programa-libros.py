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
    
    def crear_tablas(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Libros (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ISBN TEXT UNIQUE,
                Titulo TEXT,
                Autor TEXT,
                Genero TEXT,
                Precio REAL,
                FechaUltimoPrecio TEXT,
                CantDisponible INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ventas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LibroID INTEGER,
                Cantidad INTEGER,
                FechaVenta TEXT,
                FOREIGN KEY (LibroID) REFERENCES Libros(ID)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_libros (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ISBN TEXT,
                Titulo TEXT,
                Autor TEXT,
                Genero TEXT,
                Precio REAL,
                FechaUltimoPrecio TEXT,
                CantDisponible INTEGER
            )
        ''')

        conexion.commit()
    #Carga completa de los Libros
    def cargar_libro(self, id ,isbn, titulo, autor, genero, precio, cant_disponible):
        try:
            cursor.execute('INSERT INTO Libros (ID, ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, CantDisponible) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(id, isbn, titulo, autor, genero, precio, datetime.now().strftime("%Y-%m-%d"), cant_disponible))
            conexion.commit()
            print("¡Libro cargado exitosamente!")
        except sqlite3.IntegrityError:
            print("El ISBN ingresado ya existe. Por favor, ingrese un ISBN único.")
    #Modificar los precios de los Libros       
    def modificar_precio(self, id, nuevo_precio):
        try:
            cursor.execute('SELECT * FROM Libros WHERE ID = ?', (id,))
            libro = cursor.fetchone()
            if libro:
                confirmacion = input(f"¿Está seguro de cambiar el precio del libro '{libro[2]}'? (S/N): ")
                if confirmacion.upper() == 'S':
                    cursor.execute('UPDATE Libros SET Precio = ?, FechaUltimoPrecio = ? WHERE ID = ?',(nuevo_precio, datetime.now().strftime("%Y-%m-%d"), id))
                    conexion.commit()
                    print("¡Precio modificado exitosamente!")
            else:
                print("No se encontró ningún libro con ese ID.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
            
    #Borrar Libros        
    def borrar_libro(self, id):
        try:
            cursor.execute('SELECT * FROM Libros WHERE ID = ?', (id,))
            libro = cursor.fetchone()
            if libro:
                confirmacion = input(f"¿Está seguro de borrar el libro '{libro[1]}'? (S/N): ")
                if confirmacion.upper() == 'S':
                    cursor.execute('DELETE FROM Libros WHERE ID = ?', (id,))
                    conexion.commit()
                    print("¡Libro borrado exitosamente!")
            else:
                print("No se encontró ningún libro con ese ID.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
    
    #Incrementar el stock de los libros        
    def cargar_disponibilidad(self, id, incremento):
        try:
            cursor.execute('SELECT * FROM Libros WHERE ID = ?', (id,))
            libro = cursor.fetchone()
            if libro:
                nueva_cantidad = libro[7] + incremento
                cursor.execute('UPDATE Libros SET CantDisponible = ? WHERE ID = ?', (nueva_cantidad, id))
                conexion.commit()
                print("¡Disponibilidad cargada exitosamente!")
            else:
                print("No se encontró ningún libro con ese ID.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
    #Ordenar los Libros        
    def listar_libros_ordenados(self):
         cursor.execute('SELECT Autor, Genero FROM Libros ORDER BY Autor, Genero')
    libros = cursor.fetchall()
    if libros:
        autor_actual = None
        genero_actual = None

        print("Listado de Libros:")
        for libro in libros:
            if libro[0] != autor_actual:
                autor_actual = libro[0]
                print(f"\nAutor: {autor_actual}")

            if libro[1] != genero_actual:
                genero_actual = libro[1]
                print(f"\n  Género: {genero_actual}")

            print(f"    - {libro[2]}")
    else:
        print("No hay libros cargados en la base de datos.")
    
    #Registro de ventas de Libros        
    def registrar_venta(self, libro_id, cantidad):
        try:
            cursor.execute('SELECT * FROM Libros WHERE ID = ?', (libro_id,))
            libro = cursor.fetchone()
            if libro:
                if libro[7] >= cantidad:
                    fecha_venta = datetime.now().strftime("%Y-%m-%d")
                    cursor.execute('INSERT INTO Ventas (LibroID, Cantidad, FechaVenta) VALUES (?, ?, ?)',(libro_id, cantidad, fecha_venta))
                    nueva_cantidad = libro[7] - cantidad
                    cursor.execute('UPDATE Libros SET CantDisponible = ? WHERE ID = ?', (nueva_cantidad, libro_id))
                    conexion.commit()
                    print("¡Venta registrada exitosamente!")
                else:
                    print("No hay suficientes unidades disponibles para realizar la venta.")
            else:
                print("No se encontró ningún libro con ese ID.")
        except ValueError:
            print("El ID ingresado no es válido. Por favor, ingrese un ID numérico.")
            
    #Actualizar los precios de los Libros        
    def actualizar_precios(self, porcentaje_aumento):
        try:
            cursor.execute('SELECT * FROM Libros')
            libros = cursor.fetchall()
            if libros:
                for libro in libros:
                    precio_actual = libro[5]
                    nuevo_precio = precio_actual * (1 + porcentaje_aumento / 100)
                    cursor.execute('INSERT INTO historico_libros (ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, CantDisponible) VALUES (?, ?, ?, ?, ?, ?, ?)',(libro[1], libro[2], libro[3], libro[4], libro[5], libro[6], libro[7]))
                    cursor.execute('UPDATE Libros SET Precio = ?, FechaUltimoPrecio = ? WHERE ID = ?',(nuevo_precio, datetime.now().strftime("%Y-%m-%d"), libro[0]))
                conexion.commit()
                print("¡Precios actualizados exitosamente!")
            else:
                print("No hay libros cargados en la base de datos.")
        except ValueError:
            print("El porcentaje de aumento ingresado no es válido. Por favor, ingrese un valor numérico.")
            
    #Registros Anteriores        
   def mostrar_registros_anteriores(self, fecha_limite):
    try:
        cursor.execute('SELECT * FROM Libros WHERE FechaUltimoPrecio < ?', (fecha_limite,))
        libros = cursor.fetchall()
        
        cursor.execute('SELECT * FROM historico_libros WHERE FechaUltimoPrecio < ?', (fecha_limite,))
        historico_libros = cursor.fetchall()
        
        if libros or historico_libros:
            print("Registros anteriores a la fecha límite:")
            
            if libros:
                print("Registros de Libros:")
                for libro in libros:
                    print(f"ID: {libro[0]}, ISBN: {libro[1]}, Título: {libro[2]}, Autor: {libro[3]}, Género: {libro[4]}, Precio: {libro[5]}, Fecha Último Precio: {libro[6]}, Cantidad Disponible: {libro[7]}")
                    
            if historico_libros:
                print("Registros de histórico_libros:")
                for historico_libro in historico_libros:
                    print(f"ID: {historico_libro[0]}, ISBN: {historico_libro[1]}, Título: {historico_libro[2]}, Autor: {historico_libro[3]}, Género: {historico_libro[4]}, Precio: {historico_libro[5]}, Fecha Último Precio: {historico_libro[6]}, Cantidad Disponible: {historico_libro[7]}")
        else:
            print("No hay registros anteriores a la fecha límite en la base de datos.")
    except ValueError:
        print("La fecha ingresada no es válida. Por favor, ingrese una fecha en formato 'YYYY-MM-DD'.")


# Crear objeto Libreria y ejecutar menú
libreria = Libreria()
libreria.crear_tablas()
libreria.ejecutar_menu()

# Cerrar conexión a la base de datos
conexion.close()

