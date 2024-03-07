import main

def Init(module: main.Module):
    pass


def Update(module: main.Module):
    with open('/sys/class/power_supply/BAT0/status') as file:
        status = file.read().strip('\n')

        if status == 'Charging':
            status_indicator = '▲ '
        elif status == 'Discharging':
            status_indicator = '▼ '
        else:
            status_indicator = '- '


    with open('/sys/class/power_supply/BAT0/capacity') as file:
        battery_percentage_str = file.read().strip('\n')

    battery_percentage = int(battery_percentage_str)

    if battery_percentage < 10:
        module.settings.urgent = True

    module.full_text = status_indicator + battery_percentage_str + '%'
