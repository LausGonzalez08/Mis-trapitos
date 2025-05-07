#INTERFAZ DE LOGIN(no confundir con login)
#----Bibliotecas----
import tkinter as tk
from tkinter import messagebox
import sys

#----INTERFAZ DE LOGIN----
class LoginView(tk.Toplevel):
    def __init__(self, master, controller):#Recibe master y controller
        super().__init__(master)
        self.controller = controller #Hace propio controller para poder usarlo
        self.title("Login") #Titulo de la ventana
        self.attributes('-fullscreen', True) #Tamaño de ventana(<ancho>x<alto>±<posición_x>±<posición_y>)
        self._make_widgets() #Llama a la funcion make_widgets
        
    #----WIDGET----
    def _make_widgets(self): #funcion para crealo que va dentro de la venta principal
        try:
            self.logo_image = tk.PhotoImage(file="usuario.png")
            logo_label = tk.Label(self, image=self.logo_image)
            logo_label.pack(pady=10)
        except:
            # Si hay error al cargar la imagen, mostramos un mensaje o simplemente continuamos
            print("No se pudo cargar la imagen del logo")
            pass
        
        self.marco_login = tk.Frame(self) #Agrega el elemento Frame de tkinter a marco_login
        self.marco_login.pack(pady=10) #

        # Campos de usuario y contraseña
        tk.Label(self.marco_login, text="Usuario:").grid(row=0, column=0, sticky="e", pady=0)#Zona de texto Usuario
        self.entry_usuario = tk.Entry(self.marco_login) #Zona de entrada de texto
        self.entry_usuario.grid(row=0, column=1) #Tamaño

        tk.Label(self.marco_login, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=0) #Zona de texto Contraseña
        self.entry_contraseña = tk.Entry(self.marco_login, show="*") #Zona de entrada de texto y pone * por caracter ingresado
        self.entry_contraseña.grid(row=1, column=1)#Tamaño

        # Marco para botones
        marco_botones = tk.Frame(self)#Agrega el elemento Frame de tkinter a marco_botones
        marco_botones.pack(pady=10)#Tamaño

        btn_login = tk.Button(marco_botones, text="Ingresar", command=self.controller.login) #Boton para iniciar sesion
        btn_login.grid(row=0, column=0, padx=0)#Tamaño de boton
        btn_login = tk.Button(marco_botones, text="Salir", command=sys.exit) #Boton para Salir
        btn_login.grid(row=0, column=1, padx=10)


#----Interfaz de Restro de nuevo usuario----
class RegisterView(tk.Toplevel):
    def __init__(self, master, controller):#Recibe master y controller
        super().__init__(master)
        self.controller = controller #Hace propio controller
        self.title("Registro") #Titulo de la ventana
        self.geometry("300x350+400+300") #Tamaño de ventana(<ancho>x<alto>±<posición_x>±<posición_y>)
        self._make_widgets() #Crea el widget
        
    def _make_widgets(self): #Funcion para crear lo que va dentro de la ventana
        tk.Label(self, text="Nuevo usuario:").pack(pady=(10,0)) #Zona de texto Nuevo Usuario
        self.entry_nuevo_usuario = tk.Entry(self) #Zona de entrada de texto
        self.entry_nuevo_usuario.pack() #coloca los widgets uno debajo del otro (por defecto, en vertical)
        
        tk.Label(self, text="Nueva contraseña:").pack(pady=(10,0))#Zona de texto Nueva contraseña
        self.entry_nueva_contraseña = tk.Entry(self, show="*")#Zona de entrada de texto y oculta lo ingresado con *
        self.entry_nueva_contraseña.pack()#coloca los widgets uno debajo del otro (por defecto, en vertical)
        
        tk.Label(self, text="Confirmar contraseña:").pack(pady=(10,0))#Zona de texto Confirmar contraseña
        self.entry_confirmar_contraseña = tk.Entry(self, show="*")#Zona de entrada de texto y oculta lo ingresado con *
        self.entry_confirmar_contraseña.pack()#coloca los widgets uno debajo del otro (por defecto, en vertical)

        # Selección del tipo de usuario
        self.tipo_usuario = tk.StringVar(value="empleado")
        frame_tipo = tk.Frame(self) #Agrega el elemento Frame de tkinter a frame_tipo
        frame_tipo.pack(pady=5) #Coloca el widget en la posicion Y=5 pixeles
        tk.Label(frame_tipo, text="Tipo de usuario:").pack(anchor="w")#Zona de texto 
        tk.Radiobutton(frame_tipo, text="Administrador", variable=self.tipo_usuario, value="admin").pack(anchor="w") #Crea el selecionador para Administrador
        tk.Radiobutton(frame_tipo, text="Empleado", variable=self.tipo_usuario, value="empleado").pack(anchor="w") #Crea el seleccionador para Empleado

        btn_guardar = tk.Button(self, text="Registrar", command=self.controller.register_user) #Crea el boton el cual mandara a llamar a funciones>controller>register_user
        btn_guardar.pack(pady=10) #Coloca el widget en la posicion Y=10 pixeles
        
"""pack() sencillo y rápido (vertical u horizontal).
grid() para ubicarlos en filas y columnas.
place() para posicionamiento exacto con coordenadas.
pady = Tamaño en Y
padx = Tamaño en X
pack = agrega lo de la funcion en la ventana principal
Entry = Zona para ingresar texto.
        """
