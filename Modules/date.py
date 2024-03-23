import main
import datetime

def Init(module: main.Module):
    module.color = '1010101'

def Update(module: main.Module):
    now = datetime.datetime.now()

    second = str(now.second)
    second = '0' + second if len(second) < 2 else second
    minute = str(now.minute)
    minute = '0' + minute if len(minute) < 2 else minute
    hour = str(now.hour)
    hour = '0' + hour if len(hour) < 2 else hour
    day = str(now.day)
    day = '0' + day if len(day) < 2 else day
    month = str(now.month)
    month = '0' + month if len(month) < 2 else month
    year = str(now.year)


    time_str = hour + ':' + minute + ':' + second

    date_str = day + '-' + month + '-' + year

    module.full_text = date_str + ' ' + time_str

