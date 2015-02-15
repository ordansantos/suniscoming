

import pygame
import Screen
import Person
import Walls


class Game:
    
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.p = Person.Person()
        
        self.p.setPosition((self.width / 2 , self.height / 2))
        
        self.key_states= {pygame.K_UP:False, pygame.K_DOWN:False, pygame.K_LEFT:False, pygame.K_RIGHT:False}
        
        
        walls = Walls.Walls()
        
    def setScreenWidth(self, width):
        self.width = width
        
    def setScreenHeight(self, height):
        self.height = height
        
    def run(self):
        self.screen = Screen.Screen(self.width, self.height)
        self.running = True
        
        while self.running:
            self.doEvent()
            self.screen.blitPerson(self.p)
            self.clock.tick(60)
            
    def doEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False;
                
            if e.type == pygame.KEYUP:
                self.key_states[e.key] = False
                    
            if e.type == pygame.KEYDOWN:
                self.key_states[e.key] = True
                
        if self.key_states[pygame.K_UP]:
            self.p.moveUp()
        if self.key_states[pygame.K_DOWN]:
            self.p.moveDown()
        if self.key_states[pygame.K_LEFT]:
            self.p.moveLeft()
        if self.key_states[pygame.K_RIGHT]:
            self.p.moveRight()
                
                
    
            
            