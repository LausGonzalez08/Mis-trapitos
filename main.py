#INICIALIZADOR
#----Bibliotecas----
from funciones import AppController 
"""se importa AppControler (orquestador de modulos del programa) de funciones.py"""

if __name__ == "__main__":#se crea un main algo como en C++
    app = AppController() #Se asigna AppController a app
    app.login_view.mainloop() #de app se obtiene y ejecuta login_view
"""para ejecutar una funcion en python basta con poner el nombre de la funcion y (), ejemplo: app() con esto se ejecutaria app que es AppController,
pero en este caso ocupamos solo el login de AppController"""

