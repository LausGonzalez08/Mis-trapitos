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
        self.resizable(False, False)
        self.state('zoomed')#Tamaño de ventana(<ancho>x<alto>±<posición_x>±<posición_y>)
        #self._make_menu()# Crea el menú superior
        #self._make_buttons()  # Crea los botones en la parte inferior
        
        # Frame principal para organizar la interfaz
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para los botones (lado izquierdo)
        self.button_frame = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Frame para el contenido dinámico (lado derecho)
        self.content_frame = tk.Frame(self.main_frame, bg='white')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._make_menu()
        self._make_buttons()
        
        # Mostrar contenido inicial (opcional)
        self.show_default_content()
    
    #----Funcion de Menu en interfaz ----
    def _make_menu(self):
        self.barra_menu = tk.Menu(self) #Agrega el elemento menu de tkinter a barra_menu
        self.config(menu=self.barra_menu) #Agrega la barra de menu a menu y menu a config
        #Menu
        menu_opciones = tk.Menu(self.barra_menu, tearoff=0, bg="lightblue", fg="black") #Se aagrega un submenu que se desplega en barra_menu y su configuracion visual.
        menu_opciones.add_command(label="Datos de Usuario", command=lambda: self.controller.show_settings(self.username)) #añade un boton al submenu con la opcion de ajustes, por el momento no hace nada.
        #Opciones solo para administrador
        if self.is_admin: #validador si is_admin es true mostrara lo siguiente en el menu
            menu_opciones.add_separator() #Añade un separador en el submenu
            menu_opciones.add_command(label="Nuevo Usuario", command=self.controller.show_register) 
            menu_opciones.add_separator()
            menu_opciones.add_command(label="Datos de Usuarios", command=self.controller.show_user_data)
            """añade un boton al submenu con la opcion para añadir nuevo usuario y manda a llamar controller para abrir la interfaz de show_register"""
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Cerrar sesión", command=self.controller.logout)
        """añade un boton al submenu con la opcion para añadir nuevo usuario y manda a llamar controller para abrir la interfaz de login"""
        menu_opciones.add_command(label="Salir", command=sys.exit)
        """añade un boton al submenu con la opcion para Salir y hace uso de la biblioteca Sys,
        esto es para que se cierre completamente el programa y que cualquier subproceso que haya quedado, se termine completamente."""
        self.barra_menu.add_cascade(label="Opciones", menu=menu_opciones)#Agrega el boton "Opciones" a la barra de menu

    
    def _make_buttons(self):
            # Botones con comandos que cambian el contenido
            btn_venta = tk.Button(self.button_frame, text="Generar venta", width=20,
                                command=self.show_venta_content)
            btn_venta.pack(pady=10, padx=10, fill=tk.X)
            
            btn_inventario = tk.Button(self.button_frame, text="Capturar Inventario", width=20,
                                    command=self.show_inventario_content)
            btn_inventario.pack(pady=10, padx=10, fill=tk.X)
            
            btn_clientes = tk.Button(self.button_frame, text="Consultar Clientes", width=20,
                                command=self.show_clientes_content)
            btn_clientes.pack(pady=10, padx=10, fill=tk.X)
    
    def clear_content_frame(self):
        """Limpia el frame de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_default_content(self):
        """Muestra contenido por defecto"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Bienvenido al sistema", 
                font=('Arial', 24), bg='white').pack(pady=50)
    
    def show_venta_content(self):
        self.clear_content_frame()

        # Frame principal dividido en dos
        izquierda_frame = tk.Frame(self.content_frame, bg='#f7f7f7')
        izquierda_frame.pack(side='left', fill='both',  expand=True, padx=20, pady=20)

        derecha_frame = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        # --- Izquierda: ingreso de datos ---
        tk.Label(izquierda_frame, text="Nueva Venta", font=('Arial', 18), bg='white').pack(pady=10)

        tk.Label(izquierda_frame, text="ID de Producto:", bg='white').pack()
        id_frame = tk.Frame(izquierda_frame, bg='white')
        id_frame.pack(pady=5)
        entry_id = tk.Entry(id_frame, width=30)
        entry_id.pack(side='left')
        btn_buscar = tk.Button(id_frame, text="🔍", width=2, command=self.buscar_producto_por_nombre)
        btn_buscar.pack(side='left', padx=5)

        tk.Label(izquierda_frame, text="Cantidad:", bg='white').pack()

        cantidad_spinbox = tk.Spinbox(izquierda_frame, from_=1, to=100, width=30)
        cantidad_spinbox.pack(pady=5)

        tk.Label(izquierda_frame, text="Cliente:", bg='white').pack()
        tk.Entry(izquierda_frame, width=33).pack(pady=5)

        # 👇 Estos botones ahora sí se mostrarán correctamente
        btn_agregar = tk.Button(izquierda_frame, text="Agregar Producto", command=self.agregar_producto)
        btn_agregar.pack(pady=5)

        btn_registrar = tk.Button(izquierda_frame, text="Registrar Venta", command=self.registrar_venta)
        btn_registrar.pack(pady=5)

        # --- Derecha: resumen de productos ---
        tk.Label(derecha_frame, text="Resumen de Venta", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)

        self.resumen_listbox = tk.Listbox(derecha_frame, width=100, height=50)
        self.resumen_listbox.pack(padx=10, pady=10)


#---------------------------FUNCIONES DE PRUEBA----------------------------------------------
    def agregar_producto(self):
        # Esto lo puedes reemplazar por lógica real
        self.resumen_listbox.insert(tk.END, "Producto X - Cantidad: 1")
        print("Producto agregado al resumen.")

    def buscar_producto_por_nombre(self):
        # Aquí va la lógica que deseas implementar, por ahora solo imprime
        print("Buscando producto por nombre...")
        
    def registrar_venta(self):
        print("Se registro una venta.")
    
    def show_inventario_content(self):
        """Muestra el contenido para capturar inventario"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Capturar Inventario", 
                font=('Arial', 18), bg='white').pack(pady=20)
    def show_clientes_content(self):
        """Muestra el contenido para consultar clientes"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Consultar Clientes", 
                font=('Arial', 18), bg='white').pack(pady=20)
        