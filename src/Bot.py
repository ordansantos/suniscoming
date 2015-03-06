
import Person
from collections import deque
import pygame
import threading
import PathFind
import pygtk, gtk, gobject

class Bot:
    
    @staticmethod
    def putNewBot ( (x, y), image = '../characters/kauan.png' ):
        
        person = Person.Person.getNewPerson(x, y, image)
        
        person_bot = BotThread(kwargs={'person': person})
        person_bot.setDaemon(True)
        person_bot.start()
        
class BotThread(threading.Thread):
    
    def run(self):

        self.p = self._Thread__kwargs['person']
        self.path_deque = deque()
        self.clock = pygame.time.Clock()
        
        while True:
            
            self.clock.tick(30)
            
            if (len(self.path_deque)):
                self.moveBot()
                if (self.path_deque == 0):
                    self.p.stopped()
            else:
                x1, y1 = Person.Person.getMaster().getPosition()
                x0, y0 = self.p.getPosition()

                dist = PathFind.PathFind.euclidianDistance( (x0, y0), (x1, y1) )
                
                if (dist <= 100 and dist > 4):
                    self.path_deque = PathFind.PathFind.getPath ((x0, y0), (x1, y1))
                else:
                    
                    self.p.attack(pygame.K_SPACE)
                    
            if self.p.life == 0:
                break
            
    def moveBot(self):
        x, y = self.p.getPosition()
        x1, y1 = self.path_deque.popleft()

        if (x1 > x):
            if (y1 > y):
                self.p.downRight()
            elif (y1 < y):
                self.p.upRight()
            else:
                self.p.right()

        elif (x1 < x):
            if (y1 > y):
                self.p.downLeft()
            elif (y1 < y):
                self.p.upLeft()
            else:
                self.p.left()

        else:
            if (y1 > y):
                self.p.down()
            elif (y1 < y):
                self.p.up()



