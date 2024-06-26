import tkinter as tk
import json

class CambioDeColor:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Cambiar color de fondo")
        self.ventana.geometry("300x200")

        # Cargar colores desde el archivo JSON o usar colores predeterminados si el archivo no existe o está vacío
        try:
            with open('color.json', 'r') as file:
                self.colores = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.colores = {}

        # Establecer el color actual desde el archivo JSON o usar el primer color si no está especificado
        self.color_actual = self.colores.get("Actual", list(self.colores.values())[0] if self.colores else {"principal": "#151515", "subcolores": ["#59595B"], "texto": "white"})

        self.ventana.config(bg=self.color_actual["principal"])
        ## boton
        self.boton_abrir_colores = tk.Button(self.ventana, text="Cambiar Color de Fondo", command=self.abrir_ventana_colores)
        self.boton_abrir_colores.pack(pady=20)
        self.boton_abrir_colores.config(bg=self.color_actual["subcolores"][0], fg=self.color_actual["texto"])

    def guardar_color(self):
        self.colores["Actual"] = self.color_actual
        with open('color.json', 'w') as file:
            json.dump(self.colores, file, indent=4)

    def cambiar_color(self, color, text_color):
        self.color_actual["principal"] = color
        self.color_actual["texto"] = text_color
        self.ventana.config(bg=color)
        self.boton_abrir_colores.config(bg=color, fg=text_color)
        self.guardar_color()
        if hasattr(self, 'ventana_colores'):
            self.ventana_colores.destroy()

    def cambiar_atributos(self, bg_color, border_color, text_color):
        self.color_actual["principal"] = bg_color
        self.color_actual["subcolores"] = [border_color]
        self.color_actual["texto"] = text_color
        self.ventana.config(bg=bg_color)
        self.boton_abrir_colores.config(bg=border_color, fg=text_color)
        self.guardar_color()
        if hasattr(self, 'ventana_colores'):
            self.ventana_colores.destroy()

    def abrir_ventana_colores(self):
        self.ventana_colores = tk.Toplevel(self.ventana)
        self.ventana_colores.title("Seleccionar color")
        self.ventana_colores.geometry("150x300")
        self.ventana_colores.config(bg=self.color_actual["principal"])

        # Crear botones circulares para cada color predefinido, omitiendo el color actual y el color "Default"
        for nombre, info in self.colores.items():
            if nombre == "Actual" or nombre == "Default" or info["principal"] == self.color_actual["principal"]:
                continue  # Saltar la configuración "Actual", "Default" y el color actual
            color = info["principal"]
            subcolores = info["subcolores"]
            text_color = info["texto"]

            frame = tk.Frame(self.ventana_colores)
            frame.pack(pady=5)
            canvas = tk.Canvas(frame, width=120, height=50, highlightthickness=0, bg=self.color_actual["subcolores"][0])
            canvas.pack(side=tk.LEFT)

            circle = canvas.create_oval(10, 10, 40, 40, fill=color, outline="black", width=1)
            text = canvas.create_text(50, 25, text=nombre, anchor=tk.W)  # x, y

            canvas.tag_bind(text, '<Button-1>', lambda event, c=color, t=text_color: self.cambiar_color(c, t))
            canvas.tag_bind(circle, '<Button-1>', lambda event, c=color, t=text_color: self.cambiar_color(c, t))

            # Crear botones para subcolores
            for subcolor in subcolores:
                subcolor_button = tk.Button(frame, bg=subcolor, width=2, height=1,
                                            command=lambda bg=color, bc=subcolor, tc=text_color: self.cambiar_atributos(bg, bc, tc))
                subcolor_button.pack(side=tk.LEFT)

if __name__ == "__main__":
    root = tk.Tk()
    app = CambioDeColor(root)
    root.mainloop()
