import config
import json

from typing import List, Callable

import sys
sys.path.append(config.ELEMENT_SCRIPT_PATH)

class ModuleSettings:
    def __init__(self, color: str = "",
                background: str = "",
                border: str = "",
                border_top: int = 0,
                border_bottom: int = 0,
                border_left: int = 0,
                border_right: int = 0,
                min_width: int = 0,
                align: str = "left",
                urgent: bool = False,
                separator: bool = True,
                seperator_block_width: int = 10,
                markup: str = "none") -> None:

        self.color = color
        self.background = background
        self.border = border
        self.border_top = border_top
        self.border_bottom = border_bottom
        self.border_left = border_left
        self.border_right = border_right
        self.min_width = min_width
        self.align = align
        self.urgent = urgent
        self.separator = separator
        self.seperator_block_width = seperator_block_width
        self.markup = markup


class Module:
    def __init__(self, name: str, instance: int, update: Callable[['Module'], None], init: Callable[['Module'], None], settings: ModuleSettings) -> None:
        self.name = name
        self.instance = instance

        self.full_text = ""
        self.short_text = ""

        self.settings = settings

        self.update = update
        self.init = init


def GenerateModuleDict(module: Module):
    return {
        'name': module.name,
        'instance': str(module.instance),
        'full_text': module.full_text,
        'short_text': module.short_text,
        'color': module.settings.color,
        'background': module.settings.background,
        'border': module.settings.border,
        'border_top': module.settings.border_top,
        'border_bottom': module.settings.border_bottom,
        'border_left': module.settings.border_left,
        'border_right': module.settings.border_right,
        'border_left': module.settings.border_left,
        'min_width': module.settings.min_width,
        'align': module.settings.align,
        'urgent': module.settings.urgent,
        'separator': module.settings.separator,
        'separator_block_width': module.settings.seperator_block_width,
        'markup': module.settings.markup
    }


def GenerateHeaderDict(version: int, click_events: bool = False, cont_signal: int = 18, stop_signal: int = 19):
    return {
        'version': version,
        'click_events': click_events,
        'cont_signal': cont_signal,
        'stop_signal': stop_signal
    }


def GenerateLine(instances: List[Module]) -> str:
    out = "["

    for instance in instances:
        out += json.dumps(GenerateModuleDict(instance)) + ','
    out = out.strip(',')

    out += "]"

    return out

def Init(instances: List[Module]):
    for instance in instances:
        instance.init(instance)

    print(json.dumps(GenerateHeaderDict(config.VERSION, config.CLICK_EVENTS, config.SIGCONT, config.SIGSTOP)))
    print('[' + GenerateLine(instances))
    sys.stdout.flush()


def Update(instances: List[Module]):
    for instance in instances:
        instance.update(instance)

    print(', ' + GenerateLine(instances))
    sys.stdout.flush()