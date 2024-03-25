import json
import sys
import os
import time

from typing import List, Callable, Dict

import importlib.util

class Config:
    def __init__(self, module_dir: str, modules: List[str]) -> None:
        self.module_dir = module_dir
        self.modules = modules


    def LoadFromDict(config: Dict[str, any]) -> 'Config':
        module_dir = ''
        if 'modules_directory' in config:
            module_dir = config['modules_directory']

        if module_dir == '':
            module_dir = os.path.join(os.path.dirname(__file__), 'Modules')

        if not os.path.exists(module_dir):
            raise Exception("No module directory was found!")

        modules = config['modules'] if 'modules' in config else []

        return Config(
            module_dir = module_dir,
            modules = modules
        )

    def LoadFromPath(path:str) -> 'Config':
        with open(path) as config_file:
            config = json.load(config_file)

        return Config.LoadFromDict(config)

class Module:
    def __init__(self,
                name: str,
                instance: int,
                update: Callable[['Module'], None],
                init: Callable[['Module'], None],
                color: str = '',
                background: str = '',
                border: str = '',
                border_top: int = 0,
                border_bottom: int = 0,
                border_left: int = 0,
                border_right: int = 0,
                min_width: int = 0,
                align: str = 'left',
                urgent: bool = False,
                separator: bool = True,
                separator_block_width: int = 10,
                markup: str = 'none',
                timeout = 1.0) -> None:

        self.name = name
        self.instance = instance

        self.full_text = ''
        self.short_text = ''

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
        self.separator_block_width = separator_block_width
        self.markup = markup

        self.update = update
        self.init = init

        self.timeout = timeout

        self._update_time = 0


def LoadModule(path: str, instance: int) -> any:
    if not os.path.exists(path):
        raise Exception(f"Module {os.path.splitext(os.path.basename(path))[0]} does not exist")

    spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return Module(module.__name__, instance, module.Update, module.Init)


def LoadModules(config: Config):
    instance_count = {}
    modules = []

    for rel_path in config.modules:
        if rel_path in instance_count:
            instance_count[rel_path] += 1
        else:
            instance_count[rel_path] = 0

        module_path = config.module_dir + rel_path + '.py'
        modules.append(LoadModule(module_path, instance_count[rel_path]))

    return modules


def GenerateModuleDict(module: Module):
    return {
        'name': module.name,
        'instance': module.instance,
        'full_text': module.full_text,
        'short_text': module.short_text,
        'color': module.color,
        'background': module.background,
        'border': module.border,
        'border_top': module.border_top,
        'border_bottom': module.border_bottom,
        'border_left': module.border_left,
        'border_right': module.border_right,
        'border_left': module.border_left,
        'min_width': module.min_width,
        'align': module.align,
        'urgent': module.urgent,
        'separator': module.separator,
        'separator_block_width': module.separator_block_width,
        'markup': module.markup
    }

#TODO Make configurable / smarter
def GenerateHeaderDict():
    return {
        'version': 1,
        'click_events': False,
        'cont_signal': 18,
        'stop_signal': 19
    }


def GenerateLine(instances: List[Module]) -> str:
    out = []

    for instance in instances:
        out.append(GenerateModuleDict(instance))

    return json.dumps(out)

def Init(instances: List[Module], config: Config):
    for instance in instances:
        instance.init(instance)

    print(json.dumps(GenerateHeaderDict()))
    print('[' + GenerateLine(instances))
    sys.stdout.flush()


def Update(instances: List[Module]):
    for instance in instances:
        now = time.time()

        if now - instance._update_time > instance.timeout:
            instance.update(instance)
            instance._update_time = now

    print(',' + GenerateLine(instances))
    sys.stdout.flush()