
import pygame

from pygame.locals import *

class Character:
    
    def __init__(self):
        self.nome = 'example'
        self.position = [0, 0]
        self.speed = 1
        
        self.MOVES = {
            K_RIGHT: ( 1, 0),
            K_LEFT : (-1, 0),
            K_UP   : ( 0,-1),
            K_DOWN : ( 0, 1),
            K_d    : ( 1, 0),
            K_a    : (-1, 0),
            K_w    : ( 0,-1),
            K_s    : ( 0, 1)
        }
        
        # temporary
        self.image = pygame.image.load(file("img/character.png"))
        self.size = (self.image.get_width(), self.image.get_height())
    
    def move(self, key):
        if key in self.MOVES.keys():
            self.position[0] += self.MOVES[key][0] * self.speed
            self.position[1] += self.MOVES[key][1] * self.speed
