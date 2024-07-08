import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import time
import datetime as dt
from datetime import timedelta
from PIL import Image, ImageTk
import requests
import json
class DataManager:
    # constructor de la clase
    def __init__(self):
        self.data = {}
    ...
class getWhether:
    def __init__(self):
        self.data = {}
    def loadData(self):
        with open("whether.json", "r") as file:
            self.data = json.load(file)
        if self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m-%d")}T10:00:00Z" and self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m")}-{int(dt.datetime.today().strftime("%d"))-1}T10:00:00Z" :
            self.apiCall()
    def save_data_to_file(self,data):
        with open("whether.json", "w") as file:
            json.dump(data, file)
        self.loadData()
    def apiCall(self):
        print("////////////////API call///////////////////")
        api_key="a51S5D6NSdSEfLhIK5t97rShUgKgLb0T"
        # api_key="xcDOEQGB3KiPXjJmIfYGQXhW4bWpQBja"
        url = f"https://api.tomorrow.io/v4/weather/forecast?location=Osorno%2C%20Los%20Lagos%2C%20Chile&units=metric&apikey={api_key}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        js=json.loads(response.text)
        self.save_data_to_file(js)

class CalendarioApp(tk.Tk):
    def __init__(self,fecha):
        # configucacion
        super().__init__()
        self.title('Kalendario')
        self.geometry('700x700')
        self.minsize(700,700)
        self.maxsize(700,700)
        self.config(background="#22252A")
        # cargamos las imagenes
        self.arrows={1:ImageTk.PhotoImage(Image.open("img/up-arrow.png").resize((20,20), Image.LANCZOS)),
                     2:ImageTk.PhotoImage(Image.open("img/down-arrow.png").resize((20,20), Image.LANCZOS)),
                     3:ImageTk.PhotoImage(Image.open("img/up-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     4:ImageTk.PhotoImage(Image.open("img/down-arrow-lock.png").resize((20,20), Image.LANCZOS))}
        self.imagenes={1000:ImageTk.PhotoImage(Image.open("img/1000.png").resize((80,80), Image.LANCZOS)),
                       1001:ImageTk.PhotoImage(Image.open("img/1001.png").resize((80,80), Image.LANCZOS)),
                       1100:ImageTk.PhotoImage(Image.open("img/1100.png").resize((80,80), Image.LANCZOS)),
                       1101:ImageTk.PhotoImage(Image.open("img/1101.png").resize((80,80), Image.LANCZOS)),
                       1102:ImageTk.PhotoImage(Image.open("img/1102.png").resize((80,80), Image.LANCZOS)),
                       2000:ImageTk.PhotoImage(Image.open("img/2000.png").resize((80,80), Image.LANCZOS)),
                       2100:ImageTk.PhotoImage(Image.open("img/2100.png").resize((80,80), Image.LANCZOS)),
                       4000:ImageTk.PhotoImage(Image.open("img/4000.png").resize((80,80), Image.LANCZOS)),
                       4001:ImageTk.PhotoImage(Image.open("img/4001.png").resize((80,80), Image.LANCZOS)),
                       4200:ImageTk.PhotoImage(Image.open("img/4200.png").resize((80,80), Image.LANCZOS)),
                       4201:ImageTk.PhotoImage(Image.open("img/4201.png").resize((80,80), Image.LANCZOS)),
                       5000:ImageTk.PhotoImage(Image.open("img/5000.png").resize((80,80), Image.LANCZOS)),
                       5001:ImageTk.PhotoImage(Image.open("img/5001.png").resize((80,80), Image.LANCZOS)),
                       5100:ImageTk.PhotoImage(Image.open("img/5100.png").resize((80,80), Image.LANCZOS)),
                       5101:ImageTk.PhotoImage(Image.open("img/5101.png").resize((80,80), Image.LANCZOS)),
                       6000:ImageTk.PhotoImage(Image.open("img/6000.png").resize((80,80), Image.LANCZOS)),
                       6001:ImageTk.PhotoImage(Image.open("img/6001.png").resize((80,80), Image.LANCZOS)),
                       6200:ImageTk.PhotoImage(Image.open("img/6200.png").resize((80,80), Image.LANCZOS)),
                       6201:ImageTk.PhotoImage(Image.open("img/6201.png").resize((80,80), Image.LANCZOS)),
                       7000:ImageTk.PhotoImage(Image.open("img/7000.png").resize((80,80), Image.LANCZOS)),
                       7101:ImageTk.PhotoImage(Image.open("img/7101.png").resize((80,80), Image.LANCZOS)),
                       7102:ImageTk.PhotoImage(Image.open("img/7102.png").resize((80,80), Image.LANCZOS)),
                       8000:ImageTk.PhotoImage(Image.open("img/8000.png").resize((80,80), Image.LANCZOS))}
        # parametros del clima
        self.tipo_clima={1000:"Despejado",1001:"Nublado",1100:"Mayormente Despejado",1101:"Parcialmente Nublado",
                         1102:"Mayormente Nublado",2000:"Neblina",2100:"Ligera Neblina",4000:"Llovizna",4200:"Lluvia Ligera",
                         4001:"Lluvia",4201:"Lluvia Intensa",5001:"Neviscas",5100:"Nieve Ligera",5000:"Nieve",
                         5101:"Nieve Ligera",6000:"Llovizna Helada",6001:"Lluvia Helada",6200:"Lluvia Helada Ligera",
                         6201:"lluvia helada Intensa",7102:"Ligera Hielo Granulado",7000:"Hielo Granulado",7101:"Hielo Granulado Intenso",
                         8000:"Tormenta"}
        # controles del calendario
        self.control_calendario= control_calendario(self,fecha)
        # panel del clima
        self.control_clima=seccion_clima(self,fecha)
        self.mainloop()

class control_calendario(ttk.Frame):
    def __init__(self, parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=0,y=0,relwidth=0.4,relheight=0.2)
        self.calendario_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.arrows=parent.arrows
        self.anio_cambio= StringVar()
        self.mes_cambio= StringVar()
        self.style()
        self.fecha()
        self.change_fecha()
        self.controles_atras()
        self.controles_adelante()
        self.grid()
    def change_fecha(self):
        self.mes_cambio.set(f"{self.calendario_time.strftime("%m")}")
        self.anio_cambio.set(f"{self.calendario_time.strftime("%Y")}")
        self.mes_anio()
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background="#22252A",foreground="#FFFFFF")
    def fecha(self):
        months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.fecha1= ttk.Label(self,font='1', text=f"{self.calendario_time.strftime("%d")} de {months[int(self.calendario_time.strftime("%m"))-1]} de {self.calendario_time.strftime("%Y")}",background="#22252A",foreground="#FFFFFF")
    def controles_atras(self):
        self.btn_prevmes = ttk.Button(self,command=self.prev_month,image=self.arrows[2])
        self.btn_prevanio = ttk.Button(self,command=self.prev_year,image=self.arrows[2])
    def mes_anio(self):
        self.anio= ttk.Label(self, textvariable=self.anio_cambio,background="#22252A",foreground="#FFFFFF")
        self.mes= ttk.Label(self, textvariable=self.mes_cambio,background="#22252A",foreground="#FFFFFF")
    def controles_adelante(self):
        self.btn_nextmes = ttk.Button(self,command=self.next_month,image=self.arrows[1])
        self.btn_nextanio = ttk.Button(self,command=self.next_year,image=self.arrows[1])
    def grid(self):
        self.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.columnconfigure((0,1,2,3),weight=1,uniform='a')

        self.fecha1.place(x=0,y=0,relwidth=1,relx=0.19,relheight=0.3)
        self.styles.place(x=0,y=0,relwidth=1,relx=0,relheight=1)
        self.anio.grid(row=3,column=1, sticky='')
        self.mes.grid(row=3,column=2, sticky='')
        self.btn_nextmes.grid(row=2, column=2, sticky='',columnspan=1)
        self.btn_nextanio.grid(row=2, column=1, sticky='',columnspan=1)
        self.btn_prevmes.grid(row=4, column=2, sticky='',columnspan=1)
        self.btn_prevanio.grid(row=4, column=1, sticky='',columnspan=1)
    def prev_month(self):
        try:
            self.calendario_time = self.calendario_time.replace(month=self.calendario_time.month - 1, day=1)
        except:
            self.calendario_time = self.calendario_time.replace(year=self.calendario_time.year - 1,month=12)
        self.change_fecha()
    def prev_year(self):
        self.calendario_time = self.calendario_time.replace(year=self.calendario_time.year - 1)
        self.change_fecha()
    def next_month(self):
        try:
            self.calendario_time = self.calendario_time.replace(month=self.calendario_time.month + 1, day=1)
        except:
            self.calendario_time = self.calendario_time.replace(year=self.calendario_time.year + 1, month=1)

        self.change_fecha()
    def next_year(self):
        self.calendario_time = self.calendario_time.replace(year=self.calendario_time.year + 1)
        self.change_fecha()
class seccion_clima(ttk.Frame):
    def __init__(self,parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=300,y=0,relwidth=0.6,relheight=0.2)
        self.data_clima=getWhether()
        self.data_clima.loadData()
        self.clima_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.arrows=parent.arrows
        self.imagenes=parent.imagenes
        self.tipo_clima=parent.tipo_clima
        self.index=0
        # inicio de los estilos
        self.style()
        self.line1()
        self.line2()
        self.line3()
        # primera seccion
        self.descripcion()
        self.controles()
        # segunda seccion
        ...
        # tercera seccion
        self.horaYminutomasGrados()
        self.texto()
        # grid
        self.grid()
    # estilos
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background="#22252A",foreground="#FFFFFF")
    def line1(self):
        self.lines1=ttk.Label(self,font='1', text=f"",background="#E5A769")
    def line2(self):
        self.lines2=ttk.Label(self,font='1', text=f"",background="#74ADEA")
    def line3(self):   
        self.lines3=ttk.Label(self,font='1', text=f"",background="#5662F6")
    # primera seccion
    # texto de "lluviendo" o "sol"
    def descripcion(self):
        self.descripcion1= ttk.Label(self,font='1', text=self.tipo_clima[self.data_clima.data.get("timelines").get("daily")[0].get("values").get("weatherCodeMin")],background="#22252A",foreground="#FFFFFF")
        self.descripcionDetalle1= ttk.Label(self,font=('Arial',10), text=f"Datos",background="#22252A",foreground="#FFFFFF")
        self.descripcionDetalle2= ttk.Label(self,font=('Arial',10), text=f"Temp. Max: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMax")}°ᶜ",background="#22252A",foreground="#FFFFFF")
        self.descripcionDetalle3= ttk.Label(self,font=('Arial',10), text=f"Temp. Min: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMin")}°ᶜ",background="#22252A",foreground="#FFFFFF")
        self.descripcionDetalle4= ttk.Label(self,font=('Arial',10), text=f"Viento: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("windSpeedAvg")}km/h",background="#22252A",foreground="#FFFFFF")
        self.descripcionDetalle5= ttk.Label(self,font=('Arial',10), text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("humidityAvg")}%",background="#22252A",foreground="#FFFFFF")
        self.fecha1= ttk.Label(self,font=("Arial",10), text=dt.datetime.today().strftime("%d/%m/%Y"),background="#22252A",foreground="#FFFFFF")
        self.imagen1=ttk.Label(self,font='1',background="#22252A",image=self.imagenes[self.data_clima.data.get("timelines").get("daily")[0].get("values").get("weatherCodeMin")])
        self.dia= ttk.Label(self, text=self.clima_time.strftime("%d"),background="#22252A",foreground="#FFFFFF")
    def controles(self):
        self.btn_nextdia = ttk.Button(self,command=self.next_dia,image=self.arrows[1])
        self.btn_prevdia = ttk.Button(self,command=self.prev_dia,image=self.arrows[4])
    def next_dia(self):
        self.configure(-1,1)
    def prev_dia(self):
        self.configure(0,-1)
    def configure(self,i,op):
        if f'{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[2][0:2]}-{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[1]}'!=self.clima_time.strftime("%d-%m"):
            try:
                self.clima_time = self.clima_time.replace(day=self.clima_time.day + op)
            except:
                self.clima_time = self.clima_time.replace(month=self.clima_time.month + op,day=(self.clima_time-(timedelta(days=1) if i==0 else -timedelta(days=1))).day)
            self.btn_nextdia.configure(image=self.arrows[1]) if i==0 else self.btn_prevdia.configure(image=self.arrows[2])
            self.index=self.index+op
            self.imagen1.configure(image=self.imagenes[self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("weatherCodeMin")])
            self.fecha1.configure(text=self.clima_time.strftime("%d/%m/%Y"))
            self.descripcion1.configure(text=self.tipo_clima[self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("weatherCodeMin")])
            self.descripcionDetalle2.configure(text=f"Temp. Avg: {self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("temperatureAvg")}°ᶜ")
            self.descripcionDetalle3.configure(text=f"Amanecer: {(dt.datetime.strptime((self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("sunriseTime").split("T")[1][0:5]),"%H:%M")-timedelta(hours=4)).strftime("%H:%M")}hrs")
            self.descripcionDetalle4.configure(text=f"Atardecer: {(dt.datetime.strptime((self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("sunsetTime").split("T")[1][0:5]),"%H:%M")-timedelta(hours=4)).strftime("%H:%M")}hrs")
            self.descripcionDetalle5.configure(text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("humidityAvg")}%")
            self.dia.configure(text=self.clima_time.strftime("%d"))
            if f'{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[2][0:2]}-{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[1]}'==self.clima_time.strftime("%d-%m"):
                self.btn_prevdia.configure(image=self.arrows[4]) if i==0 else self.btn_nextdia.configure(image=self.arrows[3])
                if self.index==0:
                    self.descripcionDetalle2.configure(text=f"Temp. Max: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMax")}°ᶜ")
                    self.descripcionDetalle3.configure(text=f"Temp. Min: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMin")}°ᶜ")
                    self.descripcionDetalle4.configure(text=f"Viento: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("windSpeedAvg")}km/h")
                    self.descripcionDetalle5.configure(text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("humidityAvg")}%")
    # tercera seccion
    def texto(self):
        self.texto1= ttk.Label(self,font=('Times New Roman',15), text=f"Hoy",background="#22252A",foreground="#FFFFFF")
        self.texto2= ttk.Label(self,font=('Times New Roman',8), text=f"Al minuto",background="#22252A",foreground="#FFFFFF")
    def change_horaYminutomasGrados(self):
        delta=dt.datetime.now()+timedelta(hours=4)
        try:
            for i in range(len(self.data_clima.data.get("timelines").get("minutely"))):
                if self.data_clima.data.get("timelines").get("minutely")[i].get("time") ==f"{delta.strftime("%Y-%m-%d")}T{delta.strftime("%H")}:{delta.strftime("%M")}:00Z":
                    gradoMinute = self.data_clima.data.get("timelines").get("minutely")[i].get("values")
                    break
            self.hora1.configure(text=time.strftime("%H:%M:%S"))
            self.gradosXminuto1.configure(text=f"{gradoMinute.get("temperature")}°ᶜ")
            self.gradosSec1.configure(text=f"{gradoMinute.get("humidity")}% de Humedad")
            self.gradosSec2.configure(text=f"Viento de {gradoMinute.get("windSpeed")}km/h")
        except:
            self.data_clima.apiCall()
        self.after(1000,self.change_horaYminutomasGrados)
    def horaYminutomasGrados(self):
        self.hora1= ttk.Label(self,font=('Times New Roman',15), text="",background="#22252A",foreground="#FFFFFF")
        self.gradosXminuto1= ttk.Label(self,font=('Arial',20), text=f"{"00"}°ᶜ",background="#22252A",foreground="#FFFFFF")
        self.gradosSec1= ttk.Label(self,font=('Arial',10), text=f"{"0"}% de Humedad",background="#22252A",foreground="#FFFFFF")
        self.gradosSec2= ttk.Label(self,font=('Arial',10), text=f"Viento de {"0"}km/h",background="#22252A",foreground="#FFFFFF")
        self.change_horaYminutomasGrados()
    # grid seccion
    def grid(self):
        self.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
        # lineas separadoras 
        self.lines1.place(x=0,y=0,relwidth=0.012,relheight=1)
        self.lines2.place(x=138,y=30,relwidth=0.0009,relheight=1)
        self.lines3.place(x=265,y=0,relwidth=0.012,relheight=1)
        # primera seccion
        self.imagen1.place(x=47,y=56,relwidth=0.2,relx=0,rely=0,relheight=0.65)
        self.descripcionDetalle1.place(x=180,y=18,relwidth=0.1,relx=0,relheight=0.2)
        self.descripcionDetalle2.place(x=140,y=43,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcionDetalle3.place(x=140,y=68,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcionDetalle4.place(x=140,y=93,relwidth=0.297,relx=0,relheight=0.2)
        self.descripcionDetalle5.place(x=140,y=118,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcion1.place(x=5,y=12,relwidth=0.3,relx=0,relheight=0.3)
        self.fecha1.place(x=110,y=4,relwidth=0.3,relx=0,relheight=0.15)
        self.styles.place(x=5,y=0,relwidth=1,relx=0,relheight=1)
        self.dia.grid(row=3,column=0, sticky='')
        self.btn_prevdia.grid(row=4, column=0, sticky='',rowspan=2)
        self.btn_nextdia.grid(row=2, column=0, sticky='',columnspan=1)
        # tercera seccion
        self.texto1.place(x=315,y=0,relwidth=0.3,relx=0,relheight=0.2)
        self.texto2.place(x=305,y=80,relwidth=0.3,relx=0,relheight=0.1)
        self.hora1.place(x=296,y=14,relwidth=0.3,relx=0,relheight=0.3)
        self.gradosXminuto1.place(x=290,y=50,relwidth=0.3,relx=0,relheight=0.2)
        self.gradosSec1.place(x=272,y=93,relwidth=0.3,relx=0,relheight=0.2)
        self.gradosSec2.place(x=274,y=118,relwidth=0.3,relx=0,relheight=0.2)


class seccion_calendario(ttk.Frame):
    ...
CalendarioApp(dt.datetime.today().strftime('%Y-%m-%d'))