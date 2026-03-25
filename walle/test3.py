import math
import pybox.pybox
import time
import RPi._GPIO as GPIO
import pygame
from adafruit_servokit import ServoKit


controller = pybox.UltimateC()

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

rightArmRotate_channel = 3
rightArmRotate_limits = [76, 150]
rightArmRotateState = 0

leftArmVertical_channel = 4
leftArmVertical_limits = [35, 144]

rightArmVertical_channel = 5
rightArmVertical_limits = [35, 144]

# 6 NA
# 7 NA

rightThumb_channel = 8
leftThumb_channel = 9
thumbLimits = [108, 170]
leftThumbState = 0
rightThumbState = 0

leftArmRotate_channel = 10
leftArmRotate_limits = [66, 155]
leftArmRotateState = 0


ch2 = 2
ch2limits = [5, 175]

ch12 = 12
ch12limits = [5, 175]

ch11 = 11
ch11limits = [140, 175]


audioA = pygame.mixer.Sound("/home/pi/walle/audio/eve.mp3")
audioX = pygame.mixer.Sound("/home/pi/walle/audio/Wa...Wall-e.mp3")
audioY = pygame.mixer.Sound("/home/pi/walle/audio/Aaaaah !.mp3")
audioB = pygame.mixer.Sound("/home/pi/walle/audio/Ohooo !.mp3")


kit.continuous_servo[0].throttle = 0
kit.continuous_servo[1].throttle = 0


servo_defaults = [0, 0, 108, 108, 100, 108, 108, 108, 108, 108, 108, 108, 175, 108]

for i in range(2, len(servo_defaults)):
    kit.servo[i].angle = servo_defaults[i]


try:
    while True:

        if abs(controller.get_l_joy_x()) > 0.1 or abs(controller.get_l_joy_y() > 0.1):
            joystick_x = controller.get_l_joy_x()
            joystick_y = controller.get_l_joy_y()

            motorA_speed = 100 * joystick_y + 100 * joystick_x
            motorB_speed = 100 * joystick_y - 100 * joystick_x
            motorA_speed = max(-100, min(100, motorA_speed)) / -150
            motorB_speed = max(-100, min(100, motorB_speed)) / -150
            kit.continuous_servo[motorA_channel].throttle = -motorA_speed
            kit.continuous_servo[motorB_channel].throttle = motorB_speed
            # print(motorA_speed)
            # print(motorB_speed)
        else:
            kit.continuous_servo[motorA_channel].throttle = 0.1
            kit.continuous_servo[motorB_channel].throttle = 0.1

        if controller.get_d_pad_x():
            kit.servo[2].angle = 0
        else:
            kit.servo[2].angle = 180


except KeyboardInterrupt:
    init = True
    controller.stop()
    GPIO.cleanup()
