#FUNCIONES
"""Favor de ser cuidadosos al realizar cambios en esta parte, es el cerebro de todo"""
#----Bibliotecas----
from usuarios import UserModel #Obtiene la funcion UserModel de usuarios.py
from InicioInterfaz import MainView #Obtiene la funcion MainView de InicioInterfaz.py
from logininterfaz import LoginView, RegisterView, messagebox #Obtiene las funciones LoginView, RegisterView y messagebox de logininterfaz.py
import tkinter as tk #Importa Tkinter

#----Main-----
class AppController:
    def __init__(self): #constructores
        self.root = tk.Tk()  #Precarga Tkinter
        self.model = UserModel() #Obtiene UserModel
        self.main_view = None #Obtiene main_view
        self.login_view = LoginView(None, self) #Obtiene LoginView de la interfaz de login
        self.register_view = None #Obtiene register_view
        self.root.withdraw() #Oculta la ventana
    
    #Funcion para Login
    def login(self):
        usuario = self.login_view.entry_usuario.get() #Obtiene lo ingresado de la zona de texto de usuario en logininterfaz.py
        contraseña = self.login_view.entry_contraseña.get() #Obtiene lo ingresado de la zona de texto de contraseña en logininterfaz.py
        if self.model.validate_credentials(usuario, contraseña): #Envia lo ingresado a validate_credentials
            is_admin = self.model.is_admin(usuario) #Envia el usuario ingresado a is_admin
            self.main_view = MainView(self.root, self, username=usuario, is_admin=is_admin) #Obtiene los datos
            self.login_view.destroy()#Cierra la ventana de login
            self.main_view.mainloop()#Mantiene la interfaz abierta
        else:
            messagebox.showerror("Error", "Credenciales incorrectas") #Validador si los datos son incorrectos
    
    #----Funcion para mostrar la interfaz de registro----
    def show_register(self):
        self.register_view = RegisterView(self.root, self) #Manda a llamar a la funcion
    
    #----Funcion para registrar usuarios
    def register_user(self):
        nuevo_user = self.register_view.entry_nuevo_usuario.get() #Obtiene lo ingresado de la zona de texto de usuario en logininterfaz.py
        nueva_pass = self.register_view.entry_nueva_contraseña.get() #Obtiene lo ingresado de la zona de texto de contraseña en logininterfaz.py
        confirm_pass = self.register_view.entry_confirmar_contraseña.get() #Obtiene lo ingresado de la zona de texto de confirmar contraseña en logininterfaz.py
        
        if nueva_pass != confirm_pass: #Valida que si las contraseñas coinciden
            messagebox.showerror("Error", "Las contraseñas no coinciden") #Si no coinciden muestra el mensaje
            return
            
        es_admin = self.register_view.tipo_usuario.get() == "admin" #Obtiene si es administrador el usuario 
        success, message = self.model.add_user(nuevo_user, nueva_pass, admin=es_admin) #Manda lo ingresado a la base de datos y guarda lo recibido de Usuarios.py
        if success: #Si se realizo el registro
            messagebox.showinfo("Éxito", message)
            self.register_view.destroy()
        else:
            messagebox.showerror("Error, algo salio mal", message) #Si no se realizo el exito
    
    #----Funcion para cerrar sesion----
    def logout(self):
        # Cerrar ventana principal
        if self.main_view: #Si esta en InicioInterfaz.py
            self.main_view.destroy() #Destruye la ventana principal
            self.main_view = None
        # Mostrar nueva ventana de login
        self.login_view = LoginView(self.root, self) #Vuelve a llamar LoginView de logininterfaz.py
        self.login_view.deiconify()#Muestra la ventana Oculta
    
    #----Funcion que ejecuta y muestra el programa-----
    def run(self):
        self.main_view.mainloop()

