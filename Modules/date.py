import main
import datetime

def Init(module: main.Module):
    module.color = 'FFFFFF'

    module.background = '802050'
    module.border = '802050'

    module.separator = False
    module.separator_block_width = 0

    module.border_left = 1
    module.border_right = 1


def Update(module: main.Module):
    now = datetime.datetime.now()

    day = str(now.day)
    day = '0' + day if len(day) < 2 else day
    month = str(now.month)
    month = '0' + month if len(month) < 2 else month
    year = str(now.year)

    date_str = day + '-' + month + '-' + year

    module.full_text = date_str

