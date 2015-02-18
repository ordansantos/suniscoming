
import pygame
import Screen
import Person

class Game:
    
    def __init__(self):
        
        pygame.init()
        
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(self.width, self.height)     
        
        self.p = Person.Person.getNewPerson(100, 250)
        self.p2 = Person.Person.getNewPerson(110, 275, '../characters/kauan.png')

        
        self.millis = 0
    
    def setScreenWidth(self, width):
        self.width = width
    
    def setScreenHeight(self, height):
        self.height = height
    
    def run(self):
        self.running = True
  
        while self.running:
            self.millis = self.clock.tick(30)
            pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d) - Person(%d)' %(self.p.x, self.p.y, self.p.life, self.p2.life))
            
            self.p.move()
        
            self.screen.draw(self.p, self.millis)
        
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
