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


class Module(main.Module):
    def Init(self):
        self.color = '000000'

        self.background = '00FF00'
        self.border = '00FF00'

        self.border_left = 1
        self.border_right = 1

        self.separator = False
        self.sep_block_width = 0

        self.blink_state = False

    def Update(self):
        charge_status = ChargeStatus.GetChargeStatus()

        status_indicator = ''
        match charge_status:
            case ChargeStatus.CHARGING:
                status_indicator = '▲'
            case ChargeStatus.DISCHARGING:
                status_indicator = '▼'
            case ChargeStatus.NOT_CHARGING:
                status_indicator = '-'

        battery_percentage = round(psutil.sensors_battery().percent)

        if battery_percentage >= 60:
            self.background = '00FF00'
            self.border = '00FF00'
        elif battery_percentage >= 20:
            self.background = 'FFFF00'
            self.border = 'FFFF00'
        elif battery_percentage >= 10:
            self.background = 'FF0000'
            self.border = 'FF0000'
        elif charge_status == ChargeStatus.DISCHARGING:
            self.Blink()
        else:
            self.background = 'FF0000'
            self.border = 'FF0000'

        self.full_text = f'{status_indicator} {str(battery_percentage)}%'

    def Blink(self):
        if blink_state:
            blink_state = False
            self.background = 'FF0000'
            self.border = 'FF0000'
        else:
            blink_state = True
            self.background = 'FFFFFF'
            self.border = 'FF0000'