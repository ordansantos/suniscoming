
import pygame

class Sun:
    
    # 2,5 minutes = 150000
    PERIOD = 1500

    def __init__(self):
        self.color = (240, 240, 240)
        self.time = 0
        self.gray = 240
    
    def getColor(self):
        time = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - self.time) >= Sun.PERIOD:
            self.color = self.nextColor()
            self.time = time
        return self.color
    
    def nextColor(self):
        self.gray -= 16
        if self.gray == -16:
            self.gray = 240
        return (self.gray, self.gray, self.gray)
