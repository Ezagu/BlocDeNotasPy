"""Bloc de notas"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class App:

    def __init__(self):
        # ventana
        self.ventana = tk.Tk()
        self.ventana.title("Bloc de notas")
        self.ventana.geometry("450x500")

        # estados
        self.guardado = True
        self.wrap_text = False

        # barra de menu
        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        self.archivo_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Archivo", menu=self.archivo_menu)

        self.archivo_menu.add_command(
            label="Abrir", command=self.abrir_archivo)
        self.archivo_menu.add_command(label="Guardar")
        self.archivo_menu.add_command(label="Cerrar")

        self.edicion_menu = tk.Menu(self.ventana, tearoff=0)
        self.barra_menu.add_cascade(label="Edición", menu=self.edicion_menu)

        self.edicion_menu.add_command(
            label="Ajustar texto", command=self.toggle_wrap)

        # scrolltext
        self.scroll_text = ScrolledText(
            self.ventana, padx=5, pady=5, wrap="none")
        self.scroll_text.pack(expand=True, fill="both")
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

    def get_guardado(self):
        """Comprueba si el archivo abierto esta guardado o no"""
        return self.guardado

    def set_guardado(self, value: bool):
        """Cambia el valor de la variable guardado"""
        self.guardado = value

    def abrir_archivo(self):
        """Lee un archivo y lo coloca en el scrolled text"""

    def guardar_archivo(self):
        """Guarda el archivo"""

    def cerrar_archivo(self):
        """Cierra el archivo"""

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

    def iniciar(self):
        """Inicia el programa"""
        self.ventana.mainloop()


def main():
    """Main del archivo"""
    app = App()
    app.iniciar()


if __name__ == "__main__":
    main()
