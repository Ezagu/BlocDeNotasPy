"""Bloc de notas"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

guardado = True


def abrir_archivo():
    """Lee un archivo y lo coloca en el scrolled text"""


def guardar_archivo():
    """Guarda el archivo"""
    guardado = True


def cerrar_archivo():
    """Cierra el archivo"""


def comprobar_guardado():
    """Comprueba si el archivo abierto esta guardado o no"""
    return guardado


def mostrar_menu_contextual(event):
    """Muestra el menu contextual"""
    menu_contextual.tk_popup(event.x_root, event.y_root)


def copiar_texto():
    """Copia el texto seleccionado"""
    scroll_text.event_generate("<<Copy>>")


def cortar_texto():
    """Corta el texto seleccionado"""
    scroll_text.event_generate("<<Cut>>")


def pegar_texto():
    """Pega el texto"""
    scroll_text.event_generate("<<Paste>>")


# ------Ventana----------
ventana = tk.Tk()
ventana.title("Bloc de notas")
ventana.geometry("450x500")

# ----Barra de menu-------
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

archivo_menu = tk.Menu(ventana, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=archivo_menu)

archivo_menu.add_command(label="Abrir", command=abrir_archivo)
archivo_menu.add_command(label="Guardar")
archivo_menu.add_command(label="Cerrar")

# -----Scroll text-------
scroll_text = ScrolledText(ventana, padx=5, pady=5, wrap="word")
scroll_text.pack(expand=True, fill="both")

# ----Contextual Menu------
menu_contextual = tk.Menu(ventana, tearoff=0)
menu_contextual.add_command(label="Copiar", command=copiar_texto)
menu_contextual.add_command(label="Cortar", command=cortar_texto)
menu_contextual.add_command(label="Pegar", command=pegar_texto)

scroll_text.bind("<Button-3>", mostrar_menu_contextual)

ventana.mainloop()
