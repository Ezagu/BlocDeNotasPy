"""Bloc de notas"""

from archivos import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class App:

    def __init__(self):
        # ventana
        self.ventana = tk.Tk()
        self.ventana.title("Sin título")
        self.ventana.geometry("450x500")

        # estados
        self.wrap_text = False
        self.archivo_guardado:bool = True

        #archivos
        self.path_actual = None
        self.nombre_del_archivo = None

        # scrolltext
        self.scroll_text = ScrolledText(
            self.ventana, padx=5, pady=5, wrap="none")
        self.scroll_text.pack(expand=True, fill="both")
        self.scroll_text.bind("<<Modified>>", self.guardado_false)

        # scrollbar
        self.scrollbar_horizontal = tk.Scrollbar(
            self.ventana, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")
        self.scrollbar_horizontal.config(command=self.scroll_text.xview)
        self.scroll_text.config(xscrollcommand=self.scrollbar_horizontal.set)

        # barra de menu
        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        self.archivo_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Archivo", menu=self.archivo_menu)

        self.archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        self.archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        self.archivo_menu.add_command(label="Guardar Como", command=self.guardar_archivo_como)
        self.archivo_menu.add_command(label="Cerrar", command=self.cerrar)

        self.edicion_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Edición", menu=self.edicion_menu)

        self.edicion_menu.add_command(
            label="Ajustar texto", command=self.toggle_wrap)

        # menu contextual
        self.menu_contextual = tk.Menu(self.ventana, tearoff=0)
        self.menu_contextual.add_command(
            label="Copiar", command=self.copiar_texto)
        self.menu_contextual.add_command(
            label="Cortar", command=self.cortar_texto)
        self.menu_contextual.add_command(
            label="Pegar", command=self.pegar_texto)

        self.scroll_text.bind("<Button-3>", self.mostrar_menu_contextual)

    def mostrar_menu_contextual(self, event):
        """Muestra el menu contextual"""
        self.menu_contextual.tk_popup(event.x_root, event.y_root)

    def copiar_texto(self):
        """Copia el texto seleccionado"""
        self.scroll_text.event_generate("<<Copy>>")

    def cortar_texto(self):
        """Corta el texto seleccionado"""
        self.scroll_text.event_generate("<<Cut>>")

    def pegar_texto(self):
        """Pega el texto"""
        self.scroll_text.event_generate("<<Paste>>")

    def toggle_wrap(self):
        """Alterna entre ajustar y desajustar el texto"""
        self.scroll_text.config(wrap="none" if self.wrap_text else "word")
        self.wrap_text = not self.wrap_text
        self.edicion_menu.entryconfig(
            0, label="Ajustar texto" if not self.wrap_text else "Desajustar texto")
        self.toggle_scrollbar_horizontal()

    def toggle_scrollbar_horizontal(self):
        """Oculta o muestra la barra de desplazamiento horizontal"""
        if self.wrap_text:
            self.scrollbar_horizontal.forget()
        else:
            self.scrollbar_horizontal.pack(side="bottom", fill="x")

    def show_archivo_no_guardado(self):
        """Crea ventana emergente de que el archivo no fue guardado"""
        ventana_emergente = tk.Toplevel(self.ventana)
        ventana_emergente.title("Archivo sin guardar")
        ventana_emergente.geometry("300x150")

        label = tk.Label(ventana_emergente, text="Archivo no guardado")
        label.pack()
        boton_guardar = tk.Button(ventana_emergente,text="Guardar" ,command=self.guardar_archivo_y_abrir)
        boton_no_guardar = tk.Button(ventana_emergente,text="No guardar" ,command=self.abrir_archivo)
        boton_cancelar = tk.Button(ventana_emergente, text="Cancelar", command=lambda : cerrar_ventana(ventana_emergente))
        boton_guardar.pack()
        boton_no_guardar.pack()
        boton_cancelar.pack()

        def cerrar_ventana(ventana):
            ventana.destroy()

    def abrir_archivo(self):
        """Abre un archivo"""
        if not self.archivo_guardado:
            self.show_archivo_no_guardado()
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto (.txt)", "*.txt")])
            if file_path:
                with open(file_path,"r", encoding="utf-8") as file:
                    contenido = file.read()
                    self.borrar_texto()
                    self.scroll_text.insert(1.0,contenido)
                    self.path_actual = file_path
                    self.scroll_text.edit_modified(False)
                    self.archivo_guardado = True  
                    self.set_nombre_ventana(self.get_nombre_archivo())        

    def guardar_archivo_y_abrir(self):
        """Guarda el archivo y si es guardado abre otro archivo"""
        if self.guardar_archivo():
            print("Se guardo el archivo")
            self.abrir_archivo()
        else:
            print("No se guardo el archivo")
    
    def no_guardar_y_abrir(self):
        """Borra el texto y abre un archivo"""
        self.borrar_texto()
        self.abrir_archivo()
        
    def guardar_archivo(self):
        """Guarda el archivo, si no se sabe el destino se guarda como, devuelve True si se guarda y False si no se guarda"""
        if not self.path_actual:
            #Si no se sabe el destino se guarda como
            return self.guardar_archivo_como()
        else:
            #Si se sabe el destino se guarda directamente
            contenido = self.scroll_text.get(1.0,tk.END)
            with open(self.path_actual, "w", encoding="utf-8") as file:
                file.write(contenido)
                file.close()
                self.archivo_guardado = True
                self.scroll_text.edit_modified(False)
                self.set_nombre_ventana(self.get_nombre_archivo())
                return True

    def guardar_archivo_como(self):
        """Guarda el archivo, devuelve True si se guardó y False si no se guardó"""
        contenido = self.scroll_text.get(1.0,tk.END)
        file_path = filedialog.asksaveasfilename(filetypes=[("Archivo de texto (.txt)", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            #Si se seleccionó un path correcto
            with open(file_path, "w", encoding="utf-8") as file:
                #Guarda el archivo
                file.write(contenido)
                file.close()
                self.path_actual = file_path
                self.archivo_guardado = True
                self.scroll_text.edit_modified(False)
                self.set_nombre_ventana(self.get_nombre_archivo())
                return True
        else:
            return False

    def guardado_false(self, event):
        """Indica que no se guardo el archivo"""
        print("Texto modificado")
        self.scroll_text.edit_modified(False)
        self.archivo_guardado = False
        self.set_nombre_ventana(self.get_nombre_archivo() + "*")

    def get_nombre_archivo(self):
        """Devuelve el nombre del archivo, default -> Sin título"""
        if self.path_actual:
            nombres = self.path_actual.split('/')
            return nombres[len(nombres) - 1]
        else:
            return "Sin título"

    def cerrar(self):
        """Si el archivo esta guardado cierra la app"""
        if not self.archivo_guardado:
            self.show_archivo_no_guardado()
        else:
            self.ventana.destroy()
            
    def borrar_texto(self):
        """Borra el texto"""
        self.scroll_text.delete(1.0,tk.END)

    def set_nombre_ventana(self, nombre):
        """Cambia el nombre de la ventana principal"""
        self.ventana.title(nombre)

    def iniciar(self):
        """Inicia el programa"""
        self.ventana.mainloop()
