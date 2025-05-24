import os
import shutil
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox
import json  # Para manejar la configuración

class BackupManager:
    def __init__(self, db_name='Mis_Trapitos.db', historial_db='LoginHistorial.db'):
        self.db_name = db_name
        self.historial_db = historial_db
        self.config_file = 'backup_config.json'
        self.config = self._load_config()
        
    def _load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'backup_path': None,
                'last_backup_date': None,
                'backup_frequency': 7  # Días entre backups
            }
            
    def _save_config(self):
        """Guarda la configuración en el archivo"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)
            
    def set_backup_path(self, path):
        """Establece la ruta de backup (solo administrador)"""
        self.config['backup_path'] = path
        self._save_config()
            
    def get_backup_path(self):
        """Obtiene la ruta de backup guardada"""
        return self.config.get('backup_path')
        
    def set_backup_frequency(self, days):
        """Establece la frecuencia de backups en días"""
        self.config['backup_frequency'] = days
        self._save_config()
            
    def should_make_backup(self):
        """Determina si es momento de hacer backup según la última fecha"""
        if not self.config['backup_path']:
            return False
            
        last_date = self.config.get('last_backup_date')
        if not last_date:
            return True
            
        try:
            last_date = datetime.strptime(last_date, '%Y-%m-%d')
            next_backup = last_date + timedelta(days=self.config['backup_frequency'])
            return datetime.now() >= next_backup
        except ValueError:
            return True
            
    def create_backup(self):
        """Crea una copia de seguridad de todas las bases de datos"""
        if not self.config['backup_path']:
            return False, "No se ha configurado la ruta de backup"
            
        if not os.path.exists(self.config['backup_path']):
            os.makedirs(self.config['backup_path'])
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(self.config['backup_path'], f"backup_{timestamp}")
        os.makedirs(backup_folder)
        
        try:
            # Copiar las bases de datos
            shutil.copy2(self.db_name, backup_folder)
            shutil.copy2(self.historial_db, backup_folder)
            
            # Actualizar última fecha de backup
            self.config['last_backup_date'] = datetime.now().strftime('%Y-%m-%d')
            self._save_config()
            
            return True, f"Backup creado en: {backup_folder}"
        except Exception as e:
            return False, f"Error al crear backup: {str(e)}"
            
    def select_backup_path(self):
        """Permite seleccionar una ruta para los backups"""
        root = tk.Tk()
        root.withdraw()
        
        path = filedialog.askdirectory(title="Seleccionar carpeta para backups")
        if path:
            self.set_backup_path(path)
            return True, f"Ruta de backup configurada: {path}"
        return False, "No se seleccionó ninguna ruta"
        
    def show_backup_settings(self):
        """Muestra diálogo de configuración de backups con opción de backup manual"""
        root = tk.Tk()
        root.title("Configuración de Backups")
        
        # Frame principal
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack()
        
        # Sección de configuración
        config_frame = tk.LabelFrame(main_frame, text="Configuración", padx=5, pady=5)
        config_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        # Ruta de backup
        tk.Label(config_frame, text="Ruta actual:").grid(row=0, column=0, sticky='e')
        path_label = tk.Label(config_frame, text=self.get_backup_path() or "No configurada")
        path_label.grid(row=0, column=1, sticky='w')
        
        tk.Button(config_frame, text="Cambiar ruta", 
                command=lambda: self._update_path(path_label)).grid(row=0, column=2, padx=5)
        
        # Frecuencia
        tk.Label(config_frame, text="Frecuencia (días):").grid(row=1, column=0, sticky='e')
        freq_spin = tk.Spinbox(config_frame, from_=1, to=30, width=5)
        freq_spin.grid(row=1, column=1, sticky='w')
        freq_spin.delete(0, 'end')
        freq_spin.insert(0, str(self.config['backup_frequency']))
        
        # Sección de acciones
        action_frame = tk.Frame(main_frame)
        action_frame.grid(row=1, column=0, pady=10)
        
        # Botón para backup manual
        backup_btn = tk.Button(action_frame, text="Crear Backup Ahora", 
                            command=lambda: self._create_manual_backup(root),
                            bg="#4CAF50", fg="white")
        backup_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para guardar configuración
        save_btn = tk.Button(action_frame, text="Guardar Configuración", 
                            command=lambda: self._save_settings(freq_spin, root))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Estado del último backup
        status_frame = tk.LabelFrame(main_frame, text="Último Backup", padx=5, pady=5)
        status_frame.grid(row=2, column=0, sticky="ew")
        
        last_backup = self.config.get('last_backup_date') or "Nunca"
        last_backup_path = self.config.get('backup_path') or "No configurado"
        
        tk.Label(status_frame, text=f"Fecha: {last_backup}").pack(anchor='w')
        tk.Label(status_frame, text=f"Ubicación: {last_backup_path}").pack(anchor='w')
        
        root.mainloop()

    def _create_manual_backup(self, window):
        """Crea una copia de seguridad manualmente"""
        if not self.config['backup_path']:
            messagebox.showerror("Error", "Primero configure una ruta de backup")
            return
        
        try:
            # Deshabilitar botones durante el backup
            for widget in window.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state=tk.DISABLED)
            
            window.update()  # Actualizar la interfaz
            
            success, message = self.create_backup()
            if success:
                messagebox.showinfo("Éxito", f"Backup creado exitosamente:\n{message}")
                # Actualizar la información del último backup
                self._update_backup_info(window)
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        finally:
            # Rehabilitar botones
            for widget in window.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state=tk.NORMAL)

    def _update_backup_info(self, window):
        """Actualiza la información del último backup en la ventana"""
        for widget in window.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Último Backup":
                for label in widget.winfo_children():
                    if "Fecha:" in label.cget("text"):
                        label.config(text=f"Fecha: {self.config.get('last_backup_date')}")
                    elif "Ubicación:" in label.cget("text"):
                        label.config(text=f"Ubicación: {self.config.get('backup_path')}")
                break
        
    def _update_path(self, label):
        """Actualiza la etiqueta de la ruta"""
        success, message = self.select_backup_path()
        if success:
            label.config(text=self.get_backup_path())
            messagebox.showinfo("Éxito", message)
            
    def _save_settings(self, freq_spin, window):
        """Guarda la configuración y cierra la ventana"""
        try:
            days = int(freq_spin.get())
            self.set_backup_frequency(days)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de días")