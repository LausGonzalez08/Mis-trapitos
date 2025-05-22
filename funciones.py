#FUNCIONES
"""Favor de ser cuidadosos al realizar cambios en esta parte, es el cerebro de todo"""
#----Bibliotecas----
from usuarios import UserModel #Obtiene la funcion UserModel de usuarios.py
from InicioInterfaz import MainView #Obtiene la funcion MainView de InicioInterfaz.py
from logininterfaz import LoginView, RegisterView, messagebox #Obtiene las funciones LoginView, RegisterView y messagebox de logininterfaz.py
from ajustesinterfaz import SettingView
from userdataview import UserDataView
import tkinter as tk #Importa Tkinter


#----Main-----
class AppController:
    def __init__(self): #constructores
        self.root = tk.Tk()  #Precarga Tkinter
        self.model = UserModel() #Obtiene UserModel
        self.main_view = None #Obtiene main_view
        self.login_view = LoginView(self.root, self) #Obtiene LoginView de la interfaz de login
        self.register_view = None #Obtiene register_view
        self.root.withdraw() #Oculta la ventana
        self.login_view.entry_contraseña.bind("<Return>", self.login)# Enlazar evento <Return> al campo de contraseña
    #Funcion para Login
    def login(self, event=None):
        usuario = self.login_view.entry_usuario.get()
        contraseña = self.login_view.entry_contraseña.get()
        
        if self.model.validate_credentials(usuario, contraseña):
            self.model.registrar_login(usuario) 
            is_admin = self.model.is_admin(usuario)
            user_info = self.model.get_user_info(usuario)
            
            # Verificar si tiene dirección y teléfono
            if not user_info[3] or not user_info[4]:  # address y number
                self.login_view.destroy()
                messagebox.showwarning("Información requerida", 
                                      "Debe completar su información personal antes de continuar")
                self.show_settings(usuario, first_login=True)
            else:
                self.login_view.destroy()
                self.main_view = MainView(self.root, self, username=usuario, is_admin=is_admin)
                self.main_view.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def show_settings(self, username, first_login=False):
        settings_view = SettingView(self.root, self, username)
        if first_login:
            # Hacer que la ventana de configuración sea modal (obligatorio completar)
            settings_view.grab_set()
            settings_view.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilitar cierre
        settings_view.mainloop()
    
    def show_main_view(self, username):
        is_admin = self.model.is_admin(username)
        self.main_view = MainView(self.root, self, username=username, is_admin=is_admin)
        self.main_view.mainloop()
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
        self.login_view.entry_contraseña.bind("<Return>", self.login) #Funcion para leer la tecla ingresada
        self.login_view.deiconify()#Muestra la ventana Oculta
    
    def show_user_data(self):
        UserDataView(self.root, self)
    #----Funcion que ejecuta y muestra el programa-----
    def run(self):
        self.main_view.mainloop()

