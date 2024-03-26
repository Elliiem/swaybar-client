import main
import datetime

def Init(module: main.Module):
    module.color = '1010101'


def Update(module: main.Module):
    now = datetime.datetime.now()

    day = str(now.day)
    day = '0' + day if len(day) < 2 else day
    month = str(now.month)
    month = '0' + month if len(month) < 2 else month
    year = str(now.year)

    date_str = f"{day}.{month}.{year}"

    module.full_text = date_str

