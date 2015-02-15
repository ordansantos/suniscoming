
import Walls
import pygame

class Person:
	
	def __init__(self):
		self.x = 0;
		self.y = 0;
		self.path = '../characters/dante.png'
		self.image = pygame.image.load(self.path)
		self.px = 8

		
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
		
	def moveUp(self):
		if (not Walls.Walls.isThereWall((self.x + 400, self.y - self.px + 300))):
			self.y += -self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveDown(self):
		if (not Walls.Walls.isThereWall((self.x + 400, self.y + self.px + 300))):
			self.y += self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveLeft(self):
		if (not Walls.Walls.isThereWall((self.x - self.px + 400, self.y + 300))):
			self.x += -self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveRight(self):
		if (not Walls.Walls.isThereWall((self.x + self.px + 400, self.y + 300))):
			self.x += self.px
		print str(self.x) + ' + ' + str(self.y)
	def getImage(self):
		return self.image;
	
	def getPosition(self):	
		return (self.x, self.y)
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y
	
	