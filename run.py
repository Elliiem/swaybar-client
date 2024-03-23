import main

import time
import os

config = main.Config.LoadFromPath(os.path.dirname(__file__) + '/config.json')

instances = main.LoadModules(config.module_dir)

main.Init(instances, config)

while True:
    main.Update(instances)
    time.sleep(60)
