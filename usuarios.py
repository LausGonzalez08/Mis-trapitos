#INTERFAZ DE LOGIN
#----Bibliotecas----
import sqlite3 #Libreria de la base de datos
import os
from datetime import datetime

#----Clase para la administracion de usuarios----
class UserModel: 
    def __init__(self, db_name='Mis_Trapitos.db'): #Carga la base de datos 
        self.db_name = db_name #Hace propio la base de datos
        self._ensure_db() #LLama al ensure_db
        self.historial_db = 'LoginHistorial.db'
        self._ensure_historial_db()
        self._ensure_inventario_db()
        self._ensure_clientes_db()
        self._ensure_proveedores_db()
        self._ensure_ventas_db()  
    #----Funcion para la base de datos----
    def _ensure_historial_db(self):
        """Crea la base de datos de historial de logins si no existe"""
        conn = sqlite3.connect(self.historial_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                fecha_hora TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def registrar_login(self, username):
        """Registra un login exitoso en la base de datos de historial"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.historial_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logins (username, fecha_hora) VALUES (?, ?)", (username, now))
        conn.commit()
        conn.close()

    def _ensure_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT 0,
                address TEXT,
                number TEXT
            )
        ''')
        # Verificar si las columnas nuevas existen y agregarlas si no
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'address' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN address TEXT")
        
        if 'number' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN number TEXT")
        conn.commit()
        conn.close()
    
    def add_user(self, username, password, admin=False):
        if not username or not password:
            return False, "Todos los campos son obligatorios"
        
        if self._user_exists(username):
            return False, "El usuario ya existe"
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", 
                     (username, password, int(admin)))
        conn.commit()
        conn.close()
        return True, "Usuario registrado con éxito!"
    
    def get_all_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users

    def delete_user(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()

    def update_password(self, username, new_password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()

    def get_login_historial(self):
        conn = sqlite3.connect(self.historial_db)
        cursor = conn.cursor()
        cursor.execute("SELECT username, fecha_hora FROM logins ORDER BY fecha_hora DESC")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_user_info(self, username):
        """Obtiene toda la información del usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_info = cursor.fetchone()
        conn.close()
        return user_info
    
    def update_user_info(self, username, address, number):
        """Actualiza la dirección y teléfono del usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET address = ?, number = ? WHERE username = ?", 
                      (address, number, username))
        conn.commit()
        conn.close()
        return True
    
    #----Funcion para verificar que un usuario ya existe en la BD
    def _user_exists(self, username):#Recibe Username
        conn = sqlite3.connect(self.db_name)#Conecta con la base de datos
        cursor = conn.cursor() #Crea el puntero para obtener datos de la base de datos
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,)) #Busca el usuario en la base de datos
        exists = cursor.fetchone() is not None #Guarda Sin no existe el usuario retorna None
        conn.close()#Cierra la conexion con la base de datos
        return exists #retorna exists (Username o None)
    
    #----Funcion para validar credenciales----
    def validate_credentials(self, username, password): #Recibe username y password
        conn = sqlite3.connect(self.db_name)#Conecta con la base de datos
        cursor = conn.cursor()  #Crea el puntero para obtener datos de la base de datos
        cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password)) #Obtiene los datos (Usuario y contraseña)
        valid = cursor.fetchone() is not None #Guarda una tupla con los datos si no hay retorna none
        conn.close() #Cierra la conexion con la base de datos
        return valid #Retorna lo que hay valid (Username,password o None)
    
    #----Funcion para validar si un usuario es administrador----
    def is_admin(self, username): #Recibe username
        conn = sqlite3.connect(self.db_name) #Conecta con la base de datos
        cursor = conn.cursor()  #Crea el puntero para obtener datos de la base de datos
        cursor.execute("SELECT admin FROM users WHERE username = ?", (username,)) #Busca el valor admin en la tabla de la base de datos
        row = cursor.fetchone() #Guarda los datos obtenidos en la base de datos
        conn.close()#Cierra la conexion con la base de datos
        return bool(row[0]) if row else False #Retorna True si row tiene datos, si row es None retorna False.
    
    def _ensure_inventario_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventario (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                proveedor TEXT,
                tipo TEXT,
                talla TEXT,
                persona TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def agregar_producto(self, id, nombre, cantidad, precio_unitario, proveedor, tipo, talla, persona):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO inventario (id, nombre, cantidad, precio_unitario, proveedor, tipo, talla, persona) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id, nombre, cantidad, precio_unitario, proveedor, tipo, talla, persona)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def obtener_inventario(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventario")
        datos = cursor.fetchall()
        conn.close()
        return datos
    
    def _ensure_ventas_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id TEXT NOT NULL,
                cliente_nombre TEXT NOT NULL,
                usuario TEXT NOT NULL,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')
        
        # Tabla de detalles de venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS venta_detalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id TEXT NOT NULL,
                producto_nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                talla TEXT,
                proveedor TEXT,
                tipo TEXT,
                persona TEXT,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES inventario(id)
            )
        ''')
        conn.commit()
        conn.close()

    def obtener_producto_completo(self, id_producto):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, cantidad, precio_unitario, proveedor, tipo, talla, persona 
            FROM inventario 
            WHERE id = ?
        """, (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    def registrar_venta_completa(self, id_cliente, nombre_cliente, usuario, total, productos):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Registrar venta principal
            cursor.execute("""
                INSERT INTO ventas 
                (cliente_id, cliente_nombre, usuario, fecha, total) 
                VALUES (?, ?, ?, datetime('now'), ?)
            """, (id_cliente, nombre_cliente, usuario, total))
            venta_id = cursor.lastrowid
            
            # Registrar productos
            for producto in productos:
                cursor.execute("""
                    INSERT INTO venta_detalle 
                    (venta_id, producto_id, producto_nombre, cantidad, precio_unitario,
                    talla, proveedor, tipo, persona, subtotal) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    venta_id,
                    producto['id'],
                    producto['nombre'],
                    producto['cantidad'],
                    producto['precio'],
                    producto['talla'],
                    producto['proveedor'],
                    producto['tipo'],
                    producto['persona'],
                    producto['subtotal']
                ))
                
                # Actualizar inventario
                cursor.execute("""
                    UPDATE inventario 
                    SET cantidad = cantidad - ? 
                    WHERE id = ?
                """, (producto['cantidad'], producto['id']))
            
            conn.commit()
            return venta_id
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error al registrar venta: {e}")
            return False
        finally:
            conn.close()
    def disminuir_cantidad_producto(self, id_producto, cantidad):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT cantidad FROM inventario WHERE id = ?", (id_producto,))
        resultado = cursor.fetchone()

        if resultado:
            cantidad_actual = resultado[0]
            nueva_cantidad = cantidad_actual - cantidad

            if nueva_cantidad > 0:
                cursor.execute("UPDATE inventario SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
                conn.commit()
                conn.close()
                return "parcial"
            elif nueva_cantidad == 0:
                cursor.execute("DELETE FROM inventario WHERE id = ?", (id_producto,))
                conn.commit()
                conn.close()
                return "total"
            else:
                conn.close()
                return "excede"
        else:
            conn.close()
            return "no_encontrado"
    
    def buscar_productos_por_nombre(self, nombre):
        """Busca productos por nombre (coincidencia parcial)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad FROM inventario WHERE nombre LIKE ?", 
                    (f"%{nombre}%",))
        productos = cursor.fetchall()
        conn.close()
        return productos

#clientes

    def _ensure_clientes_db(self):
        """Crea la tabla de clientes"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                correo TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def agregar_cliente(self, id, nombre, direccion, telefono, correo):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (id, nombre, direccion, telefono, correo) VALUES (?, ?, ?, ?, ?)",
                (id, nombre, direccion, telefono, correo)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def obtener_clientes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()
        conn.close()
        return datos

#proveedores

    def _ensure_proveedores_db(self):
        """Crea la tabla de proveedores"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                nombre TEXT PRIMARY KEY,
                contacto TEXT NOT NULL,
                direccion TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def agregar_proveedor(self, nombre, contacto, direccion):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO proveedores (nombre, contacto, direccion) VALUES (?, ?, ?)",
                (nombre, contacto, direccion)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def eliminar_proveedor(self, nombre):
        """Elimina un proveedor por su nombre"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM proveedores WHERE nombre = ?", (nombre,))
            conn.commit()
            return cursor.rowcount > 0  # Retorna True si se eliminó al menos un registro
        except sqlite3.Error:
            return False
        finally:
            conn.close()
        
    def obtener_proveedor(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores")
        datos = cursor.fetchall()
        conn.close()
        return datos