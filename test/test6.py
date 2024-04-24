import datetime as dt
from datetime import timedelta
delta=dt.datetime.now()+timedelta(hours=4)

print(f"{delta.strftime("%Y-%m-%d")}T{delta.strftime("%H")}:{delta.minute}:00Z")
print("2024-04-24T04:25:00Z")