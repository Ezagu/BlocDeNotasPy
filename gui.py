"""Bloc de notas"""

from archivos import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class App:

    def __init__(self):
        # ventana
        self.ventana = tk.Tk()
        self.ventana.title("Bloc de notas")
        self.ventana.geometry("450x500")

        # estados
        self.wrap_text = False
        self.archivo_guardado:bool = True

        #archivos
        self.path_actual = None

        # barra de menu
        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        self.archivo_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Archivo", menu=self.archivo_menu)

        self.archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        self.archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        self.archivo_menu.add_command(label="Guardar Como", command=self.guardar_archivo_como)
        self.archivo_menu.add_command(label="Cerrar", command=self.cerrar_archivo)

        self.edicion_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Edición", menu=self.edicion_menu)

        self.edicion_menu.add_command(
            label="Ajustar texto", command=self.toggle_wrap)

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
        ventana_emergente = tk.Toplevel(self.ventana)
        ventana_emergente.title("Archivo sin guardar")
        ventana_emergente.geometry("300x150")

        label = tk.Label(ventana_emergente, text="Archivo no guardado")
        label.pack()
        boton_guardar = tk.Button(ventana_emergente,text="Guardar" ,command=self.guardar_archivo)
        boton_no_guardar = tk.Button(ventana_emergente,text="No guardar" ,command=self.abrir_archivo)
        boton_cancelar = tk.Button(ventana_emergente, text="Cancelar", command=lambda : cerrar_ventana(ventana_emergente))
        boton_guardar.pack()
        boton_no_guardar.pack()
        boton_cancelar.pack()

        def cerrar_ventana(ventana):
            ventana.destroy()

    def abrir_archivo(self):
        print(self.archivo_guardado)
        if not self.archivo_guardado:
            self.show_archivo_no_guardado()
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto (.txt)", "*.txt")])
            if file_path:
                with open(file_path,"r", encoding="utf-8") as file:
                    contenido = file.read()
                    self.scroll_text.delete(1.0,tk.END)
                    self.scroll_text.insert(1.0,contenido)
                    self.path_actual = file_path
                    self.scroll_text.edit_modified(False)
                    self.archivo_guardado = True          
                    

    def guardar_archivo(self):
        """Guarda el archivo"""
        if not self.path_actual:
            self.guardar_archivo_como()
        else:
            contenido = self.scroll_text.get(1.0,tk.END)
            with open(self.path_actual, "w", encoding="utf-8") as file:
                file.write(contenido)
                file.close()
                self.archivo_guardado = True
                self.scroll_text.edit_modified(False)

    def guardar_archivo_como(self):
        """Guarda el archivo"""
        contenido = self.scroll_text.get(1.0,tk.END)
        file_path = filedialog.asksaveasfilename(filetypes=[("Archivo de texto (.txt)", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(contenido)
                file.close()
                self.path_actual = file_path
                self.archivo_guardado = True
                self.scroll_text.edit_modified(False)

    def guardado_false(self, event):
        """Indica que no se guardo el archivo"""
        print("Texto modificado")
        self.archivo_guardado = False

    def cerrar_archivo(self):
        """Cierra el archivo"""
        if not self.archivo_guardado:
            self.show_archivo_no_guardado()
        else:
            self.scroll_text.delete(1.0,tk.END)

    def iniciar(self):
        """Inicia el programa"""
        self.ventana.mainloop()
