
import Person
from collections import deque
import pygame
import threading
import PathFind

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
            else:
                x, y = self.p.getPosition()
                self.path_deque = PathFind.PathFind.getPath ((x, y), Person.Person.getMaster().getPosition())
                self.p.stopped()
    
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
