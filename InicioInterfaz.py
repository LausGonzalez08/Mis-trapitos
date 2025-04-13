import tkinter as tk
#VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Inicio")
ventana.geometry("800x600+100+50")
# BARRA DE MENU
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu) 

#MENU DE ARCHIVO
menu_opciones = tk.Menu(barra_menu, tearoff=0, bg="lightblue", fg="black")
menu_opciones.add_command(label="Ajustes")
menu_opciones.add_separator()
menu_opciones.add_command(label="Salir", command=ventana.quit)
barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
#MANTIENE LA VENTANA ABIERTA
ventana.mainloop()