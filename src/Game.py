

import pygame
import Screen
import Character
import Walls


class Game:
    
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(self.width, self.height)     
        # self.p = Character.Character()
        self.p = Character.Character()
        
        self.p.setPosition((108 , 196))
        
        walls = Walls.Walls()
        self.millis = 0
        
    def setScreenWidth(self, width):
        self.width = width
        
    def setScreenHeight(self, height):
        self.height = height
        
    def run(self):
        self.running = True
        
        while self.running:
            self.millis = self.clock.tick(30)
            self.p.move()
            self.screen.clear(self.p.getPosition())
            self.screen.blitPerson(self.p, self.millis)
            self.screen.draw(self.p.getPosition())
            self.doEvent()
    
    def doEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False;
            
            if e.type == pygame.KEYUP:
                if e.key in self.p.arrow_states.keys():
                    self.p.setArrow(e.key, False)
            if e.type == pygame.KEYDOWN:
                if e.key in self.p.arrow_states.keys():
                    self.p.setArrow(e.key, True)
                if e.key in self.p.attack_keys.keys():
                    self.p.attack(e.key)
