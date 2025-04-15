import sys
sys.path.insert(1, '../pybox')
import pybox
import time

controller = pybox.UltimateC()

while True:
    print(controller.get_r_trigger())
    time.sleep(0.25)
    # pass
    