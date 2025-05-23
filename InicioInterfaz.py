#INTERFAZ DE INICIO (no confundir con login)
#----Bibliotecas----
import tkinter as tk #Tkinter que es la libreria para la interfaz, que se importa como tk =Tkinter
import sys #Importamos Sys 
from ajustesinterfaz import SettingView
from tkinter import messagebox

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
        self.button_frame = tk.Frame(self.main_frame, width=400, bg='lightgray')
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
            
            btn_baja = tk.Button(self.button_frame, text="Baja de Producto", width=20, command=self.show_baja_producto_content)
            btn_baja.pack(pady=10, padx=10, fill=tk.X)
        
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
        izquierda_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        derecha_frame = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        # --- Izquierda: ingreso de datos ---
        tk.Label(izquierda_frame, text="Nueva Venta", font=('Arial', 18), bg='#f7f7f7').pack(pady=10)

        tk.Label(izquierda_frame, text="ID de Producto:", bg='#f7f7f7').pack()
        id_frame = tk.Frame(izquierda_frame, bg='#f7f7f7')
        id_frame.pack(pady=5)
        self.entry_id = tk.Entry(id_frame, width=30)
        self.entry_id.pack(side='left')
        btn_buscar = tk.Button(id_frame, text="🔍", width=2, command=self.buscar_producto_por_nombre)
        btn_buscar.pack(side='left', padx=5)

        tk.Label(izquierda_frame, text="Cantidad:", bg='#f7f7f7').pack()
        cantidad_spinbox = tk.Spinbox(izquierda_frame, from_=1, to=100, width=30)
        cantidad_spinbox.pack(pady=5)

        tk.Label(izquierda_frame, text="Cliente:", bg='#f7f7f7').pack()
        tk.Entry(izquierda_frame, width=33).pack(pady=5)

        # 👇 Botones
        btn_agregar = tk.Button(izquierda_frame, text="Agregar Producto")
        btn_agregar.pack(pady=5)


        btn_registrar = tk.Button(izquierda_frame, text="Registrar Venta", command=self.registrar_venta)
        btn_registrar.pack(pady=5)

        # --- Derecha: resumen de productos ---
        tk.Label(derecha_frame, text="Resumen de Venta", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)

        self.resumen_inventario = tk.Listbox(derecha_frame, width=100, height=50)
        self.resumen_inventario.pack(padx=10, pady=10)



