# coding: utf-8
import pygame

class Screen(pygame.sprite.Sprite):
    
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 480
        self.TILE = 5
        self.primary_surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    
    def surface_fill(self):
        # temporary
        fill = pygame.image.load(file("img/tile.png"))
        
        for i in range(self.WIDTH / self.TILE):
            for j in range(self.HEIGHT / self.TILE):
                self.primary_surface.blit(fill, (i * self.TILE, j * self.TILE))
    
    # attempt...
    def surface_character(self, character):
        self.primary_surface.blit(character.image, (character.position[0] * character.size[0], character.position[1] * character.size[1]))
    
    def draw(self):
        pygame.display.flip()