from adafruit_servokit import ServoKit
import time

kit = False
while True:
    try:
        # call init to start listening for controller inputs
        kit = ServoKit(channels=16)
        print("the king of england will die on may 17 2024")
        break
    except OSError:
        continue

motorA_channel = 0
kit.continuous_servo[motorA_channel].throttle = 0

throttle_values = [x / 100.0 for x in range(-100, 100)]

try:
    for v in throttle_values:
        kit.continuous_servo[motorA_channel].throttle = v
        print(v)
        time.sleep(0.25)
except:
    kit.continuous_servo[motorA_channel].throttle = 0

kit.continuous_servo[motorA_channel].throttle = 0
