
import pygame
import Screen
import Person
import Sun
import Bot
import ClientSocket

class Game:
    
    def __init__(self):
        
        pygame.init()
        
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(self.width, self.height)     
        
        self.sun = Sun.Sun()
        
        self.p = Person.Person.getNewPerson(100, 250, '../characters/ordan.png')
        self.p.px= 1
        Person.Person.setMaster(self.p.getId())
        
        Bot.Bot.putNewBot((1700, 1700), '../characters/skeleton.png')
        #Bot.Bot.putNewBot((160, 300))
        #Bot.Bot.putNewBot((130, 400))
        #Bot.Bot.putNewBot((120, 350))
        #Bot.Bot.putNewBot((200, 300))
        #Bot.Bot.putNewBot((100, 340))
        #Bot.Bot.putNewBot((250, 251))
        #Bot.Bot.putNewBot((130, 501))
        #Bot.Bot.putNewBot((600, 800))
        #Bot.Bot.putNewBot((1000, 2000))
        
        self.client = ClientSocket.ClientSocket()
        
    def setScreenWidth(self, width):
        self.width = width
    
    def setScreenHeight(self, height):
        self.height = height
    
    def run(self):
        self.running = True
  
        while self.running:
            self.clock.tick(30)
            pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
            self.p.move()
            self.screen.draw(self.p, self.sun)
            #self.doEvent()
            
            client_event = self.client.get()
            
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        self.client.sendMovement("left")
                    if e.key == pygame.K_RIGHT:
                        self.client.sendMovement("right")
                    if e.key == pygame.K_DOWN:
                        self.client.sendMovement("down")
                    if e.key == pygame.K_UP:
                        self.client.sendMovement("up")
                if e.type == pygame.KEYUP:
                    self.p.stopped()
            for e in client_event['moves']:
                if e == 'up':
                    self.p.up()
                if e == 'down':
                    self.p.down()
                if e == 'left':
                    self.p.left()
                if e == 'right':
                    self.p.right()
                
    def doEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                pygame.quit()
        """  
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
                    """
                    
