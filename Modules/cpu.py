import main

import psutil

def Init(module: main.Module):
    module.color = '000000'

    module.background = '4040FF'
    module.border = '4040FF'

    module.border_left = 1
    module.border_right = 1

    module.separator = False
    module.separator_block_width = 0


def Update(module: main.Module):
    cpu_percent = str(round(psutil.cpu_percent()))

    module.full_text = f'cpu: {cpu_percent}%'