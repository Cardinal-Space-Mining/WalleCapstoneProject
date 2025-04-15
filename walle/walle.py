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






audioA = pygame.mixer.Sound('/home/pi/walle/audio/eve.mp3')
audioX = pygame.mixer.Sound('/home/pi/walle/audio/Wa...Wall-e.mp3')
audioY = pygame.mixer.Sound('/home/pi/walle/audio/Aaaaah !.mp3')
audioB = pygame.mixer.Sound('/home/pi/walle/audio/Ohooo !.mp3')


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
            motorA_speed = max(-100, min(100, motorA_speed))/-150
            motorB_speed = max(-100, min(100, motorB_speed))/-150
            kit.continuous_servo[motorA_channel].throttle = -motorA_speed
            kit.continuous_servo[motorB_channel].throttle = motorB_speed
            # print(motorA_speed)
            # print(motorB_speed)
        else:
            kit.continuous_servo[motorA_channel].throttle = 0.1
            kit.continuous_servo[motorB_channel].throttle = 0.1
        
        
        # D Pad / Arm Functions
        
        if controller.get_d_pad_y() > 0 or controller.get_d_pad_y() < 0:
            kit.servo[leftArmVertical_channel].angle = kit.servo[leftArmVertical_channel].angle + controller.get_d_pad_y()
            kit.servo[rightArmVertical_channel].angle = kit.servo[rightArmVertical_channel].angle + controller.get_d_pad_y()

        print(controller.get_r_joy_x())
        print(controller.get_r_joy_y())

        # Left Thumb
        if (controller.get_l_bumper() == 1 and leftThumbState == 0) or (controller.get_l_bumper() == 0 and leftThumbState == 1):
            if (controller.get_l_bumper() == 0):
                leftThumbState = 0
                kit.servo[leftThumb_channel].angle = thumbLimits[1]
            else:
                leftThumbState = 1
                kit.servo[leftThumb_channel].angle = thumbLimits[0]

        # Right Thumb
        if (controller.get_r_bumper() == 1 and rightThumbState == 0) or (controller.get_r_bumper() == 0 and rightThumbState == 1):
            if (controller.get_r_bumper() == 0):
                rightThumbState = 0
                kit.servo[rightThumb_channel].angle = thumbLimits[0]
            else:
                rightThumbState = 1
                kit.servo[rightThumb_channel].angle = thumbLimits[1]
                
        # Left Arm Rotate
        if (controller.get_r_joy_button() == 1 and leftArmRotateState == 0) or (controller.get_r_joy_button() == 0 and leftArmRotateState == 1):
            if (controller.get_r_joy_button() == 0):
                leftArmRotateState = 0
                kit.servo[leftArmRotate_channel].angle = leftArmRotate_limits[0]
            else:
                leftArmRotateState = 1
                kit.servo[leftArmRotate_channel].angle = leftArmRotate_limits[1]

        # Right Arm Rotate
        if (controller.get_r_joy_button() == 1 and rightArmRotateState == 0) or (controller.get_r_joy_button() == 0 and rightArmRotateState == 1):
            if (controller.get_r_joy_button() == 0):
                rightArmRotateState = 0
                kit.servo[rightArmRotate_channel].angle = rightArmRotate_limits[0]
            else:
                rightArmRotateState = 1
                kit.servo[rightArmRotate_channel].angle = rightArmRotate_limits[1]

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
        
        #Audio
        if controller.get_a_button == 1:
            audioA.play()
        if controller.get_x_button == 1:
            audioX.play()
        if controller.get_y_button == 1:
            audioY.play()
        if controller.get_b_button == 1:
            audioB.play()

        pass
except KeyboardInterrupt:
    init = True
    controller.stop()
    GPIO.cleanup()