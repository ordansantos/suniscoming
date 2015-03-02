
import pygame
import Screen
import Person
import Sun
import Bot
import TextBox
import ClientSocket

class Game:
    
    def __init__(self):
        
        pygame.init()
        
        self.width = 800
        self.height =  600

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(self.width, self.height)
        self.txt = self.screen.txt
        
        self.arrow_states = {
            pygame.K_UP: [False, -1],
            pygame.K_DOWN: [False, 1],
            pygame.K_LEFT: [False, -1],
            pygame.K_RIGHT: [False, 1],
        }
        
        self.arrow = [0, 0]
        
        self.sun = Sun.Sun()
        
        self.p = Person.Person.getNewPerson(457, 1457, '../characters/ordan.png')
        self.p.px= 1
        Person.Person.setMaster(self.p.getId())
        
        #Bot.Bot.putNewBot((1700, 1700), '../characters/skeleton.png')
        #Bot.Bot.putNewBot((160, 300))
        #Bot.Bot.putNewBot((130, 400))
        """Bot.Bot.putNewBot((120, 350))
        Bot.Bot.putNewBot((200, 300))
        Bot.Bot.putNewBot((100, 340))
        Bot.Bot.putNewBot((250, 251))
        Bot.Bot.putNewBot((130, 501))
        Bot.Bot.putNewBot((166, 300))
        Bot.Bot.putNewBot((131, 400))
        Bot.Bot.putNewBot((122, 350))
        Bot.Bot.putNewBot((203, 300))
        Bot.Bot.putNewBot((104, 340))
        Bot.Bot.putNewBot((255, 251))
        Bot.Bot.putNewBot((138, 501))
        Bot.Bot.putNewBot((169, 308))
        Bot.Bot.putNewBot((139, 408))
        Bot.Bot.putNewBot((129, 358))
        Bot.Bot.putNewBot((209, 308))
        Bot.Bot.putNewBot((109, 348))
        Bot.Bot.putNewBot((259, 258))
        Bot.Bot.putNewBot((139, 508))"""
        #Bot.Bot.putNewBot((600, 800))
        #Bot.Bot.putNewBot((1000, 2000))
        
        """ self.client = ClientSocket.ClientSocket() """
    
    def setScreenWidth(self, width):
        self.width = width
    
    def setScreenHeight(self, height):
        self.height = height
    
    def run(self):
        self.running = True
        
        while self.running:
            self.clock.tick(30)
            pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
            self.screen.draw(self.p, self.sun)
            self.doEvent()
            self.p.move(self.arrow)
            
            '''client_event = self.client.get()
            
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

            for e in client_event['moves']:
                if e == 'up':
                    self.p.up()
                if e == 'down':
                    self.p.down()
                if e == 'left':
                    self.p.left()
                if e == 'right':
                    self.p.right()'''
                
    def doEvent(self):
        
        events = pygame.event.get()
        
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            
            self.clicked(e)
            mouse_pos = pygame.mouse.get_pos()
            
            if self.txt.onTextBox(mouse_pos) or self.txt.writing_now:
                self.txt.handleTextBox(events)
            
            else:
                if e.type == pygame.KEYUP:
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = False
                        self.updateArrows()
                
                if e.type == pygame.KEYDOWN:
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = True
                        self.updateArrows()
                    if e.key in self.p.attack_keys.keys():
                        self.p.attack(e.key)
                    if e.key == pygame.K_f:
                        self.p.updateFurtiveness()
    
    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.txt.updateWriting()
        return True
    
    def updateArrows(self):
        self.arrow = [0, 0]
        if self.arrow_states[pygame.K_UP][0]:
            self.arrow[1] += self.arrow_states[pygame.K_UP][1]
        if self.arrow_states[pygame.K_DOWN][0]:
            self.arrow[1] += self.arrow_states[pygame.K_DOWN][1]
        if self.arrow_states[pygame.K_LEFT][0]:
            self.arrow[0] += self.arrow_states[pygame.K_LEFT][1]
        if self.arrow_states[pygame.K_RIGHT][0]:
            self.arrow[0] += self.arrow_states[pygame.K_RIGHT][1]
    
