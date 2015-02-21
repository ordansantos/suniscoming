
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
        self.millis = 0
        

        
        while True:
            
            self.millis = self.clock.tick(30)
            
            if (len(self.path_deque)):
                self.moveBot()
            else:
                
                x, y = self.p.getPosition()
                self.path_deque = PathFind.PathFind.getPath ((x, y), Person.Person.getMaster().getPosition())
                
            self.p.stopped()
    def moveBot(self):
        x, y = self.p.getPosition()
        x1, y1 = self.path_deque.popleft()
        print x, y, x1, y1
        if (x1 > x):
            if (y1 > y):
                self.p.downRight()
                print 'entrou 1'
            elif (y1 < y):
                self.p.upRight()
                print 'entrou 2'
                
            else:
                self.p.right()
                print 'entrou 3'

        elif (x1 < x):
            if (y1 > y):
                self.p.downLeft()
                print 'entrou 4'
            elif (y1 < y):
                self.p.upLeft()
                print 'entrou 5'
            else:
                self.p.left()
                print 'entrou 6'

        else:
            if (y1 > y):
                self.p.down()
                print 'entrou 7'
            elif (y1 < y):
                self.p.up()
                print 'entrou 8'

        
        
        