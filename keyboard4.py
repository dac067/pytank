import pygame
import sys
pygame.init()

from pygame import *
import os
os.putenv('SDL_VIDEODRIVER', 'fbcon')

self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print('Forward')
            elif event.key == pygame.K_s:
                print('Backward')
