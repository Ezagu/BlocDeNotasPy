from tkinter import filedialog
from operacion import Operacion

class Archivos:

    def __init__(self):
        self.path:str = None
        self.texto: str = ""

    def get_texto(self) -> str:
        """Devuelve el texto del archivo"""
        return self.texto
    
    def set_texto(self, texto):
        """Setea el texto"""
        self.texto = texto

    def get_nombre(self):
        """Devuelve el nombre del archivo abierto, sino no esta guardado todavia devuelve "Sin título"""
        if self.path:
            nombres = self.path.split("/")
            return nombres[-1]
        else:
            return "Sin título"

    def guardar(self):
        """Si se conoce el destino del archivo lo guarda directamente, sino lo guarda como, si se guarda devuelve True sino False"""
        if self.path:
            with open(self.path,"w", encoding="utf-8") as file_obj:
                file_obj.write(self.get_texto())
                file_obj.close()
                return True
        else:
            return self.guardar_como()
        return False

    def guardar_como(self):
        """Pregunta el lugar donde guardar el texto y lo guarda, si se guarda devuelve True, sino False"""
        file_path = filedialog.asksaveasfilename(filetypes=[("Archivo de texto (.txt)", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path,"w", encoding="utf-8") as file_obj:
                self.path = file_path
                file_obj.write(self.get_texto())
                file_obj.close()
                return True
        else:
            return False
        
    def abrir(self) -> str:
        """Abre un archivo"""
        file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto (.txt)", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                self.path = file_path
                self.texto = file_obj.read()

    def nuevo(self):
        """Si el archivo está guardado, crea un nuevo archivo"""
        self.texto = None
        self.path = None

    def is_guardado(self, texto):
        """Compara el texto con otro y si son iguales si está guardado"""
        print("Se guardó?:", self.texto == texto)
        print("Texto en archivo:", self.texto)
        print("Texto en scrolledText:", texto)
        return self.texto == texto