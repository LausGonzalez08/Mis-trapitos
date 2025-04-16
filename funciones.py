from usuarios import UserModel
from iniciointerfaz import MainView
from logininterfaz import LoginView, RegisterView, messagebox
class AppController:
    def __init__(self):
        self.model = UserModel()
        self.main_view = MainView()
        self.main_view.withdraw()
        self.login_view = LoginView(self.main_view, self)
        self.register_view = None

    def login(self):
        usuario = self.login_view.entry_usuario.get()
        contraseña = self.login_view.entry_contraseña.get()
        print(usuario)
        print(contraseña)
        if self.model.validate_credentials(usuario, contraseña):
            self.login_view.destroy()
            self.main_view.deiconify()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def show_register(self):
        self.register_view = RegisterView(self.login_view, self)

    def register_user(self):
        nuevo_user = self.register_view.entry_nuevo_usuario.get()
        nueva_pass = self.register_view.entry_nueva_contraseña.get()
        confirm_pass = self.register_view.entry_confirmar_contraseña.get()
        
        if nueva_pass != confirm_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        es_admin = self.register_view.tipo_usuario.get() == "admin"
        success, message = self.model.add_user(nuevo_user, nueva_pass, admin=es_admin)
        if success:
            messagebox.showinfo("Éxito", message)
            self.register_view.destroy()
        else:
            messagebox.showerror("Error", message)

    def run(self):
        self.main_view.mainloop()

