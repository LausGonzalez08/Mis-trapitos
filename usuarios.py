#INTERFAZ DE LOGIN
#----Bibliotecas----
import sqlite3 #Libreria de la base de datos
import os

#----Clase para la administracion de usuarios----
class UserModel: 
    def __init__(self, db_name='Mis_Trapitos.db'): #Carga la base de datos 
        self.db_name = db_name #Hace propio la base de datos
        self._ensure_db() #LLama al ensure_db
    
    #----Funcion para la base de datos----
    def _ensure_db(self):
        """Verifica si la base de datos existe, si no, la crea con la tabla de usuarios"""
        conn = sqlite3.connect(self.db_name) #Conecta con la base de datos
        cursor = conn.cursor() #Crea el puntero para obtener datos de la base de datos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT 0
            )
        ''') #Busca o crea la Tabla en la base de datos
        conn.commit()#Guarda los cambios
        conn.close()# Cierra la conexión
    
    #----Funcion para añadir usuarios----
    def add_user(self, username, password, admin=False): #Recibe username, password, admin
        if not username or not password:#Validacion para comprobar que todos los campos hayan sido llenados
            return False, "Todos los campos son obligatorios"
        
        if self._user_exists(username): #Validacion para avisar que un usuario ya existe
            return False, "El usuario ya existe"
        
        conn = sqlite3.connect(self.db_name) #Conectar con la base de datos
        cursor = conn.cursor()  #Crea el puntero para obtener datos de la base de datos
        cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (username, password, int(admin))) #Inserta los datos
        conn.commit()#Guarda los cambios
        conn.close()#Cierra la conexion con la base de datos
        return True, "Usuario registrado con éxito!" #Si se registro bien, retorna
    
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