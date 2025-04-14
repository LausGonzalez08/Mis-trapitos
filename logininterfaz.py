import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Login")
        self.geometry("300x250+400+300")
        self._make_widgets()
        
    def _make_widgets(self):
        self.marco_login = tk.Frame(self)
        self.marco_login.pack(pady=20)

        # Campos de usuario y contraseña
        tk.Label(self.marco_login, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_usuario = tk.Entry(self.marco_login)
        self.entry_usuario.grid(row=0, column=1)

        tk.Label(self.marco_login, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_contraseña = tk.Entry(self.marco_login, show="*")
        self.entry_contraseña.grid(row=1, column=1)

        # Marco para botones
        marco_botones = tk.Frame(self)
        marco_botones.pack(pady=10)

        btn_login = tk.Button(marco_botones, text="Ingresar", command=self.controller.login)
        btn_login.grid(row=0, column=0, padx=5)

        btn_registro = tk.Button(marco_botones, text="Registrar", command=self.controller.show_register)
        btn_registro.grid(row=0, column=1, padx=5)

class RegisterView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Registro")
        self.geometry("300x200+400+300")
        self._make_widgets()
        
    def _make_widgets(self):
        tk.Label(self, text="Nuevo usuario:").pack(pady=(10,0))
        self.entry_nuevo_usuario = tk.Entry(self)
        self.entry_nuevo_usuario.pack()
        
        tk.Label(self, text="Nueva contraseña:").pack(pady=(10,0))
        self.entry_nueva_contraseña = tk.Entry(self, show="*")
        self.entry_nueva_contraseña.pack()
        
        tk.Label(self, text="Confirmar contraseña:").pack(pady=(10,0))
        self.entry_confirmar_contraseña = tk.Entry(self, show="*")
        self.entry_confirmar_contraseña.pack()
        
        btn_guardar = tk.Button(self, text="Registrar", command=self.controller.register_user)
        btn_guardar.pack(pady=10)

