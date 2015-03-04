
import sys
sys.path.append("../")

import pygame

class Sound:
    
    def __init__(self, background='../sounds/background.wav', volume=0.3):
        self.background = pygame.mixer.Sound(background)
        self.background.set_volume(volume)
        
    
    # background
    def backgroundPlay(self):
        self.background.play(-1)
    
    def backgroundStop(self):
        self.background.stop()
    
    def backgroundGetVolume(self):
        return self.background.get_volume()
    
    def backgroundSetVolume(self, volume):
        self.background.set_volume(volume)
    
    # attack
    @staticmethod
    def attackPlay(sound = '../sounds/attack.wav', volume = 0.5):
        attack = pygame.mixer.Sound(sound)
        attack.set_volume(volume)
        attack.play()
    
    # death
    @staticmethod
    def deathPlay(sound = '../sounds/died.wav', volume = 1.0):
        death = pygame.mixer.Sound(sound)
        death.set_volume(volume)
        death.play()
    
    # all
    def stopAll(self):
        self.backgroundStop()
    