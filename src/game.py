# coding: utf-8
import pygame
import myScreen
import player

from pygame.locals import *
from pygame.event import Event

class Game:
    
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = myScreen.Screen()
        self.character = player.Character()
    
    def begin(self):
        while self.running:
            pygame.time.Clock().tick(30)
            self.handle_events()
            self.screen.surface_fill()
            self.screen.surface_character(self.character)
            self.screen.draw()
    
    def handle_events(self):
        e = pygame.event.poll()
        if e.type == QUIT:
            self.running = False
        if e.type == KEYDOWN:
            self.character.move(e.key)
        if e.type == KEYUP:
            self.character.move(e.key)
