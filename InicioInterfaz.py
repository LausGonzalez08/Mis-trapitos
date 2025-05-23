#INTERFAZ DE INICIO (no confundir con login)
#----Bibliotecas----
import tkinter as tk #Tkinter que es la libreria para la interfaz, que se importa como tk =Tkinter
import sys #Importamos Sys 
from ajustesinterfaz import SettingView
from tkinter import messagebox, ttk
from datetime import datetime

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
        self.resizable(True, True)
        self.state('normal')#Tamaño de ventana(<ancho>x<alto>±<posición_x>±<posición_y>)
        #self._make_menu()# Crea el menú superiorF
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
        self._make_buttons(self.is_admin)
        
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

    
    def _make_buttons(self, is_admin=False):
        """Crea los botones de la interfaz según los permisos del usuario"""
        self.is_admin = is_admin  # Guardar el estado de admin como atributo
        
        # Botones comunes para todos los usuarios
        btn_venta = tk.Button(self.button_frame, text="Generar venta", width=20,
                            command=self.show_venta_content)
        btn_venta.pack(pady=10, padx=10, fill=tk.X)
        
        btn_inventario = tk.Button(self.button_frame, text="Capturar Inventario", width=20,
                                command=self.show_inventario_content)
        btn_inventario.pack(pady=10, padx=10, fill=tk.X)
        
        btn_baja = tk.Button(self.button_frame, text="Baja de Producto", width=20,
                            command=self.show_baja_producto_content)
        btn_baja.pack(pady=10, padx=10, fill=tk.X)
        
        btn_clientes = tk.Button(self.button_frame, text="Consultar Clientes", width=20,
                            command=self.show_clientes_content)
        btn_clientes.pack(pady=10, padx=10, fill=tk.X)

        btn_proveedores = tk.Button(self.button_frame, text="Consultar proveedores", width=20,
                                command=self.show_proveedores_content)
        btn_proveedores.pack(pady=10, padx=10, fill=tk.X)
        
        # Botones solo para administradores
        if self.is_admin:
            btn_descuentos = tk.Button(self.button_frame, text="Agregar descuentos", width=20,
                                    command=self.show_descuentos_content)
            btn_descuentos.pack(pady=10, padx=10, fill=tk.X)
            
            # Puedes agregar más botones de admin aquí si es necesario
            btn_admin_extra = tk.Button(self.button_frame, text="Opciones Admin", width=20,
                                    command=self.show_admin_panel)
            btn_admin_extra.pack(pady=10, padx=10, fill=tk.X)
    
    def actualizar_permisos(self, is_admin):
        """Actualiza los botones según los nuevos permisos"""
        self.is_admin = is_admin
        # Limpiar el frame de botones
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        # Volver a crear los botones con los nuevos permisos
        self._make_buttons(self.is_admin)
        
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
        self.productos_venta = []  # Lista para almacenar productos de la venta

        # Frame principal
        main_frame = tk.Frame(self.content_frame, bg='#f7f7f7')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame izquierdo (formulario)
        left_frame = tk.Frame(main_frame, bg='#f7f7f7')
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Frame derecho (resumen)
        right_frame = tk.Frame(main_frame, bg='#f7f7f7')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Formulario de venta ---
        tk.Label(left_frame, text="Nueva Venta", font=('Arial', 18), bg='#f7f7f7').pack(pady=10)

        # Campo ID Producto
        tk.Label(left_frame, text="ID de Producto:", bg='#f7f7f7').pack()
        id_frame = tk.Frame(left_frame, bg='#f7f7f7')
        id_frame.pack(pady=5)
        self.entry_id = tk.Entry(id_frame, width=30)
        self.entry_id.pack(side=tk.LEFT)
        btn_buscar = tk.Button(id_frame, text="🔍", width=2, command=self.buscar_producto_por_nombre)
        btn_buscar.pack(side=tk.LEFT, padx=5)

        # Campo Cantidad
        tk.Label(left_frame, text="Cantidad:", bg='#f7f7f7').pack()
        self.cantidad_spinbox = tk.Spinbox(left_frame, from_=1, to=100, width=30)
        self.cantidad_spinbox.pack(pady=5)

        # Campo Cliente
        tk.Label(left_frame, text="Cliente:", bg='#f7f7f7').pack()
        clientes = [f"{cliente[1]} (ID: {cliente[0]})" for cliente in self.controller.model.obtener_clientes()]
        self.combo_cliente = ttk.Combobox(left_frame, width=30, values=clientes)
        self.combo_cliente.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(left_frame, bg='#f7f7f7')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Agregar Producto", command=self.agregar_producto_venta).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Registrar Venta", command=self.registrar_venta).pack(side=tk.LEFT, padx=5)

        # --- Resumen de venta ---
        tk.Label(right_frame, text="Resumen de Venta", font=('Arial', 16), bg='#f7f7f7').pack()

        # Frame para el listbox y scrollbar
        list_frame = tk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.resumen_listbox = tk.Listbox(
            list_frame, 
            width=80, 
            height=20,
            yscrollcommand=scrollbar.set
        )
        self.resumen_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resumen_listbox.yview)

        # Frame para botones de eliminar
        self.buttons_frame = tk.Frame(right_frame)
        self.buttons_frame.pack(fill=tk.X)

        # Total
        total_frame = tk.Frame(right_frame, bg='#f7f7f7')
        total_frame.pack(fill=tk.X, pady=5)
        tk.Label(total_frame, text="Total:", font=('Arial', 12, 'bold'), bg='#f7f7f7').pack(side=tk.LEFT)
        self.lbl_total = tk.Label(total_frame, text="$0.00", font=('Arial', 12, 'bold'), bg='#f7f7f7')
        self.lbl_total.pack(side=tk.LEFT, padx=10)

    def show_descuentos_content(self):
        """Muestra la interfaz de gestión de descuentos"""
        self.clear_content_frame()
        
        # Frame principal
        main_frame = tk.Frame(self.content_frame, bg='#f7f7f7')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para formulario
        form_frame = tk.Frame(main_frame, bg='#f7f7f7')
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Frame para lista de descuentos
        list_frame = tk.Frame(main_frame, bg='#f7f7f7')
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(form_frame, text="Agregar Descuento", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)
        
        # Campos del formulario
        campos = [
            ("ID Producto:", "producto_id"),
            ("Nombre Producto:", "producto_nombre"),
            ("Precio Actual:", "precio_actual"),
            ("Precio con Descuento:", "precio_descuento"),
            ("Fecha Inicio (YYYY-MM-DD):", "fecha_inicio"),
            ("Fecha Fin (YYYY-MM-DD):", "fecha_fin")
        ]
        
        self.entries_descuento = {}
        for label, key in campos:
            tk.Label(form_frame, text=label, bg='#f7f7f7').pack()
            
            if key == "producto_id":
                # Combobox para seleccionar producto
                productos = self.controller.model.obtener_inventario()
                producto_list = [f"{p[0]} - {p[1]}" for p in productos]
                combo = ttk.Combobox(form_frame, width=25, values=producto_list)
                combo.pack(pady=5)
                self.entries_descuento[key] = combo
                
                # Botón para buscar producto
                btn_buscar = tk.Button(form_frame, text="Buscar", command=self.buscar_producto_descuento)
                btn_buscar.pack(pady=5)
            else:
                entry = tk.Entry(form_frame, width=30)
                entry.pack(pady=5)
                self.entries_descuento[key] = entry
        
        # Botón para agregar descuento
        btn_agregar = tk.Button(form_frame, text="Agregar Descuento", command=self.agregar_descuento)
        btn_agregar.pack(pady=15)
        
        # Lista de descuentos activos
        tk.Label(list_frame, text="Descuentos Activos", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_descuentos = tk.Listbox(
            list_frame, 
            width=80, 
            height=20,
            yscrollcommand=scrollbar.set
        )
        self.lista_descuentos.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_descuentos.yview)
        
        self.actualizar_lista_descuentos()
    
    def buscar_producto_descuento(self):
        """Busca y completa los datos del producto para el descuento"""
        seleccion = self.entries_descuento["producto_id"].get()
        if not seleccion:
            return
        
        producto_id = seleccion.split(" - ")[0]
        producto = self.controller.model.obtener_producto_completo(producto_id)
        
        if producto:
            self.entries_descuento["producto_nombre"].delete(0, tk.END)
            self.entries_descuento["producto_nombre"].insert(0, producto[1])
            
            self.entries_descuento["precio_actual"].delete(0, tk.END)
            self.entries_descuento["precio_actual"].insert(0, str(producto[3]))

    def agregar_descuento(self):
        """Agrega un nuevo descuento a la base de datos"""
        try:
            producto_id = self.entries_descuento["producto_id"].get().split(" - ")[0]
            producto_nombre = self.entries_descuento["producto_nombre"].get()
            precio_anterior = float(self.entries_descuento["precio_actual"].get())
            precio_descuento = float(self.entries_descuento["precio_descuento"].get())
            fecha_inicio = self.entries_descuento["fecha_inicio"].get()
            fecha_fin = self.entries_descuento["fecha_fin"].get()
            
            # Validar fechas
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            if precio_descuento >= precio_anterior:
                messagebox.showerror("Error", "El precio con descuento debe ser menor al precio actual")
                return
                
            if self.controller.model.agregar_descuento(
                producto_id, producto_nombre, precio_anterior, 
                precio_descuento, fecha_inicio, fecha_fin
            ):
                messagebox.showinfo("Éxito", "Descuento agregado correctamente")
                self.actualizar_lista_descuentos()
                self.limpiar_campos_descuento()
                # Aplicar descuentos inmediatamente si corresponde
                self.controller.model.aplicar_descuentos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el descuento")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def actualizar_lista_descuentos(self):
        """Actualiza la lista de descuentos activos"""
        self.lista_descuentos.delete(0, tk.END)
        descuentos = self.controller.model.obtener_descuentos_activos()
        
        for descuento in descuentos:
            texto = (
                f"Producto: {descuento[2]} (ID: {descuento[1]}) | "
                f"Precio: ${descuento[3]:.2f} → ${descuento[4]:.2f} | "
                f"Válido: {descuento[5]} a {descuento[6]}"
            )
            self.lista_descuentos.insert(tk.END, texto)

    def limpiar_campos_descuento(self):
        """Limpia los campos del formulario de descuentos"""
        for entry in self.entries_descuento.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')
    def show_admin_panel(self):
        """Muestra el panel de administración"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Panel de Administración", 
                font=('Arial', 18), bg='white').pack(pady=20)
        # Implementa las funciones administrativas aquí
    def actualizar_lista_clientes(self, combobox):
        """Actualiza la lista de clientes en el Combobox"""
        clientes = [f"{cliente[1]} (ID: {cliente[0]})" for cliente in self.controller.model.obtener_clientes()]
        combobox['values'] = clientes


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
    
    def agregar_producto_venta(self):
        try:
            # Validar campos
            id_producto = self.entry_id.get().strip()
            cantidad = self.cantidad_spinbox.get()
            cliente = self.combo_cliente.get()
            
            if not id_producto:
                messagebox.showerror("Error", "Ingrese ID de producto")
                return
                
            if not cantidad.isdigit() or int(cantidad) <= 0:
                messagebox.showerror("Error", "Cantidad inválida")
                return
                
            if not cliente:
                messagebox.showerror("Error", "Seleccione un cliente")
                return

            # Obtener producto
            producto = self.controller.model.obtener_producto_completo(id_producto)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
                
            # Verificar stock
            if int(cantidad) > producto[2]:  # producto[2] = stock
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto[2]}")
                return

            # Agregar a la lista
            self.productos_venta.append({
                'id': producto[0],
                'nombre': producto[1],
                'cantidad': int(cantidad),
                'precio': float(producto[3]),
                'talla': producto[6],
                'proveedor': producto[4],
                'tipo': producto[5],
                'persona': producto[7],
                'subtotal': int(cantidad) * float(producto[3])
            })

            # Actualizar resumen
            self.actualizar_resumen_venta()
            
            # Limpiar campos
            self.entry_id.delete(0, tk.END)
            self.cantidad_spinbox.delete(0, tk.END)
            self.cantidad_spinbox.insert(0, "1")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def registrar_venta(self):
        if not self.productos_venta:
            messagebox.showerror("Error", "No hay productos en la venta")
            return
        
        cliente = self.combo_cliente.get()
        if not cliente:
            messagebox.showerror("Error", "Debe seleccionar un cliente")
            return
        
        try:
            # Extraer datos del cliente
            id_cliente = cliente.split("(ID: ")[1][:-1]
            nombre_cliente = cliente.split(" (ID:")[0]
            
            # Calcular total
            total = sum(p['subtotal'] for p in self.productos_venta)
            
            # Registrar venta en la base de datos
            venta_id = self.controller.model.registrar_venta_completa(
                id_cliente=id_cliente,
                nombre_cliente=nombre_cliente,
                usuario=self.username,
                total=total,
                productos=self.productos_venta
            )
            
            if venta_id:
                messagebox.showinfo("Éxito", f"Venta registrada con ID: {venta_id}")
                self.productos_venta = []
                self.actualizar_resumen_venta()
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar venta: {str(e)}")
    def actualizar_resumen_venta(self):
        # Limpiar widgets anteriores
        self.resumen_listbox.delete(0, tk.END)
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        total = 0.0
        
        # Agregar productos al listbox
        for i, producto in enumerate(self.productos_venta):
            texto = f"{producto['nombre']} | Cant: {producto['cantidad']} | ${producto['precio']:.2f} c/u | Subtotal: ${producto['subtotal']:.2f}"
            self.resumen_listbox.insert(tk.END, texto)
            
            # Crear botón de eliminar
            btn = tk.Button(
                self.buttons_frame, 
                text="X", 
                command=lambda idx=i: self.eliminar_producto_venta(idx),
                bg='red', fg='white'
            )
            btn.pack(side=tk.TOP, pady=2)
            
            total += producto['subtotal']
        
        # Actualizar total
        self.lbl_total.config(text=f"${total:.2f}")

    def eliminar_producto_venta(self, index):
        self.productos_venta.pop(index)
        self.actualizar_resumen_venta()
    def registrar_venta(self):
        if not self.productos_venta:
            messagebox.showerror("Error", "No hay productos en la venta")
            return
            
        cliente = self.combo_cliente.get()
        if not cliente:
            messagebox.showerror("Error", "Seleccione un cliente")
            return
        
        try:
            # Extraer ID del cliente
            id_cliente = cliente.split("(ID: ")[1][:-1]
            nombre_cliente = cliente.split(" (ID:")[0]
            
            # Calcular total
            total = sum(p['subtotal'] for p in self.productos_venta)
            
            # Registrar venta
            venta_id = self.controller.model.registrar_venta_completa(
                id_cliente=id_cliente,
                nombre_cliente=nombre_cliente,
                usuario=self.username,
                total=total,
                productos=self.productos_venta
            )
            
            if venta_id:
                messagebox.showinfo("Éxito", f"Venta registrada (ID: {venta_id})")
                self.productos_venta = []
                self.actualizar_resumen_venta()
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar venta: {str(e)}")
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
            ("Precio por unidad al publico:", "precio_unitario"),
            ("Proveedor:", "proveedor"),
            ("Tipo de prenda:", "tipo"),
            ("Talla (P, M, G o número):", "talla"),
            ("Para (Hombre, Mujer, Niño, Niña):", "persona")
        ]
        
        self.entries_inventario = {}
        
        # Obtener la lista de proveedores para el Combobox
        proveedores = [proveedor[0] for proveedor in self.controller.model.obtener_proveedor()]
        
        for label_text, key in campos:
            tk.Label(izquierda, text=label_text, bg='white').pack()
            
            if key == "proveedor":
                # Usar Combobox para el campo de proveedor
                combo_proveedor = ttk.Combobox(
                    izquierda, 
                    width=37, 
                    values=proveedores,
                    postcommand=lambda: self.actualizar_lista_proveedores(combo_proveedor)
                )
                combo_proveedor.pack(pady=5)
                self.entries_inventario[key] = combo_proveedor
            elif key == "precio_unitario":
                # Validación para que solo acepte números decimales
                vcmd = (self.register(self.validar_precio), '%P')
                entry = tk.Entry(izquierda, width=40, validate="key", validatecommand=vcmd)
                entry.pack(pady=5)
                self.entries_inventario[key] = entry
            else:
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

    def actualizar_lista_proveedores(self, combobox):
        """Actualiza la lista de proveedores en el Combobox"""
        proveedores = [proveedor[0] for proveedor in self.controller.model.obtener_proveedor()]
        combobox['values'] = proveedores
        
    def guardar_producto(self):
        datos = {k: v.get().strip() for k, v in self.entries_inventario.items() 
                if hasattr(self, 'entries_inventario') and k in self.entries_inventario and v.winfo_exists()}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Validaciones
        if not datos["cantidad"].isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
            
        try:
            precio = float(datos["precio_unitario"])
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número decimal positivo")
            return

        exito = self.controller.model.agregar_producto(
            datos["id"], 
            datos["nombre"], 
            int(datos["cantidad"]),
            float(datos["precio_unitario"]),  # Nuevo campo
            datos["proveedor"], 
            datos["tipo"], 
            datos["talla"], 
            datos["persona"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_entradas_inventario()
            self.cargar_resumen_inventario()
        else:
            messagebox.showerror("Error", "Ya existe un producto con ese ID")
            
    
    def validar_precio(self, nuevo_valor):
        """Valida que el precio sea un número decimal positivo"""
        if nuevo_valor == "":
            return True
        try:
            float(nuevo_valor)
            return float(nuevo_valor) >= 0
        except ValueError:
            return False
    
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
                    f"{row[0]} | {row[1]} | Stock: {row[2]} | {row[3]} | Tipo: {row[4]} | Talla: {row[5]} | Para: {row[6]} | precio: {row[7]}"
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

#clientes

    def show_clientes_content(self):
        """Muestra el contenido para consultar clientes"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Consultar Clientes", 
                font=('Arial', 18), bg='white').pack(pady=20)

        # Inicializar el diccionario si no existe
        if not hasattr(self, 'entries_clientes'):
            self.entries_clientes = {}
        else:
            # Limpiar el diccionario de entradas anteriores
            self.entries_clientes.clear()

        izquierda = tk.Frame(self.content_frame, bg='#f7f7f7')
        izquierda.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        derecha = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        tk.Label(izquierda, text="Capturar Producto", font=('Arial', 18), bg='white').pack(pady=10)

        campos = [
            ("ID:", "id"),
            ("Nombre del cliente:", "nombre"),
            ("Direccion del cliente:", "direccion"),
            ("Telefono:", "telefono"),
            ("Correo electronico:", "correo")
        ]
        self.entries_clientes = {}
        for label_text, key in campos:
            tk.Label(izquierda, text=label_text, bg='white').pack()
            entry = tk.Entry(izquierda, width=40)
            entry.pack(pady=5)
            self.entries_clientes[key] = entry

        # Botones
        btn_guardar = tk.Button(izquierda, text="Guardar", command=self.guardar_cliente)
        btn_guardar.pack(pady=5)
        btn_limpiar = tk.Button(izquierda, text="Limpiar", command=self.limpiar_entradas_cliente)
        btn_limpiar.pack(pady=5)

        # Lista a la derecha
        tk.Label(derecha, text="Resumen de Cliente", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)
        self.resumen_cliente = tk.Listbox(derecha, width=100, height=50)
        self.resumen_cliente.pack(padx=10, pady=10)

        self.cargar_resumen_cliente()

    def guardar_cliente(self):
        datos = {k: v.get().strip() for k, v in self.entries_clientes.items() 
                if hasattr(self, 'entries_clientes') and k in self.entries_clientes and v.winfo_exists()}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        exito = self.controller.model.agregar_cliente(
            datos["id"], datos["nombre"], datos["direccion"], datos["telefono"], datos["correo"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            # Solo limpiar si las entradas existen
            if hasattr(self, 'entries_clientes'):
                self.limpiar_entradas_cliente()
            self.cargar_resumen_cliente()
        else:
            messagebox.showerror("Error", "Ya existe un producto con ese ID")

    def limpiar_entradas_cliente(self):
        # Verificar que el diccionario entries_clientes existe y tiene elementos
        if hasattr(self, 'entries_clientes') and self.entries_clientes:
            # Crear una copia de las claves para evitar problemas si se modifica durante la iteración
            for key in list(self.entries_clientes.keys()):
                entry = self.entries_clientes[key]
                try:
                    # Verificar si el widget aún existe
                    if entry.winfo_exists():
                        entry.delete(0, tk.END)
                except tk.TclError:
                    # Si el widget ya no existe, eliminarlo del diccionario
                    del self.entries_clientes[key]

    def cargar_resumen_cliente(self):
        # Verificar si el Listbox existe
        if hasattr(self, "resumen_cliente"):
            self.resumen_cliente.delete(0, tk.END)
            datos = self.controller.model.obtener_clientes()
            for row in datos:
                self.resumen_cliente.insert(
                    tk.END,
                    f"ID: {row[0]} | NOMBRE: {row[1]} | DIRECCION: {row[2]} | TELEFONO: {row[3]} | CORREO: {row[4]}"
                )

#proveedores

    def show_proveedores_content(self):
        """Muestra el contenido para consultar proveedores"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Consultar proveedores", 
                font=('Arial', 18), bg='white').pack(pady=20)

        # Inicializar el diccionario si no existe
        if not hasattr(self, 'entries_proveedores'):
            self.entries_proveedores = {}
        else:
            # Limpiar el diccionario de entradas anteriores
            self.entries_proveedores.clear()

        izquierda = tk.Frame(self.content_frame, bg='#f7f7f7')
        izquierda.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        derecha = tk.Frame(self.content_frame, bg='#f7f7f7', relief='sunken', borderwidth=1)
        derecha.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        tk.Label(izquierda, text="Gestión de Proveedores", font=('Arial', 18), bg='white').pack(pady=10)

        campos = [
            ("Nombre del proveedor:", "nombre"),
            ("Contacto del proveedor:", "contacto"),
            ("Direccion del proveedor:", "direccion")
        ]
        self.entries_proveedores = {}
        for label_text, key in campos:
            tk.Label(izquierda, text=label_text, bg='white').pack()
            entry = tk.Entry(izquierda, width=40)
            entry.pack(pady=5)
            self.entries_proveedores[key] = entry

        # Frame para botones
        botones_frame = tk.Frame(izquierda, bg='#f7f7f7')
        botones_frame.pack(pady=10)

        # Botón para guardar
        btn_guardar = tk.Button(botones_frame, text="Guardar", command=self.guardar_proveedor)
        btn_guardar.pack(side='left', padx=5)

        # Botón para limpiar
        btn_limpiar = tk.Button(botones_frame, text="Limpiar", command=self.limpiar_entradas_proveedor)
        btn_limpiar.pack(side='left', padx=5)

        # Botón para eliminar
        btn_eliminar = tk.Button(botones_frame, text="Eliminar", command=self.eliminar_proveedor)
        btn_eliminar.pack(side='left', padx=5)

        # Lista a la derecha
        tk.Label(derecha, text="Resumen de Proveedores", font=('Arial', 16), bg='#f7f7f7').pack(pady=10)
        self.resumen_proveedor = tk.Listbox(derecha, width=100, height=50)
        self.resumen_proveedor.pack(padx=10, pady=10)

        self.cargar_resumen_proveedor()

    def eliminar_proveedor(self):
        """Elimina un proveedor basado en el nombre ingresado"""
        nombre = self.entries_proveedores["nombre"].get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar el nombre del proveedor a eliminar")
            return
        
        # Confirmar antes de eliminar
        if not messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar al proveedor {nombre}?"):
            return
        
        # Llamar al modelo para eliminar
        exito = self.controller.model.eliminar_proveedor(nombre)
        
        if exito:
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            self.limpiar_entradas_proveedor()
            self.cargar_resumen_proveedor()
        else:
            messagebox.showerror("Error", "No se encontró el proveedor o no pudo ser eliminado")

    def guardar_proveedor(self):
        datos = {k: v.get().strip() for k, v in self.entries_proveedores.items() 
                if hasattr(self, 'entries_proveedores') and k in self.entries_proveedores and v.winfo_exists()}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        exito = self.controller.model.agregar_proveedor(
            datos["nombre"], datos["contacto"], datos["direccion"])

        if exito:
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            # Solo limpiar si las entradas existen
            if hasattr(self, 'entries_proveedores'):
                self.limpiar_entradas_proveedor()
            self.cargar_resumen_proveedor()
        else:
            messagebox.showerror("Error", "Ya existe un producto con ese Nombre")

    def limpiar_entradas_proveedor(self):
        # Verificar que el diccionario entries_proveedores existe y tiene elementos
        if hasattr(self, 'entries_proveedores') and self.entries_proveedores:
            # Crear una copia de las claves para evitar problemas si se modifica durante la iteración
            for key in list(self.entries_proveedores.keys()):
                entry = self.entries_proveedores[key]
                try:
                    # Verificar si el widget aún existe
                    if entry.winfo_exists():
                        entry.delete(0, tk.END)
                except tk.TclError:
                    # Si el widget ya no existe, eliminarlo del diccionario
                    del self.entries_proveedores[key]

    def cargar_resumen_proveedor(self):
        # Verificar si el Listbox existe
        if hasattr(self, "resumen_proveedor"):
            self.resumen_proveedor.delete(0, tk.END)
            datos = self.controller.model.obtener_proveedor()
            for row in datos:
                self.resumen_proveedor.insert(
                    tk.END,
                    f"NOMBRE: {row[0]} | CONTACTO: {row[1]} | DIRECCION: {row[2]}"
                )
