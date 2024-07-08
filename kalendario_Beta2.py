import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from calender import Calendar  as K

import sys
import os

import time
import datetime as dt
from datetime import timedelta
from PIL import Image, ImageTk
import requests
import json

# apis
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
    def save_data(self,user, date, data):
        self.data.get("users")[user].get("data")[date] = data
        self.save_data_to_file()
    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
    def save_data_to_file(self):
        with open("calendario_data.json", "w") as file:
            json.dump(self.data, file)
    def get_user(self):
        return self.data.get("sesion").get("actual")[0]
    def get_color(self,user):
        return self.data.get("users")[user].get("color")
    def logIn(self,i):
        self.data.get("sesion")["actual"] = f"{i}"
        self.save_data_to_file()
        self.restart()
    def register(self,user,password):
        self.data.get("users").append(
            {
            "id": len(self.data.get("users")),
            "name": f"{user}",
            "contrasena": f"{password}",
            "settings": "Black",
            "data": {
            }
            }
            )
        self.save_data_to_file()
    def restablecer(self,i,password):
        self.data.get("users")[i] = {
            "id": self.data.get("users")[i].get("id"),
            "name": self.data.get("users")[i].get("name"),
            "contrasena": f"{password}",
            "settings": self.data.get("users")[i].get("settings"),
            "data": self.data.get("users")[i].get("data")
            }
        self.save_data_to_file()
    def logOut(self):
        self.data.get("sesion")["actual"] = "N"
        self.save_data_to_file()
        self.restart()
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

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

class Color:
    def __init__(self):
        self.color_actual = self.colores.get("Actual", list(self.colores.values())[0] if self.colores else {"principal": "#151515", "subcolores": ["#59595B"], "texto": "white"})

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


# kalendario app
class CalendarioApp(tk.Tk):
    def __init__(self,fecha):
        # configucacion
        super().__init__()
        self.title('Kalendario')
        self.geometry('700x700')
        self.minsize(700,700)
        self.maxsize(700,700)
        self.data_Manager=DataManager()
        self.data_Manager.load_data()
        self.user=self.data_Manager.get_user()
        # self.color=Color()
        # self.color.cargar_color(self.data_Manager.get_color(int(self.user))) if self.user !="N" else self.color.cargar_default()
        # self.colorBG=self.color
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
                       "settings":ImageTk.PhotoImage(Image.open("img/settings.png").resize((20,20), Image.LANCZOS)),
                       "entrar":ImageTk.PhotoImage(Image.open("img/entrar.png").resize((90,20), Image.LANCZOS)),
                       "registro":ImageTk.PhotoImage(Image.open("img/registro.png").resize((90,20), Image.LANCZOS)),
                       "restablecer":ImageTk.PhotoImage(Image.open("img/restablecer.png").resize((90,20), Image.LANCZOS)),
                       "salir":ImageTk.PhotoImage(Image.open("img/salir.png").resize((90,20), Image.LANCZOS)),
                       "seguro":ImageTk.PhotoImage(Image.open("img/seguro.png").resize((90,20), Image.LANCZOS))}
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
        self.seccion_calendario=seccion_calendario(self,fecha)
        self.mainloop()

