import tkinter as tk
from tkinter import messagebox, simpledialog

class UserDataView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Mis Trapitos - Datos de Usuarios")
        self.geometry("800x500")
        self.resizable(False, False)

        # División de la ventana
        frame_izquierda = tk.Frame(self, width=400, bg="white")
        frame_izquierda.pack(side="left", fill="both", expand=True)
        frame_derecha = tk.Frame(self, width=400, bg="#f7f7f7")
        frame_derecha.pack(side="right", fill="both", expand=True)

        # --------------------- IZQUIERDA: Lista de usuarios ---------------------
        tk.Label(frame_izquierda, text="Usuarios registrados", font=("Arial", 14), bg="white").pack(pady=10)
        self.user_list_frame = tk.Frame(frame_izquierda, bg="white")
        self.user_list_frame.pack(fill="both", expand=True, padx=10)

        # --------------------- DERECHA: Historial de logins ---------------------
        tk.Label(frame_derecha, text="Historial de inicio de sesión", font=("Arial", 14), bg="#f7f7f7").pack(pady=10)
        self.historial_text = tk.Text(frame_derecha, wrap="none", height=25, width=50)
        self.historial_text.pack(padx=10, pady=10)

        self.cargar_usuarios()
        self.cargar_historial()

    def cargar_usuarios(self):
        # Limpia contenido anterior
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()

        usuarios = self.controller.model.get_all_users()
        for user in usuarios:
            fila = tk.Frame(self.user_list_frame, bg="white")
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=user, bg="white", width=20, anchor="w").pack(side="left", padx=5)
            tk.Button(fila, text="Eliminar", command=lambda u=user: self.eliminar_usuario(u)).pack(side="right", padx=5)
            tk.Button(fila, text="Cambiar contraseña", command=lambda u=user: self.cambiar_contraseña(u)).pack(side="right")

    def cargar_historial(self):
        registros = self.controller.model.get_login_historial()
        self.historial_text.delete(1.0, tk.END)
        for username, fecha_hora in registros:
            self.historial_text.insert(tk.END, f"{fecha_hora} - {username}\n")

    def eliminar_usuario(self, username):
        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{username}'?"):
            self.controller.model.delete_user(username)
            self.cargar_usuarios()
            messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.")

    def cambiar_contraseña(self, username):
        nueva = simpledialog.askstring("Nueva contraseña", f"Ingrese nueva contraseña para '{username}':")
        if nueva:
            self.controller.model.update_password(username, nueva)
            messagebox.showinfo("Actualizado", "Contraseña actualizada correctamente.")
