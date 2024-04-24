import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from tkcalendar import Calendar
import datetime as dt
from PIL import Image, ImageTk
from os import *
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
        if self.data.get("timelines").get("daily")[0].get("time")==f"{dt.datetime.now().strftime("%Y-%m-%d")}T10:00:00Z":
            self.data = json.load(file)
        else:
            self.apiCall()
    def save_data_to_file(self,data):
        with open("whether.json", "w") as file:
            json.dump(data, file)
        self.loadData()
    def apiCall(self):
        url = "https://api.tomorrow.io/v4/weather/forecast?location=Osorno%2C%20Los%20Lagos%2C%20Chile&units=metric&apikey=xcDOEQGB3KiPXjJmIfYGQXhW4bWpQBja"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        js=json.loads(response.text())
        self.save_data_to_file(js)

class CalendarioApp(tk.Tk):
    def __init__(self,fecha):
        # configucacion
        super().__init__()
        self.title=('Calendatio')
        self.geometry('700x700')
        self.minsize(700,700)
        self.maxsize(700,700)
        self.config(background="#22252A")
        # controles del calendario
        self.control_calendario= control_calendario(self,fecha)
        self.control_clima=seccion_clima(self)
        self.mainloop()

class control_calendario(ttk.Frame):
    def __init__(self, parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=0,y=0,relwidth=0.4,relheight=0.2)
        self.calendario_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.up_arrow= ImageTk.PhotoImage(Image.open("img/up-arrow.png").resize((20,20), Image.LANCZOS))
        self.down_arrow= ImageTk.PhotoImage(Image.open("img/down-arrow.png").resize((20,20), Image.LANCZOS))
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
        self.btn_prevmes = ttk.Button(self, text="🔽",command=self.prev_month,image=self.down_arrow)
        self.btn_prevanio = ttk.Button(self, text="🔽",command=self.prev_year,image=self.down_arrow)
    def mes_anio(self):
        self.anio= ttk.Label(self, textvariable=self.anio_cambio,background="#22252A",foreground="#FFFFFF")
        self.mes= ttk.Label(self, textvariable=self.mes_cambio,background="#22252A",foreground="#FFFFFF")
    def controles_adelante(self):
        self.btn_nextmes = ttk.Button(self, text="🔼",command=self.next_month,image=self.up_arrow)
        self.btn_nextanio = ttk.Button(self, text="🔼",command=self.next_year,image=self.up_arrow)
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
    def __init__(self,parent):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=300,y=0,relwidth=0.6,relheight=0.2)
        self.clima=getWhether()
        self.line()
        self.style()
    def style(self):
        styles=ttk.Label(self,font='1', text=f"",background="#24ACF2",foreground="#FFFFFF")
        styles.place(x=5,y=0,relwidth=1,relheight=1)
    def line(self):
        styles=ttk.Label(self,font='1', text=f"",background="#E5A769")
        styles.place(x=0,y=0,relwidth=1,relheight=1)
class seccion_calendario(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title("Calendario")
        self.master.geometry("500x350")
        self.master.config(bg="gray")

        self.cal = Calendar(self.master, select="day", year=2024, month=1, day=1)
        self.cal.pack(pady=20, fill="both", expand="yes")

        self.selected_date = StringVar()

        self.cal.bind("<<CalendarSelected>>", self.on_date_click)

    def save_data(self):
        data = {
            "date": self.selected_date.get(),
            "event": self.event_entry.get()
        }
        with open("data.json", "a") as file:
            json.dump(data, file)
            file.write("\n")
        messagebox.showinfo("Guardado", "Datos guardados correctamente.")

    def show_saved_data(self):
        with open("data.json", "r") as file:
            for line in file:
                data = json.loads(line)
                if data["date"] == self.selected_date.get():
                    messagebox.showinfo("Evento para el día", f"{data['event']}")
                    return
            messagebox.showinfo("Evento para el día", "No hay eventos guardados para este día.")

    def on_date_click(self, event):
        self.selected_date.set(self.cal.get_date())
        top = Toplevel(self.master)
        top.title("Guardar Datos")
        top.geometry("300x200")

        self.event_entry = Entry(top, width=30)
        self.event_entry.pack(pady=10)

        save_button = Button(top, text="Guardar", command=self.save_data)
        save_button.pack(pady=10)

        show_button = Button(top, text="Mostrar evento", command=self.show_saved_data)
        show_button.pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    app = CalendarioApp(root)
    root.mainloop()

CalendarioApp(dt.datetime.today().strftime('%Y-%m-%d'))
# CalendarioApp("2004-05-25")