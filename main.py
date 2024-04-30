import pygame
import time
import os

from Controller import *

# Inicializace pygame
pygame.init()

"""
POMOCNÉ PROMĚNNÉ
"""

controller = Controller()

"""
Hra běži
"""
while running:
    clock.tick(FPS)

    if not controller.events(pygame.event.get()):
        running = False

    pygame.display.update()

pygame.quit()