"""Bloc de notas"""

from archivos import Archivos
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from operacion import Operacion


class App:

    def __init__(self):
        # ventana
        self.ventana = tk.Tk()
        self.ventana.title("Sin título")
        self.ventana.geometry("450x500")
        self.ventana_emergente = None

        # estados
        self.wrap_text = False
        self.archivo_guardado:bool = True
        self.operacion : Operacion = None

        #archivos
        self.gestor_archivos = Archivos()

        # scrolltext
        self.scroll_text = ScrolledText(
            self.ventana, padx=5, pady=5, wrap="none")
        self.scroll_text.pack(expand=True, fill="both")

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
        self.archivo_menu.add_command(label="Cerrar", command=self.cerrar_archivo)

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
        self.ventana_emergente = tk.Toplevel(self.ventana)
        self.ventana_emergente.title("Archivo sin guardar")
        self.ventana_emergente.geometry("300x150")

        label = tk.Label(self.ventana_emergente, text="Archivo no guardado")
        label.pack()
        boton_guardar = tk.Button(self.ventana_emergente,text="Guardar" ,command=self.guardar_archivo)
        boton_no_guardar = tk.Button(self.ventana_emergente,text="No guardar" ,command=self.realizar_operacion)
        boton_cancelar = tk.Button(self.ventana_emergente, text="Cancelar", command=self.cerrar_ventana_emergente)
        boton_guardar.pack()
        boton_no_guardar.pack()
        boton_cancelar.pack()

    def cerrar_ventana_emergente(self):
        """Cierra la ventana emergente"""
        if self.ventana_emergente:
            self.ventana_emergente.destroy()
  
    def borrar_texto(self):
        """Borra el texto"""
        self.scroll_text.delete(1.0,tk.END)

    def set_nombre_ventana(self, nombre):
        """Cambia el nombre de la ventana principal"""
        self.ventana.title(nombre)

    def realizar_operacion(self):
        print("Realizando operacion")
        print(self.operacion)
        self.cerrar_ventana_emergente()
        if self.operacion == Operacion.ABRIR:
            print("Operacion abrir")
            self.borrar_texto()
            self.gestor_archivos.abrir()
            self.scroll_text.insert(1.0, self.gestor_archivos.get_texto())
        elif self.operacion == Operacion.CERRAR:
            self.ventana.destroy()        

    def abrir_archivo(self):
        """Abre el archivo si esta guardado, sino abre la ventana emergente"""
        if self.gestor_archivos.is_guardado(self.scroll_text.get(1.0, tk.END)[:-1]): #Elimina el ultimo caracter porque siempre pone un salto de linea
            self.borrar_texto()
            self.gestor_archivos.abrir()
            self.scroll_text.insert(1.0, self.gestor_archivos.get_texto())
        else:
            self.operacion = Operacion.ABRIR
            self.show_archivo_no_guardado()

    def guardar_archivo(self):
        """Guarda el archivo"""
        self.gestor_archivos.set_texto(self.scroll_text.get(1.0, tk.END)[:-1])
        if self.gestor_archivos.guardar():
            self.realizar_operacion()

    def guardar_archivo_como(self):
        """Guarda el archivo como"""
        self.gestor_archivos.set_texto(self.scroll_text.get(1.0, tk.END)[:-1])
        if self.gestor_archivos.guardar_como():
            self.realizar_operacion()

    def cerrar_archivo(self):
        """Si el archivo esta guardado cierra la aplicación"""
        if self.gestor_archivos.is_guardado(self.scroll_text.get(1.0,tk.END)[:-1]):
            self.ventana.destroy()
        else:
            self.operacion = Operacion.CERRAR
            self.show_archivo_no_guardado()

    def iniciar(self):
        """Inicia el programa"""
        self.ventana.mainloop()
