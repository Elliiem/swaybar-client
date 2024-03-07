import main
import time

def Init(module: main.Module):
    pass

def Update(module: main.Module):
    module.full_text = time.asctime()