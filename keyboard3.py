import pygame
from pygame.locals import *
pygame.init()
done = False    
pos = Rect(0,0,10,10)

while not done:
    for event in pygame.event.get():
        # any other key event input
        if event.type == QUIT:
            done = True        
        elif event.type == KEYDOWN:
            if event.key == K_ESC:
                done = True

    # get key current state
    keys = pygame.key.get_pressed()
    if keys[K_SPACE]: 
        print 'firing gun'
