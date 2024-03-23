import main
import psutil

from enum import Enum

class ChargeStatus(Enum):
    DISCHARGING = 0,
    CHARGING = 1,
    NOT_CHARGING = 2

    def GetChargeStatus() -> 'ChargeStatus':
        charge_status = psutil.sensors_battery().power_plugged

        if charge_status:
            return ChargeStatus.CHARGING
        elif not charge_status:
            return ChargeStatus.DISCHARGING
        else:
            return ChargeStatus.NOT_CHARGING



blink_state = False
def Blink(module: main.Module):
    global blink_state

    if blink_state:
        blink_state = False
        module.background = 'FF0000'
    else:
        blink_state = True
        module.background = 'FFFFFF'


def Init(module: main.Module):
    module.color = '101010'


def Update(module: main.Module):
    charge_status = ChargeStatus.GetChargeStatus()

    status_indicator = ''
    match charge_status:
        case ChargeStatus.CHARGING:
            status_indicator = '▲'
        case ChargeStatus.DISCHARGING:
            status_indicator = '▼'
        case ChargeStatus.NOT_CHARGING:
            status_indicator = '🔋'

    battery_percentage = int(psutil.sensors_battery().percent)

    if battery_percentage >= 60:
        module.background = '00FF00'
    elif battery_percentage >= 20:
        module.background = 'FFFF00'
    elif battery_percentage >= 10:
        module.background = 'FF0000'
    elif charge_status == ChargeStatus.DISCHARGING:
        Blink(module)

    module.full_text = str(battery_percentage) + '%'
