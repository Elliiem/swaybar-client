import main
import psutil

from enum import Enum

class ChargeState(Enum):
    DISCHARGING = 0,
    CHARGING = 1,
    NOT_CHARGING = 2


blink_state = False
def Blink(module: main.Module):
    global blink_state

    if blink_state:
        blink_state = False
        module.settings.background = 'FF0000'
    else:
        blink_state = True
        module.settings.background = 'FFFFFF'


def Init(module: main.Module):
    module.settings.color = '101010'


def Update(module: main.Module):
    charge_state = ChargeState['NOT_CHARGING']

    with open('/sys/class/power_supply/BAT0/status') as file:
        status_str = file.read().strip('\n')

        if status_str == 'Charging':
            charge_status_indicator = '▲'
            charge_state = ChargeState.CHARGING
        elif status_str == 'Discharging':
            charge_status_indicator = '▼'
            charge_state = ChargeState.DISCHARGING
        else:
            charge_status_indicator = '-'
            charge_state = ChargeState.NOT_CHARGING


    battery_percentage = int(psutil.sensors_battery().percent)

    if battery_percentage >= 60:
        module.settings.background = '00FF00'
    elif battery_percentage >= 20:
        module.settings.background = 'FFFF00'
    elif battery_percentage >= 10:
        module.settings.background = 'FF0000'
    elif charge_state == ChargeState.DISCHARGING:
        Blink(module)

    module.full_text = charge_status_indicator + ' ' + str(battery_percentage) + '%'
