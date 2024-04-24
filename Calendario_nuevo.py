from tkinter import *
from tkcalendar import *
import json
from tkinter import messagebox

def save_data():
    data = {
        "date": selected_date.get(),
        "event": event_entry.get()
    }
    with open("Calendario_data.json", "a") as file:
        json.dump(data, file)
        file.write("\n")
    messagebox.showinfo("Guardado", "Datos guardados correctamente.")

def show_saved_data():
    with open("Calendario_.json", "r") as file:
        for line in file:
            data = json.loads(line)
            if data["date"] == selected_date.get():
                messagebox.showinfo("Evento para el dia", f"{data['event']}")
                return
        messagebox.showinfo("Evento para el dia", "No hay eventos guardados para este dia.")

def on_date_click(event):
    selected_date.set(cal.get_date())
    top = Toplevel(root)
    top.title("Guardar Datos")
    top.geometry("300x200")

    global event_entry
    event_entry = Entry(top, width=30)
    event_entry.pack(pady=10)

    save_button = Button(top, text="Guardar", command=save_data)
    save_button.pack(pady=10)

    show_button = Button(top, text="Mostrar evento", command=show_saved_data)
    show_button.pack(pady=10)

root = Tk()
root.title("Calendario")
root.geometry("500x350")
root.config(bg="gray")

cal = Calendar(root, select="day", year=2024, month=1, day=1)
cal.pack(pady=20, fill="both", expand="yes")

selected_date = StringVar()

cal.bind("<<CalendarSelected>>", on_date_click)

root.mainloop()


root.mainloop()