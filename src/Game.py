
import pygame
import Screen
import Person
import Sun
import Bot

class Game:
    
    def __init__(self):
        
        pygame.init()
        
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(self.width, self.height)     
        
        self.sun = Sun.Sun()
        
        self.p = Person.Person.getNewPerson(100, 250, '../characters/ordan.png')
        Person.Person.setMaster(self.p.getId())
        
        self.millis = 0
        
        Bot.Bot.putNewBot((140, 250))
        Bot.Bot.putNewBot((160, 251))
        #Bot.Bot.putNewBot((130, 252))
        #Bot.Bot.putNewBot((120, 253))
        #Bot.Bot.putNewBot((110, 254))
        #Bot.Bot.putNewBot((100, 260))
        #Bot.Bot.putNewBot((120, 251))
        #Bot.Bot.putNewBot((130, 242))
        #Bot.Bot.putNewBot((140, 233))
        #Bot.Bot.putNewBot((120, 214))
    def setScreenWidth(self, width):
        self.width = width
    
    def setScreenHeight(self, height):
        self.height = height
    
    def run(self):
        self.running = True
  
        while self.running:
            
            self.millis = self.clock.tick(30)
            pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
            self.p.move()
            self.screen.draw(self.p, self.sun, self.millis)
            self.doEvent()
    
    def doEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            
            if e.type == pygame.KEYUP:
                if e.key in self.p.arrow_states.keys():
                    self.p.setArrow(e.key, False)
            if e.type == pygame.KEYDOWN:
                if e.key in self.p.arrow_states.keys():
                    self.p.setArrow(e.key, True)
                if e.key in self.p.attack_keys.keys():
                    self.p.attack(e.key)
                if e.key == pygame.K_f:
                    self.p.updateFurtiveness()
            

                
