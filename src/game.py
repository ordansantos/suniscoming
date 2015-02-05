
import pygame

class Game:
    
    running = True
    
    def begin(self):
        
        pygame.init()
        pygame.display.set_mode((640, 640))
        
        while self.running:
            self.eventos();
        
    def eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.running = False