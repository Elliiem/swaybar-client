import main
import datetime

def Init(module: main.Module):
    module.color = '000000'

    module.background = '600060'
    module.border = '600060'

    module.border_left = 1
    module.border_right = 1

    module.separator = False
    module.sep_block_width = 0


def Update(module: main.Module):
    now = datetime.datetime.now()

    second = str(now.second).zfill(2)
    minute = str(now.minute).zfill(2)
    hour = str(now.hour).zfill(2)


    module.full_text = f'{hour}:{minute}:{second}'
