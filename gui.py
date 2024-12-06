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
        self.ventana.option_add("*Font", "Arial 10")

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

        self.archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Control+N")
        self.archivo_menu.add_command(label="Abrir", command=self.abrir_archivo, accelerator="Control+A")
        self.archivo_menu.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Control+S")
        self.archivo_menu.add_command(label="Guardar Como", command=self.guardar_archivo_como, accelerator="Control+G")
        self.archivo_menu.add_separator()
        self.archivo_menu.add_command(label="Cerrar", command=self.cerrar_archivo, accelerator="Control+W")

        self.ventana.bind("<Control-n>", self.nuevo_archivo)
        self.ventana.bind("<Control-a>", self.abrir_archivo)
        self.ventana.bind("<Control-g>", self.guardar_archivo_como)
        self.ventana.bind("<Control-s>", self.guardar_archivo)
        self.ventana.bind("<Control-w>", self.cerrar_archivo)

        self.edicion_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Edición", menu=self.edicion_menu)

        self.edicion_menu.add_command(label="Copiar", command=self.copiar_texto, accelerator="Ctrl+C")
        self.edicion_menu.add_command(label="Cortar", command=self.cortar_texto, accelerator="Ctrl+X")
        self.edicion_menu.add_command(label="Pegar", command=self.pegar_texto, accelerator="Ctrl+V")

        self.ver_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Ver", menu=self.ver_menu)

        self.ver_menu.add_command(label="Ajustar texto", command=self.toggle_wrap)

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
        self.ver_menu.entryconfig(
            0, label="Ajustar texto" if not self.wrap_text else "Desajustar texto")
        self.toggle_scrollbar_horizontal()

    def toggle_scrollbar_horizontal(self):
        """Oculta o muestra la barra de desplazamiento horizontal"""
        if self.wrap_text:
            self.scrollbar_horizontal.forget()
        else:
            self.scrollbar_horizontal.pack(side="bottom", fill="x")

    def mostrar_ventana_emergente(self):
        """Crea ventana emergente de que el archivo no fue guardado"""
        self.ventana_emergente = tk.Toplevel(self.ventana)
        self.ventana_emergente.title("Archivo sin guardar")
        self.ventana_emergente.resizable(False, False)

        label = tk.Label(self.ventana_emergente, text=f"¿Quieres guardar los cambios de \"{self.gestor_archivos.get_nombre()}\"?")
        label.pack(pady=10,padx=15)

        frame = tk.Frame(self.ventana_emergente) 

        boton_guardar = tk.Button(frame,text="Guardar" ,command=self.guardar_archivo)
        boton_no_guardar = tk.Button(frame,text="No guardar" ,command=self.realizar_operacion)
        boton_cancelar = tk.Button(frame, text="Cancelar", command=self.cerrar_ventana_emergente)
        boton_guardar.pack(side=tk.LEFT,padx=5)
        boton_no_guardar.pack(side=tk.LEFT,padx=5)
        boton_cancelar.pack(side=tk.LEFT,padx=5)
        frame.pack(pady=10)

        #Calcular para que la ventana emergente salga justo en el medio de la ventana principal
        width_ventana = self.ventana.winfo_width()
        height_ventana = self.ventana.winfo_height()
        coordx_ventana = self.ventana.winfo_x()
        coordy_ventana = self.ventana.winfo_y()

        self.ventana_emergente.wait_visibility() #Espera que el toplevel sea visible para tomar sus medidas

        width_emergente = self.ventana_emergente.winfo_width()
        height_emergente = self.ventana_emergente.winfo_height()

        pos_x = coordx_ventana + (width_ventana // 2) - (width_emergente//2)
        pos_y = coordy_ventana + (height_ventana // 2) - (height_emergente//2)

        self.ventana_emergente.geometry(f"+{pos_x}+{pos_y}")

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
        """Realiza una operacion pedida anteriormente"""
        print(self.operacion)
        self.cerrar_ventana_emergente()
        if self.operacion == Operacion.ABRIR:
            if self.gestor_archivos.abrir():
                self.borrar_texto()
                self.scroll_text.insert(1.0, self.gestor_archivos.get_texto())
                self.actualizar_nombre()
        elif self.operacion == Operacion.CERRAR:
            self.ventana.destroy()        
        elif self.operacion == Operacion.NUEVO:
            self.gestor_archivos.nuevo()
            self.borrar_texto()
            self.actualizar_nombre()

    def abrir_archivo(self, event=None):
        """Abre el archivo si esta guardado, sino abre la ventana emergente"""
        if self.gestor_archivos.is_guardado(self.scroll_text.get(1.0, tk.END)[:-1]): #Elimina el ultimo caracter porque siempre pone un salto de linea
            self.borrar_texto()
            self.gestor_archivos.abrir()
            self.scroll_text.insert(1.0, self.gestor_archivos.get_texto())
            self.actualizar_nombre()
        else:
            self.operacion = Operacion.ABRIR
            self.mostrar_ventana_emergente()

    def guardar_archivo(self, event=None):
        """Guarda el archivo"""
        if self.gestor_archivos.guardar(self.scroll_text.get(1.0, tk.END)[:-1]):
            self.actualizar_nombre()
            self.realizar_operacion() #Si se guarda, realiza una operacion si fue pedida antes

    def guardar_archivo_como(self, event=None):
        """Guarda el archivo como"""
        if self.gestor_archivos.guardar_como(self.scroll_text.get(1.0, tk.END)[:-1]):
            self.actualizar_nombre()
            self.realizar_operacion() #Si se guarda, realiza una operacion si fue pedida antes

    def nuevo_archivo(self, event=None):
        """Si esta guardado abre un archivo nuevo"""
        if self.gestor_archivos.is_guardado(self.scroll_text.get(1.0, tk.END)[:-1]):
            self.gestor_archivos.nuevo()
            self.borrar_texto()
            self.actualizar_nombre()
        else:
            self.operacion = Operacion.NUEVO
            self.mostrar_ventana_emergente()

    def cerrar_archivo(self, event=None):
        """Si el archivo esta guardado cierra la aplicación"""
        if self.gestor_archivos.is_guardado(self.scroll_text.get(1.0,tk.END)[:-1]):
            self.ventana.destroy()
        else:
            self.operacion = Operacion.CERRAR
            self.mostrar_ventana_emergente()

    def actualizar_nombre(self):
        """Actualiza el nombre de la ventana con el nombre del archivo"""
        self.ventana.title(self.gestor_archivos.get_nombre())

    def iniciar(self):
        """Inicia el programa"""
        self.ventana.mainloop()
