import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
l=[]
def on_closing():
    l.remove(2)
    print(l)

    root.destroy()
l.append(2)
l.append(4)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()