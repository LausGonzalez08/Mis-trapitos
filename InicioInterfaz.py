#INTERFAZ DE INICIO (no confundir con login)
#----Bibliotecas----
import tkinter as tk #Tkinter que es la libreria para la interfaz, que se importa como tk =Tkinter
import sys #Importamos Sys 
from ajustesinterfaz import SettingView

#----Clase para Interfaz de inicio----
class MainView(tk.Toplevel):#Toplevel es para que la ventana pase a ser la principal
    """___init___ es el constructor de una clase"""
    
    def __init__(self, master, controller, username='', is_admin=False): #Recibe master,controller, username y is_admin de funciones.py
        """Self se usa para hacer un atributo de otra funcion o clase como propio."""
        super().__init__(master)
        self.controller = controller #Recibe controller y lo hace un atributo propio 
        self.username = username #Recibe username(Nombre de Usuario) y lo hace un atributo propio 
        self.is_admin = is_admin #Recibe is_admin y lo hace un atributo propio, en este caso (1 o 0) 

        titulo = f"Mis Trapitos - Inicio - {self.username}" #Crea un atributo titulo que en este caso llevara la palabra Inicio + lo que haya en username
        if self.is_admin:#validador de usuario tipo administrador, si is_admin es true entra al if.
            titulo += "Administrador" #Si es administrador agregar "administrador" al titulo.
        self.title(titulo)#Inserta titulo en la parte de arriba en la interfaz
        #icono
        icono = tk.PhotoImage(file="icono.png")
        self.tk.call("wm", "iconphoto", self._w, icono)

        self.state('zoomed')#Tamaño de ventana(<ancho>x<alto>±<posición_x>±<posición_y>)
        self._make_menu()# Crea el menú superior
        self._make_buttons()  # Crea los botones en la parte inferior
        
    
    
    #----Funcion de Menu en interfaz ----
    def _make_menu(self):
        self.barra_menu = tk.Menu(self) #Agrega el elemento menu de tkinter a barra_menu
        self.config(menu=self.barra_menu) #Agrega la barra de menu a menu y menu a config
        #Menu
        menu_opciones = tk.Menu(self.barra_menu, tearoff=0, bg="lightblue", fg="black") #Se aagrega un submenu que se desplega en barra_menu y su configuracion visual.
        menu_opciones.add_command(label="Ajustes", command= SettingView) #añade un boton al submenu con la opcion de ajustes, por el momento no hace nada.
        #Opciones solo para administrador
        if self.is_admin: #validador si is_admin es true mostrara lo siguiente en el menu
            menu_opciones.add_separator() #Añade un separador en el submenu
            menu_opciones.add_command(label="Nuevo Usuario", command=self.controller.show_register) 
            """añade un boton al submenu con la opcion para añadir nuevo usuario y manda a llamar controller para abrir la interfaz de show_register"""
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Cerrar sesión", command=self.controller.logout)
        """añade un boton al submenu con la opcion para añadir nuevo usuario y manda a llamar controller para abrir la interfaz de login"""
        menu_opciones.add_command(label="Salir", command=sys.exit)
        """añade un boton al submenu con la opcion para Salir y hace uso de la biblioteca Sys,
        esto es para que se cierre completamente el programa y que cualquier subproceso que haya quedado, se termine completamente."""
        self.barra_menu.add_cascade(label="Opciones", menu=menu_opciones)#Agrega el boton "Opciones" a la barra de menu

    
    def _make_buttons(self):
        # Botón en posición exacta (x=100, y=400)
        btn1 = tk.Button(self, text="Posición exacta", width=15)
        btn1.place(x=100, y=400)
        
        # Botón relativo al tamaño de la ventana
        btn2 = tk.Button(self, text="Relativo", width=15)
        btn2.place(relx=0.5, rely=0.9, anchor='center')  # 50% ancho, 90% alto