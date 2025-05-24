# main.py
from funciones import AppController 
from scheduler import aplicar_descuentos_periodicamente

if __name__ == "__main__":
    app = AppController()
    aplicar_descuentos_periodicamente(app)  # Pasa el controlador como argumento
    app.login_view.mainloop()