import json
import sys
import os

from typing import List, Callable, Dict

import importlib.util

class HeaderConfig:
    def __init__(self, version: str,
                click_events: bool,
                cont_signal: int,
                stop_signal: int) -> None:

        self.version = version
        self.click_events = click_events
        self.cont_signal = cont_signal
        self.stop_signal = stop_signal

    def LoadFromDict(config: Dict[str, any]) -> 'HeaderConfig':
        return HeaderConfig(
            version = config['version'] if 'version' in config else 1,
            click_events = config['click_events'] if 'click_events' in config else False,
            cont_signal = config['cont_signal'] if 'cont_signal' in config else 18,
            stop_signal = config['stop_signal'] if 'stop_signal' in config else 19,
        )

    def LoadFromPath(path: str) -> 'HeaderConfig':
        with open(path) as config_file:
            config = json.load(config_file)

        return HeaderConfig.LoadFromDict(config)

class Config:
    def __init__(self, module_dir: str, header_config: HeaderConfig) -> None:
        self.module_dir = module_dir
        self.header_config = header_config


    def LoadFromDict(config: Dict[str, any]) -> 'Config':
        module_dir = config['modules_dir'] if 'modules_dir' in config else os.path.dirname(__file__) + '/Modules'

        if not os.path.exists(module_dir):
            raise Exception("No module directory was found!")

        return Config(
            module_dir = module_dir,
            header_config = HeaderConfig.LoadFromDict(config)
        )

    def LoadFromPath(path:str) -> 'Config':
        with open(path) as config_file:
            config = json.load(config_file)

        return Config.LoadFromDict(config)


class ModulesConfig:
    def __init__(self, modules: Dict[str, any]) -> None:
        self.modules = modules

    def LoadFromDict(config: Dict[str, any]) -> 'ModulesConfig':
        return ModulesConfig(
            modules = config['modules'] if 'modules' in config else []
        )

    def LoadFromPath(path: str) -> 'ModulesConfig':
        with open(path) as config_file:
            config = json.load(config_file)

        return ModulesConfig.LoadFromDict(config)


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
                markup: str = 'none') -> None:

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


def LoadModule(path: str, instance: int) -> any:
    spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


    return Module(module.__name__, instance, module.Update, module.Init)


def LoadModules(path: str):
    config: ModulesConfig = ModulesConfig.LoadFromPath(path + '/config.json')

    instance_count = {}

    modules = []

    for module_rel_path in config.modules:
        if module_rel_path in instance_count:
            instance_count[module_rel_path] += 1
        else:
            instance_count[module_rel_path] = 0

        modules.append(LoadModule(path + module_rel_path + '.py', instance_count[module_rel_path]))

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


def GenerateHeaderDict(settings: HeaderConfig):
    return {
        'version': settings.version,
        'click_events': settings.click_events,
        'cont_signal': settings.cont_signal,
        'stop_signal': settings.stop_signal
    }


def GenerateLine(instances: List[Module]) -> str:
    out = []

    for instance in instances:
        out.append(GenerateModuleDict(instance))

    return json.dumps(out)

def Init(instances: List[Module], config: Config):
    for instance in instances:
        instance.init(instance)

    print(json.dumps(GenerateHeaderDict(config.header_config)))
    print('[' + GenerateLine(instances))
    sys.stdout.flush()


def Update(instances: List[Module]):
    for instance in instances:
        instance.update(instance)

    print(',' + GenerateLine(instances))
    sys.stdout.flush()