import main
from datetime import datetime
from dateutil.tz import tzlocal


def Init(module: main.Module):
    module.color = '1010101'

def Update(module: main.Module):
    now = datetime.now(tzlocal())

    offset = now.strftime('%z')

    second = str(now.second).zfill(2)
    minute = str(now.minute).zfill(2)
    hour = str(now.hour).zfill(2)


    time_str = f"{hour}:{minute}:{second}"


    module.full_text = f"UTC {offset[:-2]}:{offset[-2:]}  {time_str}"