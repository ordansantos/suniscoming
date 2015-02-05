
import pygame

screen = pygame.display.set_mode((300, 300));
print pygame.version.ver

global running
running = True

def eventos():
    global running
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    print event

while running:
    eventos();
