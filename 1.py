# Se importan distintas librerias para la función del programa 
import tkinter as tk
from tkinter import *
import datetime
import json
from PIL import ImageTk as itk
from PIL import Image
import requests
# Se crea la clase DataManager, que funciona para almacenar datos en la base de datos del programa
# atributos:
# data: tipo diccionario
class DataManager:
    # constructor de la clase
    def __init__(self):
        self.data = {}

    # funcion para abrir la base de datos del programa
    # def load_data(str) -> str 
    def load_data(self):
        try:
            with open("calendario_data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
    
    # funcion que guarda los datos en el diccionario
    # def save_data(int,str) -> int, str (guardados en el atributo (dicionario))
    def save_data(self, date, data):
        self.data[date.strftime("%Y-%m-%d")] = data
        self.save_data_to_file()

    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
    def save_data_to_file(self):
        with open("calendario_data.json", "w") as file:
            json.dump(self.data, file)

#Se crea la clase CalendarioApp, que almacena distintas funciones del programa
# atributos:
# text: str
class CalendarioApp:
    #Se define en este caso distintos objetos, como el titulo del calendario
    #Tambien con la clase DataManager para almacenar datos
    #Y para finalizar se crea el calendario del año 2024 con datetime
    def __init__(self, root, data_manager):
        self.root = root
        self.root.title("Calendario de anotaciones del año 2024")
        # Cargar datos almacenados (si existen)
        self.data_manager = data_manager
        self.data_manager.load_data()

        # Configurar el calendario
        self.current_date = datetime.date(2024, 1, 1)
        
        self.mescalculo=0

        self.create_calendar()

    #La sigueinte función tiene de finalidad de crear el calendario de forma grafica
    # con sus botones respectivos e interfaz
    # def create_calendar(str) -> str (interfaz completa)
    def create_calendar(self):
        text = Label(root, text="Kalendary",fg=color_03,font=("Arial",20),bg=color_01)
        text.pack()
        self.text = text
        # Crear un frame principal
        main_frame = tk.Frame(self.root,bg=color_01)
        main_frame.pack()

        btn_prevm = tk.Button(main_frame, text=">", command=self.prev_month,bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        btn_prevm.grid(row=0, column=2, padx=5, pady=5)
        btn_prevy = tk.Button(main_frame, text=">", command=self.prev_month,bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        btn_prevy.grid(row=0, column=1, padx=5, pady=5)

        me=tk.Label(main_frame, text=(int(datetime.date.today().strftime("%m"))+self.mescalculo),bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        me.grid(row=1, column=2)
        anio=tk.Label(main_frame, text=datetime.date.today().strftime("%Y"),bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        anio.grid(row=1, column=1)

        # Configurar botones para avanzar y retroceder entre las páginas
        btn_nextm = tk.Button(main_frame, text=">", command=self.next_month,bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        btn_nextm.grid(row=2, column=2, padx=5, pady=5)
        btn_nexty = tk.Button(main_frame, text=">", command=self.next_month,bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        btn_nexty.grid(row=2, column=1, padx=5, pady=5)
        
        # Botón para borrar datos del día seleccionado del mes actual
        btn_clear = tk.Button(main_frame, text="Cancelar", command=self.clear_month_data,bg=color_02,bd=1,fg=color_04,activebackground=color_03,activeforeground=color_02)
        btn_clear.grid(row=0, column=3, padx=5, pady=5)

        # Crear un frame para el calendario
        self.calendar_frame = tk.Frame(self.root,bg=color_01)
        self.calendar_frame.pack()

        # Mostrar el mes actual
        self.show_month()

    # Esta función sirve para los meses en especifico, con sus respectivas
    # semanas y dias, las cuales se revisa si tiene información almacenada
    # y tambien para limpar  y guardar en estas
    def show_month(self):

        # Obtener el primer día de la semana del mes
        current_date = self.current_date
        while current_date.weekday() != 0:
            current_date -= datetime.timedelta(days=1)

        # Crear el calendario para el mes
        for day in range(6):  # 6 semanas
            for week in range(7):  # 7 dias a la semana
                # Frame para cada día
                day_frame = tk.Frame(self.calendar_frame, width=90, height=90, bd=1, relief=tk.RIDGE,bg=color_02)
                day_frame.grid(row=day + 1, column=week, padx=5, pady=5)

                # Fecha
                day_label = Label(day_frame, text=current_date.strftime("%d"),bg=color_02,fg=color_04)
                day_label.pack()

                # Verificar si hay datos guardados para este día
                day_data = self.data_manager.data.get(current_date.strftime("%Y-%m-%d"), "")
                entry = Text(day_frame, wrap=tk.WORD, height=3, width=10,bg=color_01,fg=color_05)
                entry.insert(tk.END, day_data)
                entry.pack(expand=True, fill='both')
                # Asociar una función para guardar datos al cerrar la aplicación
                entry.bind("<FocusOut>", lambda event, date=current_date, entry=entry: self.save_data(date, entry.get("1.0", tk.END)))

                # Ir al siguiente día
                
                current_date += datetime.timedelta(days=1)

    #Funcion para dirigirse al anterior mes
    def prev_month(self):
        # Ir al mes anterior
        self.current_date = self.current_date.replace(month=self.current_date.month - 1, day=1)
        self.mescalculo= self.mescalculo-1
        self.show_month()
    
    #Función para dirigirse al siguiente mes
    def next_month(self):
        self.current_date = self.current_date.replace(month=self.current_date.month + 1, day=1)
        self.mescalculo= self.mescalculo+1
        self.show_month()
        self.clear_month_data()

    def save_data(self, date, data):
        self.data_manager.save_data(date, data)
        
    # Borrar los datos del mes actual
    def clear_month_data(self):
        month_start = self.current_date.replace(day=1)
        month_end = (self.current_date.replace(month=self.current_date.month + 1, day=1) - datetime.timedelta(days=1)).replace(day=1)

        for current_date in self.daterange(month_start, month_end):
            key = current_date.strftime("%Y-%m-%d")
            if key in self.data_manager.data:
                del self.data_manager.data[key]

        self.data_manager.save_data_to_file()
        self.show_month()

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n) 

if __name__ == "__main__":
    root = tk.Tk()
    root.config(background="#A1DED3") #color del fondo de la ventana
    color_01 = "#A1DED3" #color del fondo de los espacios
    color_02 = "#8FC8BE" #color del fondo de los botones
    color_03 = "#59857D" #color del Titulo
    color_04 = "#314B47" #color de la fecha
    color_05 = "#223230" #color del Texto
    color_06 = "#" #color sin usar
    # root.wm_iconbitmap('1.ico')
    ndia= str((datetime.date.today())).split('-')
    nomimg= "dia"+ndia[2]+".png"
    print(nomimg)
    root.iconphoto(False,itk.PhotoImage(file=nomimg))
    data_manager = DataManager()
    app = CalendarioApp(root, data_manager)
    root.mainloop()