class UserModel:
    def __init__(self):
        self.users = {
            "admin": "1234",
            "invitado": "invitado"
        }

    def add_user(self, username, password):
        if username in self.users:
            return False, "El usuario ya existe"
        if not username or not password:
            return False, "Todos los campos son obligatorios"
        self.users[username] = password
        return True, "Usuario registrado con éxito!"

    def validate_credentials(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False