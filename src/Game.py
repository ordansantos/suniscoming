
import pygame
import Screen
import Person
import Sun
import Bot
import Sound
import ClientSocket
import PathFind
from collections import deque
import sys

class Game:
    
    def __init__(self, screen, width, height):
        
        pygame.init()
        self.mouse_pos_right_click = None
    
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()
        self.screen = Screen.Screen(screen, self.width, self.height)
        self.txt = self.screen.txt
        
        self.sound = Sound.Sound()
        
        self.arrow_states = {
            pygame.K_UP: [False, -1],
            pygame.K_DOWN: [False, 1],
            pygame.K_LEFT: [False, -1],
            pygame.K_RIGHT: [False, 1],
        }
        
        self.arrow = [0, 0]
        
        self.sun = Sun.Sun()
        
        self.p = Person.Person.getNewPlayer(150, 350, '../characters/sprites/ordan.png')
        
        Person.Person.setMaster(self.p.getId())
        self.path_deque = deque()
        
        # Bot.BotController.putNewBot((1700, 1700), '../characters/skeleton.png')
        Bot.BotController.putNewBot((160, 320))
        Bot.BotController.putNewBot((165, 350))
        Bot.BotController.putNewBot((170, 370))
        """Bot.BotController.putNewBot((200, 300))
        Bot.BotController.putNewBot((100, 340))
        Bot.BotController.putNewBot((250, 251))
        Bot.BotController.putNewBot((130, 501))
        Bot.BotController.putNewBot((166, 300))
        Bot.BotController.putNewBot((131, 400))
        Bot.BotController.putNewBot((122, 350))
        Bot.BotController.putNewBot((203, 300))
        Bot.BotController.putNewBot((104, 340))
        Bot.BotController.putNewBot((255, 251))
        Bot.BotController.putNewBot((138, 501))
        Bot.BotController.putNewBot((169, 308))
        Bot.BotController.putNewBot((139, 408))
        Bot.BotController.putNewBot((129, 358))
        Bot.BotController.putNewBot((209, 308))
        Bot.BotController.putNewBot((109, 348))
        Bot.BotController.putNewBot((259, 258))
        Bot.BotController.putNewBot((139, 508))"""
    
        # Bot.BotController.putNewBot((600, 800))
        # Bot.BotController.putNewBot((1000, 2000))
        
        """ self.client = ClientSocket.ClientSocket() """
    
    def setScreenWidth(self, width):
        self.width = width
    
    def setScreenHeight(self, height):
        self.height = height
    
    def run(self):
        self.sound.backgroundPlay()
        self.running = True
        died = False
        while self.running:
            self.clock.tick(30)
            if self.p.life != 0:
                
                # update title
                pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
                
                # draw screen and event handle
                self.screen.draw(self.p, self.sun)
                self.doEvent()
                
                # update player
                self.p.updateDeath(self.sun.getPeriod())
                transform = self.p.updateTransform()
                
                # update sound
                self.sound.updateBackground(transform)

                # move player
                if (len(self.path_deque)):
                    x1, y1 = self.path_deque.popleft()
                    self.p.doAMovement((x1, y1))
                else:
                    self.p.move(self.arrow)
                
            else: # if player died...
                if died == False:
                    self.txt.updateReaderMessage(self.p.name + ' died!')
                    died = True
                if self.p.death != -1:
                    self.screen.draw(self.p, self.sun)
                else:
                    self.sound.stopAll()
                    self.running = False
                    pygame.quit()
                    sys.exit()

            
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
        
        # close window
        if pygame.event.peek(pygame.QUIT):
            self.running = False
            pygame.quit()
            return
        
        events = pygame.event.get()
        a = len(events)
        for e in events:
            # check click and get mouse position
            self.clicked(e)
            mouse_pos = pygame.mouse.get_pos()

            if (pygame.mouse.get_pressed()[2]):
                self.mouse_pos_right_click = mouse_pos

            if (not pygame.mouse.get_pressed()[2] and self.mouse_pos_right_click != None):
                self.updateMovementPath(self.mouse_pos_right_click)
                self.mouse_pos_right_click = None
            # handle writer box
            if self.txt.writing_now and self.arrow == [0, 0]:
                self.txt.handleWriterBox(events)
            
            else:
                
                # handle reader box
                self.txt.handleReaderBox(e)
                
                # handle character movement
                if e.type == pygame.KEYUP:
                    
                    if (len(self.path_deque)):
                        self.p.stopped
                        self.path_deque.clear()
                        
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = False
                        self.updateArrows()
                    
                    if e.key == pygame.K_LSHIFT:
                        self.p.updateSpeed(False)
                
                elif e.type == pygame.KEYDOWN:
                    
                    if (len(self.path_deque)):
                        self.p.stopped
                        self.path_deque.clear()
                        
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = True
                        self.updateArrows()
                    
                    if e.key in self.p.attack_keys.keys():
                        self.p.attack(e.key)
                    
                    if e.key == pygame.K_LSHIFT:
                        self.p.updateSpeed(True)
                
                """
                # resize screen: very very slow :(
                elif e.type == pygame.VIDEORESIZE:
                    self.width, self.height = e.dict['size']
                    self.screen = Screen.Screen(self.width, self.height)
                    self.txt = self.screen.txt """
      
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
    
    def updateMovementPath(self, mouse_pos):
        x, y = self.screen.getMousePositionOnMap(self.p, mouse_pos)
        self.path_deque = PathFind.PathFind.getPath (self.p.getPosition(), (x, y), True)
        
