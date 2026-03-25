import pygame
import time

pygame.mixer.init()

audioA = pygame.mixer.Sound("/home/pi/walle/audio/Hello.mp3")

audioA.set_volume(1)

for i in range(0, 100):
    audioA.play()
    time.sleep(3)
