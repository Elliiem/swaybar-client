import json
import sys
import os
import time

from typing import List, Callable, Dict

import importlib.util
import pathlib

MODULES_DEFAULT_PATH = pathlib.Path(__file__).parent.joinpath('Modules')

class Config:
    def __init__(self, modules_path: pathlib.Path, modules: List[pathlib.Path]) -> None:
        self.modules_path = modules_path
        self.modules = modules

    def LoadFromDict(config: Dict[str, any]) -> 'Config':
        if 'modules_directory' in config and not config['modules_directory'] == '':
            modules_path = pathlib.Path(config['modules_directory'])
        else:
            modules_path = MODULES_DEFAULT_PATH

        modules = list(map(lambda x: pathlib.Path(x + '.py'), config['modules'] if 'modules' in config else []))

        return Config (
            modules_path = modules_path,
            modules = modules
        )

    def LoadFromPath(path: pathlib.Path) -> 'Config':
        with path.open('r') as config_file:
            config = json.load(config_file)

        return Config.LoadFromDict(config)


class Module:
    def __init__(self,
                name: str,
                instance: int,
                full_text: str = '',
                short_text: str = '',
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
                sep_block_width: int = 10,
                markup: str = 'none',
                timeout = 1.0) -> None:

        self.name     = name
        self.instance = instance

        self.full_text       = full_text
        self.short_text      = short_text
        self.color           = color
        self.background      = background
        self.border          = border
        self.border_top      = border_top
        self.border_bottom   = border_bottom
        self.border_left     = border_left
        self.border_right    = border_right
        self.min_width       = min_width
        self.align           = align
        self.urgent          = urgent
        self.separator       = separator
        self.sep_block_width = sep_block_width
        self.markup          = markup
        self.timeout         = timeout

        self._update_time = 0


def LoadPythonModuleFromPath(path: pathlib.Path) -> any:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def LoadPythonModulesFromPath(path: pathlib.Path) -> Dict[pathlib.Path, any]:
    modules = {}

    module_paths = list(path.glob('**/*.py'))

    for module_path in module_paths:
        modules[module_path.relative_to(path)] = LoadPythonModuleFromPath(module_path)

    return modules


def CreateInstance(module: pathlib.Path, instances: Dict[pathlib.Path, int], python_modules: Dict[pathlib.Path, any]) -> Module:
    if module in python_modules:
        python_module = python_modules[module]
    else:
        raise Exception(f'Module {module} does not exist')

    if module in instances:
        instances[module] += 1
    else:
        instances[module] = 0

    return python_module.Module(python_module.__name__, instances[module])

def LoadModules(config: Config) -> List[Module]:
    python_modules = LoadPythonModulesFromPath(config.modules_path)
    instances = {}
    modules = []

    for module in config.modules:
        modules.append(CreateInstance(module, instances, python_modules))

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
        'separator_block_width': module.sep_block_width,
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
        instance.Init()

    print(json.dumps(GenerateHeaderDict()))
    print('[' + GenerateLine(instances))
    sys.stdout.flush()


def Update(instances: List[Module]):
    for instance in instances:
        now = time.time()

        if now - instance._update_time > instance.timeout:
            instance.Update()
            instance._update_time = now

    print(',' + GenerateLine(instances))
    sys.stdout.flush()
