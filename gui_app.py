import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys
import threading
import shutil
import queue
import logging
from datetime import datetime
from ttkbootstrap.scrolled import ScrolledText

# Importar el procesador del otro archivo
from automated_reports import ReportProcessor

class QueueHandler(logging.Handler):
    """
    Handler de logging para enviar registros a una cola de manera thread-safe.
    """
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class ReportProcessorGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly", title="Generador de Reportes de Seguridad", size=(900, 700), minsize=(700, 500))
        
        # Rutas Fijas
        self.input_dir = self.get_path("xls_folder")
        self.output_dir = self.get_path("rapport2")
        self.temp_dir = self.get_path("reports")

        # Asegurarse de que los directorios existan
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        self.processor = ReportProcessor(input_dir=self.input_dir, output_dir=self.output_dir, temp_dir=self.temp_dir)
        
        # Estado de la aplicación
        self.files_to_process = {} # Diccionario para rastrear el estado de cada archivo
        
        self.setup_ui()
        self.setup_logging()
        self.refresh_file_list()
        
        self.show_welcome_art()

    def get_path(self, default_folder):
        return os.path.abspath(default_folder)

    def setup_ui(self):
        """Configura la interfaz de usuario principal."""
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=BOTH, expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Frame de acciones
        actions_frame = self.create_actions_frame(main_frame)
        actions_frame.grid(row=0, column=0, sticky=EW, pady=(0, 10))

        # Frame de la lista de archivos
        files_frame = self.create_files_frame(main_frame)
        files_frame.grid(row=1, column=0, sticky=NSEW, pady=5)

        # Frame de logs
        log_frame = self.create_log_frame(main_frame)
        log_frame.grid(row=2, column=0, sticky=EW, pady=(10, 0))
        log_frame.rowconfigure(0, weight=0) # No expandir
        log_frame.columnconfigure(0, weight=1)

    def create_actions_frame(self, parent):
        frame = ttk.Frame(parent)
        
        ttk.Button(frame, text="1. Añadir Archivos", command=self.add_files, bootstyle="success", width=20).pack(side=LEFT, padx=5)
        self.extract_button = ttk.Button(frame, text="2. Extraer Información", command=self.start_extraction, bootstyle="primary", width=20)
        self.extract_button.pack(side=LEFT, padx=5)
        self.generate_button = ttk.Button(frame, text="3. Generar Informes Finales", command=self.start_final_report_generation, bootstyle="info", width=25)
        self.generate_button.pack(side=LEFT, padx=5)
        
        # Frame para botones de gestión
        management_frame = ttk.Frame(frame)
        management_frame.pack(side=RIGHT, padx=5)

        self.remove_button = ttk.Button(management_frame, text="Quitar Archivo", command=self.remove_selected_file, bootstyle="warning-outline", state='disabled')
        self.remove_button.pack(side=LEFT, padx=(0, 5))
        
        ttk.Button(management_frame, text="📁 Abrir Carpeta de Salida", command=self.open_output_dir, bootstyle="danger-outline").pack(side=LEFT)
        
        return frame
        
    def create_files_frame(self, parent):
        frame = ttk.Labelframe(parent, text="Archivos a Procesar", padding=10)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(frame, columns=("filename", "status"), show="headings", bootstyle="primary")
        self.tree.heading("filename", text="Nombre del Archivo")
        self.tree.heading("status", text="Estado")
        self.tree.column("status", width=200, anchor=CENTER)

        self.tree.grid(row=0, column=0, sticky=NSEW)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=NS)
        
        # Eventos de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.tree.bind("<Double-1>", self.on_file_double_click)
        
        return frame

    def show_welcome_art(self):
        """Affiche l'art ASCII dans le footer."""
        art = r"""

 _   _      _ _       
| | | |    | | |      
| |_| | ___| | | ___  
|  _  |/ _ \ | |/ _ \ 
| | | |  __/ | | (_) |
\_| |_/\___|_|_|\___/ 

"""
        self.log_text.delete(1.0, END)
        self.log_text.tag_configure("center", justify='center')
        self.log_text.insert(END, art, "center")

    def create_log_frame(self, parent):
        # Footer simple sans titre
        frame = ttk.Frame(parent, padding=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Zone pour l'art ASCII seulement
        self.log_text = ScrolledText(frame, height=8, autohide=True, bootstyle="round", font=("Courier New", 10))
        self.log_text.grid(row=0, column=0, sticky=EW)
        
        return frame

    def setup_logging(self):
        # Pas besoin de logging complexe pour un simple footer
        pass

    def poll_log_queue(self):
        # Pas besoin de polling pour un footer statique
        pass

    def add_files(self):
        filepaths = filedialog.askopenfilenames(
            title="Seleccionar archivo(s) para añadir",
            filetypes=[("Archivos de Reporte", "*.xls *.xlsx *.csv"), ("Todos los archivos", "*.*")]
        )
        if filepaths:
            try:
                for filepath in filepaths:
                    shutil.copy(filepath, self.input_dir)
                logging.info(f"{len(filepaths)} archivo(s) añadido(s) a la carpeta de entrada.")
                self.refresh_file_list()
            except Exception as e:
                logging.error(f"Error al añadir archivo: {e}")
                messagebox.showerror("Error", f"No se pudo añadir el archivo.\n{e}")

    def refresh_file_list(self):
        # Guardar la selección actual
        selected_item = self.tree.selection()
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.files_to_process = {f: {'status': 'Listo'} for f in os.listdir(self.input_dir) if f.lower().endswith(('.xls', '.xlsx', '.csv'))}

        for filename, data in self.files_to_process.items():
            self.tree.insert("", END, values=(filename, data['status']))
            
        # Restaurar la selección si aún existe
        if selected_item:
            self.tree.selection_set(selected_item)
        
        self.on_file_select() # Actualizar estado del botón

    def on_file_select(self, event=None):
        """Actualiza el estado de los botones basados en la selección."""
        if self.tree.selection():
            self.remove_button.config(state='normal')
        else:
            self.remove_button.config(state='disabled')

    def on_file_double_click(self, event=None):
        """Muestra el contenido del reporte en una nueva ventana."""
        selection = self.tree.selection()
        if not selection:
            return
            
        selected_item = selection[0]
        filename, status = self.tree.item(selected_item, "values")
        
        report_path = self.get_report_path_for_file(filename, status)
        
        if report_path and os.path.exists(report_path):
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.show_preview_window(os.path.basename(report_path), content)
            except Exception as e:
                messagebox.showerror("Error de Lectura", f"No se pudo leer el archivo de reporte:\n{e}")
        else:
            messagebox.showinfo("Sin Previsualización", "No hay un reporte que mostrar para este archivo.\n\nGenere la información o el informe final primero.")

    def get_report_path_for_file(self, filename, status):
        """Devuelve la ruta a un archivo de reporte si existe."""
        if status == "Información Extraída":
            base, _ = os.path.splitext(filename)
            return os.path.join(self.temp_dir, f"{base}_reporte.txt")
        elif status == "Reporte Final Generado":
            base, _ = os.path.splitext(filename)
            intermediate_base_name = f"{base}_reporte"
            final_name = f"{intermediate_base_name}_final.txt"
            return os.path.join(self.output_dir, final_name)
        return None

    def show_preview_window(self, title, content):
        """Crea y muestra una ventana Toplevel para la previsualización."""
        preview_window = ttk.Toplevel(self, title=f"Previsualización - {title}", size=(600, 500))
        preview_window.transient(self) # Mantener por encima de la principal
        
        text_area = ScrolledText(preview_window, padding=10, autohide=True)
        text_area.pack(fill=BOTH, expand=True)
        text_area.insert(END, content)
        text_area.config(state='disabled')

    def open_output_dir(self):
        try:
            # Comprobar si la carpeta de salida está vacía
            if not os.listdir(self.output_dir):
                 messagebox.showwarning("Carpeta Vacía", f"La carpeta de salida está vacía.\n\n{self.output_dir}")
                 return
            os.startfile(self.output_dir)
        except Exception:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {self.output_dir}")
            
    def remove_selected_file(self):
        """Elimina el archivo seleccionado de la lista y del disco."""
        selection = self.tree.selection()
        if not selection:
            return

        selected_item = selection[0]
        filename, _ = self.tree.item(selected_item, "values")
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar permanentemente el archivo '{filename}'?"):
            try:
                file_path = os.path.join(self.input_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Archivo '{filename}' eliminado con éxito.")
                else:
                    logging.warning(f"El archivo '{filename}' no se encontró en el disco para eliminarlo, solo se quitará de la lista.")
                
                # Quitar de la lista en la GUI
                self.tree.delete(selected_item)
                if filename in self.files_to_process:
                    del self.files_to_process[filename]

            except Exception as e:
                logging.error(f"Error al eliminar el archivo '{filename}': {e}")
                messagebox.showerror("Error de Eliminación", f"No se pudo eliminar el archivo:\n{e}")

    def disable_buttons(self, state=True):
        self.extract_button.config(state='disabled' if state else 'normal')
        self.generate_button.config(state='disabled' if state else 'normal')

    def start_extraction(self):
        self.disable_buttons()
        thread = threading.Thread(target=self.run_extraction_thread)
        thread.daemon = True
        thread.start()

    def run_extraction_thread(self):
        try:
            processed, failed = self.processor.extract_intermediate_reports()

            for p_file in processed:
                self.files_to_process[p_file]['status'] = 'Información Extraída'
            for f_file in failed:
                self.files_to_process[f_file]['status'] = 'Error de Extracción'
            
            self.after(0, self.update_treeview_statuses)
            self.after(0, lambda: messagebox.showinfo("Extracción Completada", f"{len(processed)} archivo(s) procesado(s) para extracción.\nPuedes ahora generar los informes finales."))
            
        except Exception as e:
            logging.error(f"Fallo crítico durante la extracción: {e}")
        finally:
            self.after(0, self.disable_buttons, False)
    
    def start_final_report_generation(self):
        self.disable_buttons()
        thread = threading.Thread(target=self.run_generation_thread)
        thread.daemon = True
        thread.start()
        
    def run_generation_thread(self):
        try:
            processed, failed = self.processor.generate_final_reports()
            
            # Actualizar estado para archivos que tenían reporte intermedio
            for item in self.tree.get_children():
                filename = self.tree.item(item)['values'][0]
                if self.files_to_process.get(filename, {}).get('status') == 'Información Extraída':
                     self.files_to_process[filename]['status'] = 'Reporte Final Generado'

            self.after(0, self.update_treeview_statuses)
            
            if processed:
                self.after(0, lambda: messagebox.showinfo("Éxito", f"Se generaron {len(processed)} reportes finales.\n\nPuedes encontrarlos en la carpeta:\n{self.output_dir}"))
            else:
                self.after(0, lambda: messagebox.showwarning("Aviso", "No se encontraron reportes intermedios para procesar o todos fallaron."))

        except Exception as e:
            logging.error(f"Fallo crítico durante la generación de reportes: {e}")
        finally:
            self.after(0, self.disable_buttons, False)

    def update_treeview_statuses(self):
        for iid in self.tree.get_children():
            filename = self.tree.item(iid)['values'][0]
            if filename in self.files_to_process:
                new_status = self.files_to_process[filename]['status']
                self.tree.item(iid, values=(filename, new_status))

def main():
    app = ReportProcessorGUI()
    app.mainloop()

if __name__ == "__main__":
    main()