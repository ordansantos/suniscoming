
import Person
import Queue
import pygame
import threading
import PathFind
import math

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
        self.path = Queue.Queue()
        self.clock = pygame.time.Clock()
        self.millis = 0

        while True:
        
            self.millis = self.clock.tick(30)
            
            if (not self.path.empty()):
                self.moveBot()
            else:
                self.p.stopped()
                x, y = self.p.getPosition()
                self.path = PathFind.PathFind.getPath ((x, y), Person.Person.getMaster().getPosition())
                self.path.get()
                
                
    def moveBot(self):
        x, y = self.p.getPosition()
        x1, y1 = self.path.get()
        
        if ( math.fabs(x - x1) <= 1 and math.fabs(y - y1) <= 1): return

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
        
        
        
        
        