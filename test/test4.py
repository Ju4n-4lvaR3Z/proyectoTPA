import datetime as dt
import json
import os

# open(f"whether.json", "r")
# json.dump(
# 
class DataWhether:

    # funcion para abrir la base de datos del programa
    # def load_data(str) -> str 
    def load_data(self):
        try:
            with open("whether.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
    
    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
def save_data_to_file(self):
    with open("whether.json", "w") as file:
        json.dump(self.data, file)
# open("1.json", "x")
with open("1.json", "r") as file:
    data = json.load(file)

print(data)
    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
data1={"chao":"chao"}
with open("1.json", "w") as file:
    json.dump(data1, file)
with open("1.json", "r") as file:
    data = json.load(file)
print(data)