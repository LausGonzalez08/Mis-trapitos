import sqlite3
import os

class UserModel:
    def __init__(self, db_name='Mis_Trapitos.db'):
        self.db_name = db_name
        self._ensure_db()

    def _ensure_db(self):
        """Verifica si la base existe, si no, la crea con la tabla de usuarios"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(self, username, password, admin=False):
        if not username or not password:
            return False, "Todos los campos son obligatorios"
        
        if self._user_exists(username):
            return False, "El usuario ya existe"
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (username, password, int(admin)))
        conn.commit()
        conn.close()
        return True, "Usuario registrado con éxito!"

    def _user_exists(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def validate_credentials(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password))
        valid = cursor.fetchone() is not None
        conn.close()
        return valid