class bienvenida(ttk.Frame):
    def __init__(self, parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=0,y=0,relwidth=0.4,relheight=0.2)
        self.calendario_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.data_Manager=parent.data_Manager
        self.arrows=parent.arrows
        self.anio_cambio= StringVar()
        self.mes_cambio= StringVar()
        self.imagenes=parent.imagenes
        self.user=parent.user
        self.style()
        self.content()
        self.grid()
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background="#22252A",foreground="#FFFFFF")
    def content(self):
        months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.fecha1= ttk.Label(self,font=("arial", 14) , text=f"{self.calendario_time.strftime("%d")} de {months[int(self.calendario_time.strftime("%m"))-1]} de {self.calendario_time.strftime("%Y")}",background="#22252A",foreground="#FFFFFF")
        self.config = ttk.Button(self,command=self.controlpanel,image=self.imagenes["settings"])
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
    def controlpanel(self):
        self.top = Toplevel(self.master)
        self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.top.title("Control de Usuario")
        self.top.geometry("500x300") if self.user=="N" else self.top.geometry("300x200")
        self.top.minsize(500,300) if self.user=="N" else  self.top.minsize(300,200)
        self.top.maxsize(500,300) if self.user=="N" else self.top.maxsize(300,200)
        self.top.config(background="#22252A")
        if self.user=="N":
            self.lines3=ttk.Label(self.top,font='1', text=f"",background="#E5A769")
            # login
            self.txtLogin = ttk.Label(self.top,font='1',text="INGRESO",background="#22252A",foreground="#FFFFFF",)
            self.textname= ttk.Label(self.top,font=('Arial',8),text="Usuario",background="#22252A",foreground="#FFFFFF",)
            self.name=ttk.Entry(self.top,font=('calibre',10,'normal'))
            self.textpassword= ttk.Label(self.top,font=('Arial',8),text="Contraseña",background="#22252A",foreground="#FFFFFF",)
            self.password=ttk.Entry(self.top,font=('calibre',10,'normal'))
            self.LogIn = ttk.Button(self.top,command=(lambda:self.validateLogin(self.name.get(),self.password.get())),image=self.imagenes["entrar"])
            self.txtOlvido= ttk.Label(self.top,font=('Arial',8),text="Olvido su contraseña?",background="#22252A",foreground="#74ADEA",)
            # register
            self.txtRegister = ttk.Label(self.top,font='1',text="REGISTRO",background="#22252A",foreground="#FFFFFF",)
            self.textRname= ttk.Label(self.top,font=('Arial',8),text="Usuario",background="#22252A",foreground="#FFFFFF",)
            self.Rname=ttk.Entry(self.top,font=('calibre',10,'normal'))
            self.textRpassword= ttk.Label(self.top,font=('Arial',8),text="Contraseña",background="#22252A",foreground="#FFFFFF",)
            self.Rpassword=ttk.Entry(self.top,font=('calibre',10,'normal'))
            self.textRDpassword= ttk.Label(self.top,font=('Arial',8),text="Otra vez",background="#22252A",foreground="#FFFFFF",)
            self.RDpassword=ttk.Entry(self.top,font=('calibre',10,'normal'))
            self.Register = ttk.Button(self.top,command=(lambda:self.validateRegister(self.Rname.get(),self.Rpassword.get(),self.RDpassword.get())),image=self.imagenes["registro"])
            
            # ERROR
            self.error=ttk.Label(self.top,font=('Arial',10),text="",background="#22252A",foreground="#CD3D49")
            # grid 
            self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
            self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
            # linea
            self.lines3.place(x=250,y=20,relwidth=0.0019,relheight=0.8)
            # login grid
            self.txtLogin.place(x=85,y=40,relwidth=0.2,relheight=0.1)   
            self.textname.place(x=70,y=70,relwidth=0.2,relheight=0.06)   
            self.name.place(x=70,y=90,relwidth=0.25,relheight=0.1) 
            self.textpassword.place(x=70,y=120,relwidth=0.2,relheight=0.06)  
            self.password.place(x=70,y=140,relwidth=0.25,relheight=0.1)    
            self.LogIn.place(x=80,y=180,relwidth=0.2,relx=0,relheight=0.1)
            self.txtOlvido.place(x=75,y=210,relwidth=0.3,relheight=0.06)  
            self.txtOlvido.bind("<Button-1>", lambda event, txtOlvido=self.txtOlvido:self.restablece())

            # register grid
            self.txtRegister.place(x=325,y=40,relwidth=0.3,relheight=0.1) 
            self.textRname.place(x=315,y=70,relwidth=0.2,relheight=0.06)   
            self.Rname.place(x=315,y=90,relwidth=0.25,relheight=0.1) 

            self.textRpassword.place(x=295,y=120,relwidth=0.2,relheight=0.06)  
            self.Rpassword.place(x=280,y=140,relwidth=0.18,relheight=0.1)    
            self.textRDpassword.place(x=400,y=120,relwidth=0.2,relheight=0.06)  
            self.RDpassword.place(x=380,y=140,relwidth=0.18,relheight=0.1)    

            self.Register.place(x=325,y=180,relwidth=0.2,relx=0,relheight=0.1)

            # error grid
            self.error.place(x=200,y=260,relwidth=0.3,relheight=0.1)
        else:
            # panel de usuario
            self.txtuser = ttk.Label(self.top,font='1',text=f"{self.data_Manager.data.get("users")[int(self.user)].get("name")}",background="#22252A",foreground="#FFFFFF",)
            self.salir = ttk.Button(self.top,command=(lambda:self.logOut()),image=self.imagenes["salir"])
            # grid 
            self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
            self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
            self.txtuser.place(x=10,y=0,relwidth=1,relheight=0.4)   
            self.salir.place(x=80,y=160,relwidth=0.4,relx=0,relheight=0.2)

    def admin(self,user,password,rpassword):
        self.topadmin = Toplevel(self.master)
        self.topadmin.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.topadmin.title("Control de admin")
        self.topadmin.geometry("300x100")
        self.topadmin.minsize(300,100)
        self.topadmin.maxsize(300,100)
        self.topadmin.config(background="#22252A")

        self.topadmin.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.topadmin.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')

        self.textRDpassword= ttk.Label(self.topadmin,font=('Arial',8),text="Contraseña Admin",background="#22252A",foreground="#FFFFFF",)
        self.passwordAdmin=ttk.Entry(self.topadmin,font=('calibre',10,'normal'))
        self.restablecer = ttk.Button(self.topadmin,command=(lambda:self.validateadmin(self.passwordAdmin.get(),user,password,rpassword)),image=self.imagenes["restablecer"])
        
        self.textRDpassword.place(x=50,y=15,relwidth=0.7,relheight=0.2)  
        self.passwordAdmin.place(x=50,y=35,relwidth=0.7,relheight=0.2)    
        self.restablecer.place(x=100,y=60,relwidth=0.34,relx=0,relheight=0.28)

    def validateadmin(self,adminpassword,user,password,rpassword):
        if adminpassword==self.data_Manager.data.get("admin").get("contrasena"):
            self.validaterestablecer(user,password,rpassword)
            self.topadmin.destroy()
    def validateLogin(self,user,password):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
                if password==self.data_Manager.data.get("users")[i].get("contrasena"):
                    self.data_Manager.logIn(i)
                else:
                    self.error.configure(text="Contraseña incorrecta")
            i+=1
            
        self.error.configure(text="No existe usuario") if s==0 else None
    
    def validateRegister(self,user,password,rpassword):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
        if user=="" or password=="" or rpassword=="":
            self.error.configure(text="Un campo esta vacio")
        elif not user.isalpha() :
            self.error.configure(text="Usuario inválido")
        elif s==1:
            self.error.configure(text="Usuario ya existe")
        elif password==rpassword:
            self.data_Manager.register(user,password)
            self.error.configure(text="Cuenta creada, Ingrese",foreground="#A1B658")
        else:
            self.error.configure(text="Contraseñas desiguales")
    def restablece(self):
        self.txtRegister.configure(text="RESTABLECER")
        self.textRpassword.configure(text="Nueva Contraseña")
        self.Register.configure(command=(lambda:self.admin(self.Rname.get(),self.Rpassword.get(),self.RDpassword.get())),image=self.imagenes["restablecer"])
    def validaterestablecer(self,user,password,rpassword):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
                if password==rpassword:
                    self.data_Manager.restablecer(i,password)

                    self.error.configure(text="Contraseña creada",foreground="#A1B658")
                else:
                    self.error.configure(text="Contraseñas desiguales")
        self.error.configure(text="No existe usuario") if s ==0 else None
    def logOut(self):
        self.salir.configure(command=(lambda:self.data_Manager.logOut()),image=self.imagenes["seguro"])

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
    def __init__(self,parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.user=parent.user
        self.data_Manager=parent.data_Manager
        self.data_clima=getWhether()
        self.data_clima.loadData()
        self.place(x=0,y=150,relwidth=1,relheight=1)
        self.imagen=parent.imagenes
        self.calendario=K(self)
        self.selected_date = StringVar()
        self.calendario.place(x=0,y=0,relwidth=1,relx=0,relheight=0.785)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_click) if self.user!="N" else self.calendario.bind("<<CalendarSelected>>", bienvenida(parent,fecha).controlpanel())

    def on_date_click(self, event):
        self.selected_date.set(self.calendario.get_date())
        self.top = Toplevel(self.master)
        self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.top.title("Block de notas")
        self.top.geometry("400x600")
        self.top.minsize(400,600)
        self.top.maxsize(400,600)
        self.top.config(background="#22252A")
        
        # entry de texto
        day_data = self.data_Manager.data.get("users")[int(self.user)].get("data").get(self.calendario.get_date(), "")
        self.event_entry = Text(self.top,wrap=tk.WORD, height=3, width=30,background="#E6DFCE")
        self.event_entry.insert(tk.END, day_data)
        # bortones
        self.boton1= ttk.Button(self.top,text="CANCELAR",image=self.imagen["cancelar"],command=self.top.destroy)
        self.boton2= ttk.Button(self.top, command=(lambda:self.save_data(self.calendario.get_date(),self.event_entry.get("1.0",tk.END))) ,image=self.imagen["guardar"])


        #grid general
        self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
        
        self.event_entry.place(x=31,y=10,relwidth=0.82,relx=0,relheight=0.9)
        self.boton1.place(x=30,y=560,relwidth=0.3,relx=0,relheight=0.05)
        self.boton2.place(x=240,y=560,relwidth=0.3,relx=0,relheight=0.05)
    def save_data(self,date, data):
        self.data_Manager.save_data(int(self.user),date, data)
        self.top.destroy()


CalendarioApp(dt.datetime.today().strftime('%Y-%m-%d'))