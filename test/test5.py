import requests
import json

url = "https://api.tomorrow.io/v4/weather/forecast?location=Osorno%2C%20Los%20Lagos%2C%20Chile&units=metric&apikey=xcDOEQGB3KiPXjJmIfYGQXhW4bWpQBja"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
with open("1.json", "w") as file:
    json.dump(json.loads(response.text), file)
print(response.text)
print(type(response.text))