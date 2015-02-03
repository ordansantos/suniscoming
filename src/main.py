
import pygame

screen = pygame.display.set_mode((300, 300));
print pygame.version.ver

running = 1 
def eventos():
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    print event

while running:
    eventos();
