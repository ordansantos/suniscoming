
import Walls
import pygame

class Human1:
	
	def __init__(self):
		self.x = 0;
		self.y = 0;
		self.path = '../characters/human1.png'
		self.sprites = self.readSprites()
		self.px = 4
		self.interval = 150
		# test
		self.cycletime = 0
		self.picnr = [3, 0]

	def readSprites(self):
		spritesheet = pygame.image.load(file(self.path))
		spritesheet.convert()
		sprites = [[0 for i in range(10)] for i in range(4)]
		
		for s in range(9): # first line contains 9 pictures of skeletons
			sprites[0][s] = (spritesheet.subsurface((16 + (s * 64), 525, 32, 50)))
		for s in range(9): # second line contains 9 pictures of skeletons
			sprites[1][s] = (spritesheet.subsurface((18 + (s * 64), 589, 32, 50)))
		for s in range(9): # 3 line contains 9 pictures of skeletons
			sprites[2][s] = (spritesheet.subsurface((16 + (s * 64), 653, 32, 50)))
		for s in range(9): # second line contains 9 pictures of skeletons
			sprites[3][s] = (spritesheet.subsurface((18 + (s * 64), 717, 32, 50)))
		
		return sprites
		
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
		
	def moveUp(self):
		if (not Walls.Walls.isThereWall((self.x + 400, self.y - self.px + 300))):
			self.y += -self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveLeft(self):
		if (not Walls.Walls.isThereWall((self.x - self.px + 400, self.y + 300))):
			self.x += -self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveDown(self):
		if (not Walls.Walls.isThereWall((self.x + 400, self.y + self.px + 300))):
			self.y += self.px
		print str(self.x) + ' + ' + str(self.y)
	def moveRight(self):
		if (not Walls.Walls.isThereWall((self.x + self.px + 400, self.y + 300))):
			self.x += self.px
		print str(self.x) + ' + ' + str(self.y)
	
	def move(self, key_states):
		if key_states[pygame.K_UP]:
			self.moveUp()
		if key_states[pygame.K_DOWN]:
			self.moveDown()
		if key_states[pygame.K_LEFT]:
			self.moveLeft()
		if key_states[pygame.K_RIGHT]:
			self.moveRight()
	
	def getImage(self, millis):
		if millis == 0:
			return self.sprites[self.picnr[0]][self.picnr[1]]
		self.cycletime += millis
		if self.cycletime > self.interval:
			self.picnr[1] += 1
			if self.picnr[1] == 9:
				self.picnr[1] = 0
			self.cycletime = 0
		return self.sprites[self.picnr[0]][self.picnr[1]]
	
	def getPosition(self):	
		return (self.x, self.y)
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y
	
	def setPic(self, key):
		if key == pygame.K_UP:
			self.picnr = [0, 0]
		if key == pygame.K_LEFT:
			self.picnr = [1, 0]
		if key == pygame.K_DOWN:
			self.picnr = [2, 0]
		if key == pygame.K_RIGHT:
			self.picnr = [3, 0]
	