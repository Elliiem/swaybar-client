import main
from datetime import datetime
from dateutil.tz import tzlocal


def Init(module: main.Module):
    module.color = '1010101'

def Update(module: main.Module):
    now = datetime.now(tzlocal())

    offset = now.strftime('%z')

    second = str(now.second)
    second = '0' + second if len(second) < 2 else second
    minute = str(now.minute)
    minute = '0' + minute if len(minute) < 2 else minute
    hour = str(now.hour)
    hour = '0' + hour if len(hour) < 2 else hour


    time_str = f"{hour}:{minute}:{second}"


    module.full_text = f"UTC {offset[:-2]}:{offset[-2:]}  {time_str}"