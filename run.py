import main
from modules import modules

import time

instance_count = {}
instances = []

for name in modules:
    if name in instance_count:
        instance = instance_count[name]
        instance_count[name] += 1
    else:
        exec(f"import {name}")
        instance = 0
        instance_count[name] = 1

    exec(f"init = {name}.Init")
    exec(f"update = {name}.Update")

    instances.append(main.Module(name, instance, update, init, main.ModuleSettings()))

main.Init(instances)
time.sleep(0.9)

while True:
    main.Update(instances)
    time.sleep(0.9)