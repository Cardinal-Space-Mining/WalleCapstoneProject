import math
import pybox.pybox
import time
import RPi._GPIO as GPIO
import pygame
from adafruit_servokit import ServoKit

init = False
while not init:
    try:
        # call init to start listening for controller inputs
        kit = ServoKit(channels=16)
        print("the king of england will die on may 17 2024")
        init = True
    except:
        pass

user_input = input("Enter a number: ")

kit.servo[8].angle = user_input
