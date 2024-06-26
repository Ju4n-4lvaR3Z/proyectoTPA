import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkcalendar import Calendar
from calender import Calendar  as K


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

    # funcion para abrir la base de datos del programa
    # def load_data(str) -> str 
    def load_data(self):
        try:
            with open("calendario_data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
            print("except")
    
    # funcion que guarda los datos en el diccionario
    # def save_data(int,str) -> int, str (guardados en el atributo (dicionario))
    def save_data(self, date, data):
        self.data[date] = data
        self.save_data_to_file()
    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
    def save_data_to_file(self):
        with open("calendario_data.json", "w") as file:
            json.dump(self.data, file)
            
class getWhether:
    def __init__(self):
        self.data = {}
    def loadData(self):
        with open("whether.json", "r") as file:
            self.data = json.load(file)
        if self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m-%d")}T10:00:00Z" and self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m")}-{"0" if (int(dt.datetime.today().strftime("%d"))-1) <10 else ""}{int(dt.datetime.today().strftime("%d"))-1}T10:00:00Z" :
            self.apiCall()
    def save_data_to_file(self,data):
        with open("whether.json", "w") as file:
            json.dump(data, file)
        self.loadData()
    def apiCall(self):
        print("////////////////API call///////////////////")
        api_key="a51S5D6NSdSEfLhIK5t97rShUgKgLb0T"
        # api_key="xcDOEQGB3KiPXjJmIfYGQXhW4bWpQBja"
        url = f"https://api.tomorrow.io/v4/weather/forecast?location=-40.57395%2C%20-73.13348&units=metric&apikey={api_key}"
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
        self.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        # cargamos las imagenes
        self.arrows={1:ImageTk.PhotoImage(Image.open("img/up-arrow.png").resize((20,20), Image.LANCZOS)),
                     2:ImageTk.PhotoImage(Image.open("img/down-arrow.png").resize((20,20), Image.LANCZOS)),
                     11:ImageTk.PhotoImage(Image.open("img/up-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     22:ImageTk.PhotoImage(Image.open("img/down-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     3:ImageTk.PhotoImage(Image.open("img/left-arrow.png").resize((20,20), Image.LANCZOS)),
                     33:ImageTk.PhotoImage(Image.open("img/left-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     4:ImageTk.PhotoImage(Image.open("img/right-arrow.png").resize((20,20), Image.LANCZOS)),
                     44:ImageTk.PhotoImage(Image.open("img/right-arrow-lock.png").resize((20,20), Image.LANCZOS))}
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
                       8000:ImageTk.PhotoImage(Image.open("img/8000.png").resize((80,80), Image.LANCZOS)),
                       "LogoG":ImageTk.PhotoImage(Image.open("img/LogoGrande.png").resize((200,100), Image.LANCZOS)),
                       "ico":ImageTk.PhotoImage(Image.open("img/LogoGrande.png").resize((200,100), Image.LANCZOS)),
                       "cancelar":ImageTk.PhotoImage(Image.open("img/cancelar.png").resize((100,20), Image.LANCZOS)),
                       "guardar":ImageTk.PhotoImage(Image.open("img/guardar.png").resize((100,20), Image.LANCZOS)),
                       "settings":ImageTk.PhotoImage(Image.open("img/settings.png").resize((20,20), Image.LANCZOS))}
        # parametros del clima
        self.tipo_clima={1000:"Despejado",1001:"Nublado",1100:"Mayormente Despejado",1101:"Parcialmente Nublado",
                         1102:"Mayormente Nublado",2000:"Neblina",2100:"Ligera Neblina",4000:"Llovizna",4200:"Lluvia Ligera",
                         4001:"Lluvia",4201:"Lluvia Intensa",5001:"Neviscas",5100:"Nieve Ligera",5000:"Nieve",
                         5101:"Nieve Ligera",6000:"Llovizna Helada",6001:"Lluvia Helada",6200:"Lluvia Helada Ligera",
                         6201:"lluvia helada Intensa",7102:"Ligera Hielo Granulado",7000:"Hielo Granulado",7101:"Hielo Granulado Intenso",
                         8000:"Tormenta"}
        # controles del calendario

        self.bienvenida= bienvenida(self,fecha)
        # panel del clima
        self.control_clima=seccion_clima(self,fecha)
        self.seccion_calendario=seccion_calendario(self)
        self.mainloop()

class bienvenida(ttk.Frame):
    def __init__(self, parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=0,y=0,relwidth=0.4,relheight=0.2)
        self.calendario_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.data_Manager=DataManager()
        self.data_Manager.load_data()
        self.arrows=parent.arrows
        self.anio_cambio= StringVar()
        self.mes_cambio= StringVar()
        self.imagenes=parent.imagenes
        self.style()
        self.content()
        self.grid()
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background="#22252A",foreground="#FFFFFF")
    def content(self):
        months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.fecha1= ttk.Label(self,font=("arial", 14) , text=f"{self.calendario_time.strftime("%d")} de {months[int(self.calendario_time.strftime("%m"))-1]} de {self.calendario_time.strftime("%Y")}",background="#22252A",foreground="#FFFFFF")
        self.config = ttk.Button(self,command=self.login,image=self.imagenes["settings"])
# bind("<<CalendarSelected>>", self.on_date_click)
        self.logo= ttk.Label(self,font='1',background="#22252A",image=self.imagenes["LogoG"])
    def grid(self):
        self.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.columnconfigure((0,1,2,3),weight=1,uniform='a')

        self.logo.place(x=50,y=0)
        self.config.place(x=10,y=10)
        self.fecha1.place(x=0,y=100,relwidth=1,relx=0.19,relheight=0.3)
        self.styles.place(x=0,y=0,relwidth=1,relx=0,relheight=1)
    # pantalla login
    def login(self):
        self.top = Toplevel(self.master)
        self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.top.title("Block de notas")
        self.top.geometry("500x300")
        self.top.minsize(500,300)
        self.top.maxsize(500,300)
        self.top.config(background="#22252A")
        # grid 
        self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
        

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
        self.btn_prevdia = ttk.Button(self,command=self.prev_dia,image=self.arrows[22])
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
                self.btn_prevdia.configure(image=self.arrows[22]) if i==0 else self.btn_nextdia.configure(image=self.arrows[11])
                if self.index==0:
                    self.descripcionDetalle2.configure(text=f"Temp. Max: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMax")}°ᶜ")
                    self.descripcionDetalle3.configure(text=f"Temp. Min: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMin")}°ᶜ")
                    self.descripcionDetalle4.configure(text=f"Viento: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("windSpeedAvg")}km/h")
                    self.descripcionDetalle5.configure(text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("humidityAvg")}%")
    # segunda seccion
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
            self.gradosSec2.configure(text=f"Viento de {gradoMinute.get("windSpeed")} km/h")
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
    def __init__(self,parent):
        super().__init__(parent)
        ttk.Label(self)
        self.data_Manager=DataManager()
        self.data_Manager.load_data()
        self.data_clima=getWhether()
        self.data_clima.loadData()
        self.place(x=0,y=150,relwidth=1,relheight=1)
        self.imagen=parent.imagenes
        self.calendario=K(self)
        self.selected_date = StringVar()
        self.calendario.place(x=0,y=0,relwidth=1,relx=0,relheight=0.785)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_click)

    def on_date_click(self, event):
        self.selected_date.set(self.calendario.get_date())
        self.top = Toplevel(self.master)
        self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.top.title("Block de notas")
        self.top.geometry("400x600")
        self.top.minsize(400,600)
        self.top.maxsize(400,600)
        self.top.config(background="#22252A")
        getdate=self.calendario.get_date().split("/")
        t=False
        # delta=dt.datetime.now()+timedelta(hours=4)
        # c=1
        # c2=0
        # for i in range(len(self.data_clima.data.get("timelines").get("hourly"))):
        #     # try:

        #             d=f"20{getdate[2]}-{"0" if int(getdate[1])<10 else ""}{getdate[1]}-{"0" if int(getdate[0])<10 else ""}{getdate[0]}T{"0" if c+4<10 else ""}{c+4}:00:00z" if c+4<24 else f"20{getdate[2]}-{"0" if int(getdate[1])<10 else ""}{getdate[1]}-{"0" if int(getdate[0])<10 else ""}{int(getdate[0])+1}T{"0" if c+4<10 else ""}{(c+4)-24}:00:00z"
        #             print(self.data_clima.data.get("timelines").get("hourly")[i].get("time"),"  ",d)
        #             if d==self.data_clima.data.get("timelines").get("hourly")[i].get("time"):
        #             # error si o si, arreglar
        #                 print(c,d," hrs --", self.data_clima.data.get("timelines").get("hourly")[i].get("values").get("temperature"))
        #                 c+=1
        #                 if c==24: break
            # except:
            #     print("ni puta idea bru")
            # if ((self.data_clima.data.get("timelines").get("hourly")[i].get("time")).split("T")[0]) ==f"20{getdate[2]}-{"0" if int(getdate[1])<10 else ""}{getdate[1]}-{"0" if int(getdate[0])<10 else ""}{getdate[0]}":

            #     t=TRUE
            #     c+=1
            #     print(c," ",((self.data_clima.data.get("timelines").get("hourly")[0].get("time")))," ",f"20{getdate[2]}-{"0" if int(getdate[1])<10 else ""}{getdate[1]}-{"0" if int(getdate[0])<10 else ""}{getdate[0]}"," ",f"{dt.datetime.now().strftime("%Y-%m-%d")}")

                
        # info del clima
        # if t==TRUE:
        #     # horas y grados
        #     self.descripcionxhoraH1= ttk.Label(self.top,font=('Arial',10), text=f"01 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH2= ttk.Label(self.top,font=('Arial',10), text=f"02 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH3= ttk.Label(self.top,font=('Arial',10), text=f"03 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH4= ttk.Label(self.top,font=('Arial',10), text=f"04 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH5= ttk.Label(self.top,font=('Arial',10), text=f"05 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH6= ttk.Label(self.top,font=('Arial',10), text=f"06 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH7= ttk.Label(self.top,font=('Arial',10), text=f"07 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH8= ttk.Label(self.top,font=('Arial',10), text=f"08 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH9= ttk.Label(self.top,font=('Arial',10), text=f"09 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH10= ttk.Label(self.top,font=('Arial',10), text=f"10 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH11= ttk.Label(self.top,font=('Arial',10), text=f"11 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH12= ttk.Label(self.top,font=('Arial',10), text=f"12 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH13= ttk.Label(self.top,font=('Arial',10), text=f"13 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH14= ttk.Label(self.top,font=('Arial',10), text=f"14 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH15= ttk.Label(self.top,font=('Arial',10), text=f"15 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH16= ttk.Label(self.top,font=('Arial',10), text=f"16 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH17= ttk.Label(self.top,font=('Arial',10), text=f"17 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH18= ttk.Label(self.top,font=('Arial',10), text=f"18 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH19= ttk.Label(self.top,font=('Arial',10), text=f"19 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH20= ttk.Label(self.top,font=('Arial',10), text=f"20 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH21= ttk.Label(self.top,font=('Arial',10), text=f"21 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH22= ttk.Label(self.top,font=('Arial',10), text=f"22 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH23= ttk.Label(self.top,font=('Arial',10), text=f"23 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")
        #     self.descripcionxhoraH24= ttk.Label(self.top,font=('Arial',10), text=f"24 Hrs {"10°"}",background="#22252A",foreground="#FFFFFF")

        # entry de texto
        day_data = self.data_Manager.data.get(self.calendario.get_date(), "")
        self.event_entry = Text(self.top,wrap=tk.WORD, height=3, width=30,background="#E6DFCE")
        self.event_entry.insert(tk.END, day_data)
        # bortones
        self.boton1= ttk.Button(self.top,text="CANCELAR",image=self.imagen["cancelar"],command=self.top.destroy)
        self.boton2= ttk.Button(self.top, command=(lambda:self.save_data(self.calendario.get_date(),self.event_entry.get("1.0",tk.END))) ,image=self.imagen["guardar"])


        #grid general
        self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
        # if t==TRUE:
        #     # horas y grados
        #     self.descripcionxhoraH1.place(x=1.2,y=5+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH2.place(x=1.2,y=5+27,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH3.place(x=1.2,y=5+49,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH4.place(x=1.2,y=5+71,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH5.place(x=1.2,y=5+93,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH6.place(x=1.2,y=5+115,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH7.place(x=1.2,y=5+137,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH8.place(x=1.2,y=5+159,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH9.place(x=1.2,y=5+181,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH10.place(x=1.2,y=203+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH11.place(x=1.2,y=225+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH12.place(x=1.2,y=247+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH13.place(x=1.2,y=269+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH14.place(x=1.2,y=291+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH15.place(x=1.2,y=313+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH16.place(x=1.2,y=335+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH17.place(x=1.2,y=357+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH18.place(x=1.2,y=379+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH19.place(x=1.2,y=401+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH20.place(x=1.2,y=423+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH21.place(x=1.2,y=445+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH22.place(x=1.2,y=467+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH23.place(x=1.2,y=489+5,relwidth=0.2,relx=0,relheight=0.05)
        #     self.descripcionxhoraH24.place(x=1.2,y=511+5,relwidth=0.2,relx=0,relheight=0.05)

        self.event_entry.place(x=31,y=10,relwidth=0.82,relx=0,relheight=0.9) if t==False else self.event_entry.place(x=66,y=10,relwidth=0.82,relx=0,relheight=0.9)
        self.boton1.place(x=30,y=560,relwidth=0.3,relx=0,relheight=0.05)
        self.boton2.place(x=240,y=560,relwidth=0.3,relx=0,relheight=0.05)
    def save_data(self,date, data):
        self.data_Manager.save_data(date, data)
        self.top.destroy()


CalendarioApp(dt.datetime.today().strftime('%Y-%m-%d'))