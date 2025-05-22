# ajustesinterfaz.py (actualizado)
import tkinter as tk
from tkinter import messagebox

class SettingView(tk.Toplevel):
    def __init__(self, master, controller, username):
        super().__init__(master)
        self.controller = controller
        self.username = username
        self.title("Mis trapitos - Configuración")
        
        self.geometry("400x350")
        self.resizable(False, False)

        user_info = self.controller.model.get_user_info(self.username)
        current_address = user_info[3] if user_info and len(user_info) > 3 else ""
        current_number = user_info[4] if user_info and len(user_info) > 4 else ""

        # Título
        tk.Label(self, text="Configuración de Usuario", font=('Arial', 14)).pack(pady=10)

        # Mostrar datos existentes si los hay
        if current_address or current_number:
            datos_frame = tk.Frame(self)
            datos_frame.pack(pady=5)
            tk.Label(datos_frame, text=f"Dirección actual: {current_address}" if current_address else "").pack()
            tk.Label(datos_frame, text=f"Teléfono actual: {current_number}" if current_number else "").pack()

        # Dirección nueva
        tk.Label(self, text="Nueva Dirección:").pack()
        self.entry_address = tk.Entry(self, width=40)
        self.entry_address.pack(pady=5)
        self.entry_address.insert(0, current_address if current_address else "")

        # Teléfono nuevo
        tk.Label(self, text="Nuevo Número de teléfono:").pack()
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
            self.controller.show_main_view(self.username)
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información")