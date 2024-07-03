import tkinter as tk
from tkinter import messagebox

def es_abecedario(caracter):
    return caracter.isalpha()

def validar_entrada(texto_insertado, accion):
    if accion == '1':  # Insertar texto
        if not es_abecedario(texto_insertado):
            messagebox.showerror("Entrada no válida", "Solo se permiten letras del abecedario.")
            return False
    return True

# Crear la ventana principal
root = tk.Tk()
root.title("Entrada del Abecedario")

# Configurar validación
vcmd = (root.register(validar_entrada), '%S', '%d')

# Crear una casilla de entrada con validación
entrada = tk.Entry(root, validate='key', validatecommand=vcmd)
entrada.pack(padx=20, pady=20)

# Iniciar el bucle de la aplicación
root.mainloop()