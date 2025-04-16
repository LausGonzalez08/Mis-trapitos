import tkinter as tk

class MainView(tk.Toplevel):
    def __init__(self, username='', is_admin=False):
        super().__init__()
        self.username = username
        self.is_admin = is_admin

        titulo = f"Inicio - {self.username}"
        if self.is_admin:
            titulo += " (Admin)"
        self.title(titulo)

        self.geometry("800x600+100+50")
        self._make_menu()
        
    def _make_menu(self):
        self.barra_menu = tk.Menu(self)
        self.config(menu=self.barra_menu) 

        menu_opciones = tk.Menu(self.barra_menu, tearoff=0, bg="lightblue", fg="black")
        menu_opciones.add_command(label="Ajustes")
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.quit)
        self.barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
