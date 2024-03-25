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


    time_str = hour + ':' + minute + ':' + second


    module.full_text = "UTC +01:00" + ' ' + time_str