#---------------------------FUNCIONES DE PRUEBA----------------------------------------------
    def buscar_producto_por_nombre(self):
        # Crear ventana de búsqueda
        busqueda_window = tk.Toplevel(self)
        busqueda_window.title("Buscar Producto")
        busqueda_window.resizable(False, False)
        
        # Frame para entrada de búsqueda
        search_frame = tk.Frame(busqueda_window)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(search_frame, text="Nombre del producto:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Botón de búsqueda
        def realizar_busqueda():
            nombre = search_entry.get().strip()
            if nombre:
                resultados = self.controller.model.buscar_productos_por_nombre(nombre)
                mostrar_resultados(resultados)
        
        search_btn = tk.Button(search_frame, text="Buscar", command=realizar_busqueda)
        search_btn.pack(side=tk.LEFT)
        
        # Frame para resultados
        results_frame = tk.Frame(busqueda_window)
        results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Lista de resultados
        resultados_listbox = tk.Listbox(results_frame, width=60, height=10)
        resultados_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        resultados_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=resultados_listbox.yview)
        
        # Función para mostrar resultados
        def mostrar_resultados(productos):
            resultados_listbox.delete(0, tk.END)
            for producto in productos:
                resultados_listbox.insert(tk.END, f"{producto[0]} | {producto[1]} | Stock: {producto[2]}")
        
        # Función para seleccionar producto - VERSIÓN CORREGIDA
        def seleccionar_producto():
            seleccion = resultados_listbox.curselection()
            if seleccion:
                producto_info = resultados_listbox.get(seleccion[0])
                id_producto = producto_info.split(" | ")[0]  # Extraer el ID
                
                # Actualizar directamente el entry_id que ya tenemos como atributo
                if hasattr(self, 'entry_id'):
                    self.entry_id.delete(0, tk.END)
                    self.entry_id.insert(0, id_producto)
                    busqueda_window.destroy()
        
        select_btn = tk.Button(busqueda_window, text="Seleccionar", command=seleccionar_producto)
        select_btn.pack(pady=10)
        
        # Hacer que la ventana sea modal
        busqueda_window.grab_set()
        busqueda_window.transient(self)
        busqueda_window.wait_window()
    def registrar_venta(self):
        print("Se registro una venta.")
    
    def show_inventario_content(self):
        self.clear_content_frame()
        
        # Inicializar el diccionario si no existe
        if not hasattr(self, 'entries_inventario'):
            self.entries_inventario = {}
        else:
            # Limpiar el diccionario de entradas anteriores
            self.entries_inventario.clear()

        izquierda = tk.Frame(self.content_frame, bg='#f7f7f7')
        izquierda.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        derecha = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        tk.Label(izquierda, text="Capturar Producto", font=('Arial', 18), bg='white').pack(pady=10)

        campos = [
            ("ID:", "id"),
            ("Nombre del producto:", "nombre"),
            ("Cantidad en stock:", "cantidad"),
            ("Proveedor:", "proveedor"),
            ("Tipo de prenda:", "tipo"),
            ("Talla (P, M, G o número):", "talla"),
            ("Para (Hombre, Mujer, Niño, Niña):", "persona")
        ]
        self.entries_inventario = {}
        for label_text, key in campos:
            tk.Label(izquierda, text=label_text, bg='white').pack()
            entry = tk.Entry(izquierda, width=40)
            entry.pack(pady=5)
            self.entries_inventario[key] = entry

        # Botones
        btn_guardar = tk.Button(izquierda, text="Guardar", command=self.guardar_producto)
        btn_guardar.pack(pady=5)
        btn_limpiar = tk.Button(izquierda, text="Limpiar", command=self.limpiar_entradas_inventario)
        btn_limpiar.pack(pady=5)

        # Lista a la derecha
        tk.Label(derecha, text="Resumen de Inventario", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)
        self.resumen_inventario = tk.Listbox(derecha, width=100, height=50)
        self.resumen_inventario.pack(padx=10, pady=10)

        self.cargar_resumen_inventario()
    
    def guardar_producto(self):
        datos = {k: v.get().strip() for k, v in self.entries_inventario.items() 
                if hasattr(self, 'entries_inventario') and k in self.entries_inventario and v.winfo_exists()}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not datos["cantidad"].isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número")
            return

        exito = self.controller.model.agregar_producto(
            datos["id"], datos["nombre"], int(datos["cantidad"]), 
            datos["proveedor"], datos["tipo"], datos["talla"], datos["persona"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            # Solo limpiar si las entradas existen
            if hasattr(self, 'entries_inventario'):
                self.limpiar_entradas_inventario()
            self.cargar_resumen_inventario()
        else:
            messagebox.showerror("Error", "Ya existe un producto con ese ID")

    def show_baja_producto_content(self):
        self.clear_content_frame()

        # Frame principal dividido en dos
        izquierda_frame = tk.Frame(self.content_frame, bg='#f7f7f7')
        izquierda_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        derecha_frame = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        # --- Izquierda: ingreso de datos ---
        tk.Label(izquierda_frame, text="Baja de Producto", font=('Arial', 18), bg='#f7f7f7').pack(pady=10)

        tk.Label(izquierda_frame, text="ID del Producto:", bg='#f7f7f7').pack()
        entry_id = tk.Entry(izquierda_frame, width=30)
        entry_id.pack(pady=5)

        tk.Label(izquierda_frame, text="Cantidad a dar de baja:", bg='#f7f7f7').pack()
        entry_cantidad = tk.Entry(izquierda_frame, width=30)
        entry_cantidad.pack(pady=5)

        # Función para confirmar la baja del producto
        def confirmar_baja():
            id_producto = entry_id.get().strip()
            cantidad = entry_cantidad.get().strip()

            if not id_producto or not cantidad.isdigit():
                messagebox.showerror("Error", "ID y cantidad válidos son requeridos")
                return

            cantidad = int(cantidad)
            resultado = self.controller.model.disminuir_cantidad_producto(id_producto, cantidad)

            if resultado == "parcial":
                messagebox.showinfo("Actualizado", "Cantidad actualizada correctamente.")
            elif resultado == "total":
                messagebox.showinfo("Eliminado", "Producto eliminado del inventario.")
            elif resultado == "excede":
                messagebox.showerror("Error", "La cantidad ingresada excede el stock.")
            elif resultado == "no_encontrado":
                messagebox.showerror("Error", "Producto no encontrado.")

            self.cargar_resumen_inventario()

        # Botón para confirmar la baja
        tk.Button(izquierda_frame, text="Confirmar Baja", command=confirmar_baja).pack(pady=10)

        # --- Derecha: resumen de inventario ---
        tk.Label(derecha_frame, text="Resumen de Inventario", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)

        # Usar el mismo nombre que en show_inventario_content
        self.resumen_inventario = tk.Listbox(derecha_frame, width=100, height=50)
        self.resumen_inventario.pack(padx=10, pady=10)

        # Cargar inventario en la lista
        self.cargar_resumen_inventario()

    def cargar_resumen_inventario(self):
        # Verificar si el Listbox existe
        if hasattr(self, "resumen_inventario"):
            self.resumen_inventario.delete(0, tk.END)
            datos = self.controller.model.obtener_inventario()
            for row in datos:
                self.resumen_inventario.insert(
                    tk.END,
                    f"{row[0]} | {row[1]} | Stock: {row[2]} | {row[3]} | Tipo: {row[4]} | Talla: {row[5]} | Para: {row[6]}"
                )

    def limpiar_entradas_inventario(self):
        # Verificar que el diccionario entries_inventario existe y tiene elementos
        if hasattr(self, 'entries_inventario') and self.entries_inventario:
            # Crear una copia de las claves para evitar problemas si se modifica durante la iteración
            for key in list(self.entries_inventario.keys()):
                entry = self.entries_inventario[key]
                try:
                    # Verificar si el widget aún existe
                    if entry.winfo_exists():
                        entry.delete(0, tk.END)
                except tk.TclError:
                    # Si el widget ya no existe, eliminarlo del diccionario
                    del self.entries_inventario[key]

    def show_clientes_content(self):
        """Muestra el contenido para consultar clientes"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Consultar Clientes", 
                font=('Arial', 18), bg='white').pack(pady=20)
        
        