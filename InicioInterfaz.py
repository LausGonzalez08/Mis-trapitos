import tkinter as tk
import sys

class MainView(tk.Toplevel):
    def __init__(self, master, controller, username='', is_admin=False):
        super().__init__(master)
        self.controller = controller
        self.username = username #Recibe Nombre de Usuario
        self.is_admin = is_admin #Recibe si es administrador

        titulo = f"Inicio - {self.username}"
        if self.is_admin:#validador de usuario tipo administrador
            titulo += " (Administrador)" #Si es administrador agregar "administrador"
        self.title(titulo)#titulo

        self.geometry("800x600+100+50")#Tamaño de ventana
        self._make_menu()#menu
        
    def _make_menu(self):
        self.barra_menu = tk.Menu(self)#Agrega la barra de menu a menu
        self.config(menu=self.barra_menu) 
        #Menu
        menu_opciones = tk.Menu(self.barra_menu, tearoff=0, bg="lightblue", fg="black")
        menu_opciones.add_command(label="Ajustes")
        #Opciones solo para administrador
        if self.is_admin:
            menu_opciones.add_separator()
            menu_opciones.add_command(
                label="Agregar nuevo Usuario", 
                command=self.controller.show_register  # <-- Acceso al controlador
            )
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=sys.exit)
        self.barra_menu.add_cascade(label="Opciones", menu=menu_opciones)#Agrega el boton "Opciones" a la barra de menu
