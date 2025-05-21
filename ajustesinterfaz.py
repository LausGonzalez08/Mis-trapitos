# ajustesinterfaz.py (actualizado)
import tkinter as tk
from tkinter import messagebox

class SettingView(tk.Toplevel):
    def __init__(self, master, controller, username, first_login=False):
        super().__init__(master)
        self.controller = controller
        self.username = username
        self.first_login = first_login  # Nuevo parámetro
        self.title("Mis trapitos - Configuración")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Configuración para hacer la ventana modal si es primer inicio
        if first_login:
            self.grab_set()
            self.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilita el cierre
        
        # Obtener información del usuario
        user_info = self.controller.model.get_user_info(self.username)
        current_address = user_info[3] if user_info and len(user_info) > 3 else ""
        current_number = user_info[4] if user_info and len(user_info) > 4 else ""
        
        # Widgets
        tk.Label(self, text="Configuración de Usuario", font=('Arial', 14)).pack(pady=10)
        
        # Dirección
        tk.Label(self, text="Dirección:").pack()
        self.entry_address = tk.Entry(self, width=40)
        self.entry_address.pack(pady=5)
        self.entry_address.insert(0, current_address if current_address else "")
        
        # Teléfono
        tk.Label(self, text="Número de teléfono:").pack()
        self.entry_number = tk.Entry(self, width=40)
        self.entry_number.pack(pady=5)
        self.entry_number.insert(0, current_number if current_number else "")
        
        # Botón Guardar
        btn_save = tk.Button(self, text="Guardar", command=self.save_info)
        btn_save.pack(pady=20)
    
    def save_info(self):
        address = self.entry_address.get()
        number = self.entry_number.get()
        
        if not address or not number:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        success = self.controller.model.update_user_info(self.username, address, number)
        if success:
            messagebox.showinfo("Éxito", "Información actualizada correctamente")
            self.destroy()
            
            # Si era primer login, notificar al controlador para abrir MainView
            if self.first_login:
                self.controller.open_main_after_settings()