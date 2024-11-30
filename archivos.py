from tkinter import filedialog

class Archivos:

    def __init__(self):
        self.archivo_actual_guardado: bool = None

    def guardar_archivo(self, contenido):
        """Guarda el archivo
        
        Args:
            contenido (str): Texto que se va a guardar
        """
        file_path = filedialog.asksaveasfilename(filetypes=[("Archivo de texto (.txt)", "*.txt"), ("Todos los archivos", "*.*")])
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(contenido)
            file.close()
            self.archivo_actual_guardado = True

    def abrir_archivo(self) -> str:
        """Devuelve todo el contenido del archivo abierto"""
        file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto (.txt)", "*.txt")])
        if file_path:
            with open(file_path,"r", encoding="utf-8") as file:
                contenido = file.read()
                return contenido

    def cerrar_archivo(self):
        pass
    
    def is_archivo_actual_guardado(self):
        return self.archivo_actual_guardado

    def archivo_no_guardado(self, event):
        self.archivo_actual_guardado = False