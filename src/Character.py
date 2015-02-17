
import Walls
import pygame

class Character:
	
	def __init__(self):
		# essential
		self.name = ''
		self.life = 100
		self.stranger = 5
		# position
		self.x = 0
		self.y = 0
		# velocity
		self.px = 4
		# sprites
		self.path = '../characters/human1.png'
		self.sprites = self.readSprites()
		# sprites controller
		self.interval = 150
		self.cycletime = 0
		self.picnr = [3, 0]
		self.lenPic = 9
		# movement controller
		self.arrow_states = {
			pygame.K_UP: [False, -1],
			pygame.K_DOWN: [False, 1],
			pygame.K_LEFT: [False, -1],
			pygame.K_RIGHT: [False, 1],
		}
		self.arrow = [0, 0]
		# attack controller
		self.attack_keys = {
			pygame.K_SPACE: False,
			pygame.K_e: False
		}
		self.side = 'right'

	def readSprites(self):
		
		# more than one day for this purpose
		spritesheet = pygame.image.load(file(self.path))
		spritesheet.convert()
		sprites = [[0 for i in range(10)] for i in range(8)]
		
		# walk
		for x in range(4):
			for y in range(9):
				sprites[x][y] = (spritesheet.subsurface((y * 64, (x + 8) * 64, 64, 64)))
		
		# slash
		for x in range(4):
			for y in range(6):
				sprites[x+4][y] = (spritesheet.subsurface((y * 64, (x + 12) * 64, 64, 64)))
		
		return sprites
		
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
	
	def move(self):
		if self.attackNow():
			return
		if self.arrow[1] == -1:
			self.moveUp()
		if self.arrow[1] == 1:
			self.moveDown()
		if self.arrow[0] == -1:
			self.moveLeft()
		if self.arrow[0] == 1:
			self.moveRight()
	
	def moveUp(self):
		if (not Walls.Walls.isThereWall((self.x, self.y - self.px))):
			self.y += -self.px
		# print str(self.x) + ' + ' + str(self.y)
	def moveLeft(self):
		if (not Walls.Walls.isThereWall((self.x - self.px, self.y))):
			self.x += -self.px
		# print str(self.x) + ' + ' + str(self.y)
	def moveDown(self):
		if (not Walls.Walls.isThereWall((self.x, self.y + self.px))):
			self.y += self.px
		# print str(self.x) + ' + ' + str(self.y)
	def moveRight(self):
		if (not Walls.Walls.isThereWall((self.x + self.px, self.y))):
			self.x += self.px
		# print str(self.x) + ' + ' + str(self.y)
	
	def getImage(self, millis):
		if self.arrow != [0, 0] or self.attackNow():
			self.cycletime += millis
			if self.cycletime > self.interval:
				self.picnr[1] += 1
				if self.picnr[1] == self.lenPic:
					self.updateAttack()
					self.updatePicnr()
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
		self.updatePicnr()
	
	def updatePicnr(self):
		if self.arrow == [0, -1]:  # up
			self.picnr = [0, 0]
			self.side = 'up'
		elif self.arrow[0] == -1:  # left
			self.picnr = [1, 0]
			self.side = 'left'
		elif self.arrow == [0, 1]: # down
			self.picnr = [2, 0]
			self.side = 'down'
		elif self.arrow[0] == 1:   # right
			self.picnr = [3, 0]
			self.side = 'right'
	
	def attack(self, key):
		if key == pygame.K_SPACE:
			self.attack_keys[key] = True
			self.slash()
			self.lenPic = 6
			self.interval = 80
	
	def updateAttack(self):
		for k in self.attack_keys.keys():
			self.attack_keys[k] = False
		if self.side == 'up':  # up
			self.picnr = [0, 0]
		elif self.side == 'left':  # left
			self.picnr = [1, 0]
		elif self.side == 'down': # down
			self.picnr = [2, 0]
		elif self.side == 'right':   # right
			self.picnr = [3, 0]
		self.lenPic = 9
		self.interval = 150
	
	def attackNow(self):
		if True in self.attack_keys.values():
			return True
	
	def slash(self):
		if self.side == 'up':  # up
			self.picnr = [4, 0]
		elif self.side == 'left':  # left
			self.picnr = [5, 0]
		elif self.side == 'down': # down
			self.picnr = [6, 0]
		elif self.side == 'right':   # right
			self.picnr = [7, 0]
	
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
	