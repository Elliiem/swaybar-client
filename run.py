import time
import os

import pathlib

import main

config_base_dir = pathlib.Path(os.environ.get('XDG_CONFIG_HOME', '~/.config'))
config_file_path = config_base_dir.joinpath('sway', 'swaybar-client.json').expanduser()

config = main.Config.LoadFromPath(config_file_path)

instances = main.LoadModules(config)

main.Init(instances, config)

while True:
    main.Update(instances)
    time.sleep(0.25)