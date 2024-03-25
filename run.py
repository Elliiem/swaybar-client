import main

import time
import os

config_base_dir = os.environ.get('XDG_CONFIG_HOME', '~/.config')
config_file_path = os.path.join(config_base_dir, 'sway', 'swaybar-client.json')

config = main.Config.LoadFromPath(os.path.expanduser(config_file_path))

instances = main.LoadModules(config)

main.Init(instances, config)

while True:
    main.Update(instances)
    time.sleep(1)
