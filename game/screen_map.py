import pygame, sys
from game import button, states, constants, utils

def map_loader(screen):
    pygame.display.set_caption("Map")  

    while True:
        pygame.display.flip()
