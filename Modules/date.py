import main
import datetime

def Init(module: main.Module):
    module.color = '1010101'


def Update(module: main.Module):
    now = datetime.datetime.now()

    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    year = str(now.year).zfill(4)

    date_str = f"{day}.{month}.{year}"

    module.full_text = date_strB