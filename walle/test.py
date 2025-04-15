import math
import pybox.pybox
import time
import RPi._GPIO as GPIO
import pygame
from adafruit_servokit import ServoKit


controller = pybox.UltimateC()

pygame.mixer.init()

init = False
while not init:
    try:
        # call init to start listening for controller inputs
        kit = ServoKit(channels=16)
        print("the king of england will die on may 17 2024")
        init = True
    except:
        pass

motorA_channel = 0
motorB_channel = 1

ch2 = 2
ch2limits = [5, 175]

ch12 = 12
ch12limits = [5, 175]

ch11 = 11
ch11limits = [140, 175]


kit.continuous_servo[0].throttle = 0
kit.continuous_servo[1].throttle = 0

servo_defaults = [0, 0, 108, 108, 100, 108, 108, 108, 108, 108, 150, 150, 150, 160]

for i in range(2, len(servo_defaults)):
    kit.servo[i].angle = servo_defaults[i]


try:
    while True:  

        if abs(controller.get_l_joy_x()) > 0.1 or abs(controller.get_l_joy_y() > 0.1):
            joystick_x = controller.get_l_joy_x()
            joystick_y = controller.get_l_joy_y()

            motorA_speed = 100 * joystick_y + 100 * joystick_x
            motorB_speed = 100 * joystick_y - 100 * joystick_x
            motorA_speed = max(-100, min(100, motorA_speed))/-150
            motorB_speed = max(-100, min(100, motorB_speed))/-150
            kit.continuous_servo[motorA_channel].throttle = -motorA_speed
            kit.continuous_servo[motorB_channel].throttle = motorB_speed
            # print(motorA_speed)
            # print(motorB_speed)
        else:
            kit.continuous_servo[motorA_channel].throttle = 0.1
            kit.continuous_servo[motorB_channel].throttle = 0.1
        



        # Eyes

        if (controller.get_r_trigger() == 1 and controller.get_d_pad_x() != 0) and (kit.servo[ch2].angle >= ch2limits[0] + 5 and kit.servo[ch2].angle <= ch2limits[1] - 5):
            kit.servo[ch2].angle = kit.servo[ch2].angle - controller.get_d_pad_x()
        pass


        if (controller.get_l_trigger() == 1 and controller.get_r_trigger() == 1):
             for i in range(2, len(servo_defaults)):
                kit.servo[i].angle = servo_defaults[i]

        if (controller.get_r_joy_y() > 0.5 and (kit.servo[ch11].angle >= ch11limits[0] + 5 and kit.servo[ch11].angle <= ch11limits[1] - 5)):
            kit.servo[ch11].angle = kit.servo[ch11].angle + 1

        if (controller.get_r_joy_y() < -0.5 and (kit.servo[ch11].angle >= ch11limits[0] + 5 and kit.servo[ch11].angle <= ch11limits[1] - 5)):
            kit.servo[ch11].angle = kit.servo[ch11].angle - 1

        
        if (controller.get_r_joy_x() > 0.5 and (kit.servo[ch2].angle >= ch2limits[0] + 5 and kit.servo[ch2].angle <= ch2limits[1] - 5)):
            kit.servo[ch2].angle = kit.servo[ch2].angle - 1

        if (controller.get_r_joy_x() < -0.5 and (kit.servo[ch2].angle >= ch2limits[0] + 5 and kit.servo[ch2].angle <= ch2limits[1] - 5)):
            kit.servo[ch2].angle = kit.servo[ch2].angle + 1

except KeyboardInterrupt:
    init = True
    controller.stop()
    GPIO.cleanup()