import math
import pybox.pybox
import time
import RPi._GPIO as GPIO
import pygame
from adafruit_servokit import ServoKit
import atexit
import sys
import math


def motor_pwr(ctrler_x: float, ctrler_y: float) -> tuple[float, float]:
    m = math.hypot(ctrler_x, ctrler_y) / math.sqrt(2)
    if m < 0.1:
        return (0.0, 0.0)
    theta = math.atan2(ctrler_x, ctrler_y)
    pi_div_4 = math.pi / 4
    m_a = math.cos(theta - pi_div_4) * m
    m_b = math.cos(theta + pi_div_4) * m
    return m_a, m_b


controller = pybox.UltimateC()

kit = False
while True:
    try:
        # call init to start listening for controller inputs
        kit = ServoKit(channels=16)
        print("the king of england will die on may 17 2024")
        break
    except OSError:
        continue

motorA_channel = 0  # Left Motor
motorB_channel = 1  # Right Motor

# PWM Channels
# See PWM Map2.txt
leftShoulder = 2
leftElbow = 3
leftWrist = 4
leftThumb = 5
leftFinger = 6
rightShoulder = 7
rightElbow = 8
rightWrist = 9
rightThumb = 10
rightFinger = 11
headPan = 12
headTilt = 13
eyeActuation = 14

shoulder_speed = 0.5
elbow_speed = 0.25
wrist_speed = 3
headPan_speed = 1
headTilt_speed = 1

audioA = pygame.mixer.Sound("/home/pi/walle/audio/eve.mp3")
audioX = pygame.mixer.Sound("/home/pi/walle/audio/Wa...Wall-e.mp3")
audioY = pygame.mixer.Sound("/home/pi/walle/audio/Aaaaah !.mp3")
audioB = pygame.mixer.Sound("/home/pi/walle/audio/Ohooo !.mp3")

kit.continuous_servo[0].throttle = 0
kit.continuous_servo[1].throttle = 0


def reset_motors():
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0


atexit.register(reset_motors)


# Default positions
#              0    1    2    3    4    5    6    7    8    9   10   11   12   13   14
servo_pos = [0, 0, 90, 90, 60, 93, 94, 90, 90, 120, 98, 99, 90, 90, 102]
mins = [0, 0, 45, 80, 0, 50, 75, 0, 65, 0, 50, 75, 0, 140, 0]  # Down to 0
maxs = [
    180,
    180,
    130,
    115,
    180,
    130,
    170,
    180,
    100,
    180,
    120,
    170,
    180,
    175,
    180,
]  # Up to 180

for i in range(2, len(servo_pos)):
    kit.servo[i].angle = servo_pos[i]


try:
    not_a = True
    not_b = True
    not_x = True
    not_y = True

    while True:
        # Motor Controls
        # motor_a, motor_b = motor_pwr(controller.get_l_joy_x(), controller.get_l_joy_y())
        motor_a = controller.get_l_joy_y()
        motor_b = controller.get_r_joy_y()
        kit.continuous_servo[motorA_channel].throttle = motor_a
        kit.continuous_servo[motorB_channel].throttle = -motor_b

        # Shoulders
        if controller.get_l_bumper() == 1:
            joystick_y = controller.get_r_joy_y()
            servo_pos[leftShoulder] = (
                servo_pos[leftShoulder] - shoulder_speed * joystick_y
            )
            servo_pos[rightShoulder] = (
                servo_pos[rightShoulder] + shoulder_speed * joystick_y
            )

        # Elbows
        if controller.get_l_bumper() == 1:
            joystick_x = controller.get_r_joy_x()
            servo_pos[leftElbow] = servo_pos[leftElbow] - elbow_speed * joystick_x
            servo_pos[rightElbow] = servo_pos[rightElbow] - elbow_speed * joystick_x

        # Wrists
        if controller.get_start() == 1:
            servo_pos[leftWrist] = servo_pos[leftWrist] + wrist_speed
            servo_pos[rightWrist] = servo_pos[rightWrist] - wrist_speed
        if controller.get_select() == 1:
            servo_pos[leftWrist] = servo_pos[leftWrist] - wrist_speed
            servo_pos[rightWrist] = servo_pos[rightWrist] + wrist_speed

        # Thumbs and Fingers
        servo_pos[leftThumb] = (
            maxs[leftThumb]
            + (mins[leftThumb] - maxs[leftThumb]) * controller.get_l_trigger()
        )
        servo_pos[leftFinger] = (
            maxs[leftFinger]
            + (mins[leftFinger] - maxs[leftFinger]) * controller.get_l_trigger()
        )

        servo_pos[rightThumb] = (
            maxs[rightThumb]
            + (mins[rightThumb] - maxs[rightThumb]) * controller.get_r_trigger()
        )
        servo_pos[rightFinger] = (
            maxs[rightFinger]
            + (mins[rightFinger] - maxs[rightFinger]) * controller.get_r_trigger()
        )

        # Head Pan and Tilt
        if controller.get_l_bumper() == 0:
            joystick_x = controller.get_r_joy_x()
            servo_pos[headPan] = servo_pos[headPan] - headPan_speed * joystick_x

            joystick_y = controller.get_r_joy_y()
            servo_pos[headTilt] = servo_pos[headTilt] + headTilt_speed * joystick_y

        # Eye Actuation
        if controller.get_r_joy_button() == 0:
            servo_pos[eyeActuation] = mins[eyeActuation]
        else:
            servo_pos[eyeActuation] = maxs[eyeActuation]

        # Ensure all positions are within range
        servo_pos = [max(lo, min(v, hi)) for v, lo, hi in zip(servo_pos, mins, maxs)]
        # print(servo_pos)

        # Apply servo positions
        for i in range(2, len(servo_pos)):
            kit.servo[i].angle = servo_pos[i]

        # Audio A
        if controller.get_a_button() == 1 and not_a:
            audioA.play()
            print("Audio A")
            not_a = False
        if controller.get_a_button() != 1:
            not_a = True

        # Audio B
        if controller.get_b_button() == 1 and not_b:
            audioB.play()
            print("Audio B")
            not_b = False
        if controller.get_b_button() != 1:
            not_b = True

        # Audio X
        if controller.get_x_button() == 1 and not_x:
            audioX.play()
            print("Audio X")
            not_x = False
        if controller.get_x_button() != 1:
            not_x = True

        # Audio Y
        if controller.get_y_button() == 1 and not_y:
            audioY.play()
            print("Audio Y")
            not_y = False
        if controller.get_y_button() != 1:
            not_y = True


except KeyboardInterrupt:
    controller._stop_flag.set()
    GPIO.cleanup()
