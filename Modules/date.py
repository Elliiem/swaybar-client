import main
import datetime

def Init(module: main.Module):
    module.settings.color = '1010101'

def Update(module: main.Module):
    now = datetime.datetime.now()

    second = str(now.second)
    second = '0' + second if len(second) == 1 else second
    minute = str(now.minute)
    minute = '0' + minute if len(minute) == 1 else minute
    hour = str(now.hour)
    hour = '0' + hour if len(hour) == 1 else hour

    module.full_text = hour + ':' + minute + ':' + second

