
import Walls
import pygame

class Character:
	
	def __init__(self):
		# position
		self.x = 0;
		self.y = 0;
		# velocity
		self.px = 4
		# sprites
		self.path = '../characters/kauan.png'
		self.sprites = self.readSprites()
		# sprites controller
		self.interval = 150
		self.cycletime = 0
		self.picnr = [3, 0]
		# movement controller
		self.arrow_states = {
			pygame.K_UP: [False, -1],
			pygame.K_DOWN: [False, 1],
			pygame.K_LEFT: [False, -1],
			pygame.K_RIGHT: [False, 1],
		}
		self.arrow = [0, 0]

	def readSprites(self):
		spritesheet = pygame.image.load(file(self.path))
		spritesheet.convert()
		sprites = [[0 for i in range(10)] for i in range(4)]
		
		for s in range(9): # up line contains 9 pictures
			sprites[0][s] = (spritesheet.subsurface((16 + (s * 64), 525, 32, 48)))
		for s in range(9): # left line contains 9 pictures
			sprites[1][s] = (spritesheet.subsurface((18 + (s * 64), 589, 30, 50)))
		for s in range(9): # down line contains 9 pictures
			sprites[2][s] = (spritesheet.subsurface((16 + (s * 64), 653, 32, 48)))
		for s in range(9): # right line contains 9 pictures
			sprites[3][s] = (spritesheet.subsurface((18 + (s * 64), 717, 30, 50)))
		return sprites
		
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
	
	def move(self):
		if self.arrow[1] == -1:
			self.moveUp()
		if self.arrow[1] == 1:
			self.moveDown()
		if self.arrow[0] == -1:
			self.moveLeft()
		if self.arrow[0] == 1:
			self.moveRight()
	
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
	
	def getImage(self, millis):
		if self.arrow != [0, 0]:
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
	
	def setArrow(self, key, state):
		self.arrow_states[key][0] = state
		self.updateArrows()

	def updateArrows(self):
		# update arrow
		self.arrow = [0, 0]
		if self.arrow_states[pygame.K_UP][0]:
			self.arrow[1] += self.arrow_states[pygame.K_UP][1]
		if self.arrow_states[pygame.K_DOWN][0]:
			self.arrow[1] += self.arrow_states[pygame.K_DOWN][1]
		if self.arrow_states[pygame.K_LEFT][0]:
			self.arrow[0] += self.arrow_states[pygame.K_LEFT][1]
		if self.arrow_states[pygame.K_RIGHT][0]:
			self.arrow[0] += self.arrow_states[pygame.K_RIGHT][1]
		# update picnr
		if self.arrow == [0, -1]:  # up
			self.picnr = [0, 0]
		elif self.arrow[0] == -1:  # left
			self.picnr = [1, 0]
		elif self.arrow == [0, 1]: # down
			self.picnr = [2, 0]
		elif self.arrow[0] == 1:   # right
			self.picnr = [3, 0]
	
	# methods for bots
	def up(self):
		self.arrow_states[pygame.K_UP][0] = True
		self.arrow_states[pygame.K_LEFT][0] = False
		self.arrow_states[pygame.K_DOWN][0] = False
		self.arrow_states[pygame.K_RIGHT][0] = False
		self.updateArrows()
		self.move()
	
	def left(self):
		self.arrow_states[pygame.K_UP][0] = False
		self.arrow_states[pygame.K_LEFT][0] = True
		self.arrow_states[pygame.K_DOWN][0] = False
		self.arrow_states[pygame.K_RIGHT][0] = False
		self.updateArrows()
		self.move()
	
	def down(self):
		self.arrow_states[pygame.K_UP][0] = False
		self.arrow_states[pygame.K_LEFT][0] = False
		self.arrow_states[pygame.K_DOWN][0] = True
		self.arrow_states[pygame.K_RIGHT][0] = False
		self.updateArrows()
		self.move()
	
	def right(self):
		self.arrow_states[pygame.K_UP][0] = False
		self.arrow_states[pygame.K_LEFT][0] = False
		self.arrow_states[pygame.K_DOWN][0] = False
		self.arrow_states[pygame.K_RIGHT][0] = True
		self.updateArrows()
		self.move()
	
	def upLeft(self):
		self.arrow_states[pygame.K_UP][0] = True
		self.arrow_states[pygame.K_LEFT][0] = True
		self.arrow_states[pygame.K_DOWN][0] = False
		self.arrow_states[pygame.K_RIGHT][0] = False
		self.updateArrows()
		self.move()
	
	def upRight(self):
		self.arrow_states[pygame.K_UP][0] = True
		self.arrow_states[pygame.K_LEFT][0] = False
		self.arrow_states[pygame.K_DOWN][0] = False
		self.arrow_states[pygame.K_RIGHT][0] = True
		self.updateArrows()
		self.move()
	
	def downLeft(self):
		self.arrow_states[pygame.K_UP][0] = False
		self.arrow_states[pygame.K_LEFT][0] = True
		self.arrow_states[pygame.K_DOWN][0] = True
		self.arrow_states[pygame.K_RIGHT][0] = False
		self.updateArrows()
		self.move()
	
	def downRight(self):
		self.arrow_states[pygame.K_UP][0] = False
		self.arrow_states[pygame.K_LEFT][0] = False
		self.arrow_states[pygame.K_DOWN][0] = True
		self.arrow_states[pygame.K_RIGHT][0] = True
		self.updateArrows()
		self.move()
	