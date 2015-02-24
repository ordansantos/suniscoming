
import pygame
import Person
from apt.auth import update

class Character:
	
	def __init__(self, image = '../characters/ordan.png'):
		# essential
		self.id = 0
		self.name = ''
		self.life = 100
		self.stranger = 5
		# position
		self.x = 0
		self.y = 0
		# velocity
		self.px = 1
		# sprites
		self.path = image
		self.sprites = self.readSprites()
		self.lifeBar = pygame.image.load(file('../characters/blood.png')).convert()
		# sprites controller
		self.interval = 100
		self.cycletime = 0
		self.picnr = [3, 0] # picture on right
		self.lenPic = 9
		# movement controller
		self.side = 'stopped'
		# attack controller
		self.attack_keys = {
			pygame.K_SPACE: False,
			pygame.K_e: False
		}
		self.attackKey = 0
		# furtiveness
		self.furtive = False
		
	""" utilities for the id
	"""
	def setId(self, p_id):
		self.id = p_id
	
	def getId(self):
		return self.id
	
	""" utilities for the position
	"""
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
	
	def getPosition(self):
		return (self.x, self.y)
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y

	""" handle images
	"""
	def readSprites(self):
		# one full day to do this function
		spritesheet = pygame.image.load(file(self.path))
		spritesheet.convert()
		sprites = [[0 for i in range(10)] for i in range(12)]
		
		# walk
		for x in range(4):
			for y in range(9):
				sprites[x][y] = (spritesheet.subsurface((y * 64, (x + 8) * 64, 64, 64)))
		
		# slash
		for x in range(4):
			for y in range(6):
				sprites[x+4][y] = (spritesheet.subsurface((y * 64, (x + 12) * 64, 64, 64)))
		
		# rebuke
		for x in range(4):
			for y in range(7):
				sprites[x+8][y] = (spritesheet.subsurface((y * 64, x * 64, 64, 64)))
		
		return sprites
	
	def getImage(self):
		if self.side != 'stopped' or self.attackKey != 0:
			self.updatePicnr()
			if self.updateTime():
				self.picnr[1] += 1
				if self.picnr[1] == self.lenPic:
					self.updateAttack()
					self.picnr[1] = 0
		return self.sprites[self.picnr[0]][self.picnr[1]]
	
	def updatePicnr(self):
		if self.attackKey == 0:
			if self.side == 'up':
				self.picnr[0] = 0
			elif self.side == 'left':
				self.picnr[0] = 1
			elif self.side == 'down':
				self.picnr[0] = 2
			elif self.side == 'right':
				self.picnr[0] = 3
	
	def updateTime(self):
		time = pygame.time.get_ticks()
		if time < self.cycletime:
			self.cycletime = 0
		if (time - self.cycletime) >= self.interval:
			self.cycletime = pygame.time.get_ticks()
			return True
		return False
	
	def getLifeBar(self):
		return self.lifeBar.subsurface(32 - int(self.life * 0.32), 0, 32, 3)
	
	""" handle movement
	"""
	def move(self, arrow):
		if self.attackKey == 0:
			if arrow == [0, -1]:
				self.up()
			elif arrow == [0, 1]:
				self.down()
			elif arrow == [-1, 0]:
				self.left()
			elif arrow == [1, 0]:
				self.right()
			elif arrow == [-1, -1]:
				self.upLeft()
			elif arrow == [1, -1]:
				self.upRight()
			elif arrow == [-1, 1]:
				self.downLeft()
			elif arrow == [1, 1]:
				self.downRight()
			else:
				self.stopped()
				self.picnr[1] = 0
	
	def up(self):
		if self.attackKey == 0:
			self.side = 'up'
			position = Person.Person.changePersonLocation(self, self.x, self.y - self.px);
			self.setPosition(position)
	
	def left(self):
		if self.attackKey == 0:
			self.side = 'left'
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y )
			self.setPosition(position)
	
	def down(self):
		if self.attackKey == 0:
			self.side = 'down'
			position = Person.Person.changePersonLocation(self, self.x, self.y + self.px);
			self.setPosition(position)
	
	def right(self):
		if self.attackKey == 0:
			self.side = 'right'
			position = Person.Person.changePersonLocation(self, self.x  + self.px , self.y);
			self.setPosition(position)
	
	def upLeft(self):
		if self.attackKey == 0:
			self.side = 'left'
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y - self.px);
			self.setPosition(position)
	
	def upRight(self):
		if self.attackKey == 0:
			self.side = 'right'
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y - self.px);
			self.setPosition(position)
	
	def downLeft(self):
		if self.attackKey == 0:
			self.side = 'left'
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y + self.px);
			self.setPosition(position)
	
	def downRight(self):
		if self.attackKey == 0:
			self.side = 'right'
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y + self.px);
			self.setPosition(position)
	
	def stopped(self):
		self.side = 'stopped'
	
	""" handle attack
	"""
	def attack(self, key):
		if self.attackKey == 0:
			self.attack_keys[key] = True
			self.attackKey = key
			if key == pygame.K_SPACE:
				self.slash()
			elif key == pygame.K_e:
				self.rebuke()
	
	def updateAttack(self):
		if self.attackKey != 0:
			if self.side == 'up':  # up
				self.picnr = [0, 0]
			elif self.side == 'left':  # left
				self.picnr = [1, 0]
			elif self.side == 'down': # down
				self.picnr = [2, 0]
			elif self.side == 'right':   # right
				self.picnr = [3, 0]
			self.attack_keys[self.attackKey] = False
			self.lenPic = 9
			self.interval = 100
			self.attackKey = 0
	
	def hit(self):
		if self.side == 'up':
			for x in xrange(self.x - 8, self.x + 8):
				for y in xrange(self.y - 12, self.y):
					self.checkAttack(x, y)
		elif self.side == 'left':
			for x in xrange(self.x - 12, self.x):
				for y in xrange(self.y - 8, self.y + 8):
					self.checkAttack(x, y)
		elif self.side == 'down':
			for x in xrange(self.x - 8, self.x + 8):
				for y in xrange(self.y, self.y + 12):
					self.checkAttack(x, y)
		elif self.side == 'right':
			for x in xrange(self.x, self.x + 12):
				for y in xrange(self.y - 8, self.y + 8):
					self.checkAttack(x, y)
	
	def checkAttack(self, x, y):
		enemy = Person.Person.getPersonByPosition(x, y)
		if enemy != None:
			if enemy.life >= 5:
				enemy.life -= 5
			if self.life <= 95:
				self.life += 5
	
	def slash(self):
		if self.side == 'up':
			self.picnr = [4, 0]
		elif self.side == 'left':
			self.picnr = [5, 0]
		elif self.side == 'down':
			self.picnr = [6, 0]
		elif self.side == 'right':
			self.picnr = [7, 0]
		self.lenPic = 6
		self.interval = 80
		self.hit()
	
	def rebuke(self):
		if self.side == 'up':
			self.picnr = [8, 0]
		elif self.side == 'left':
			self.picnr = [9, 0]
		elif self.side == 'down':
			self.picnr = [10, 0]
		elif self.side == 'right':
			self.picnr = [11, 0]
		self.lenPic = 7
		self.interval = 150
		self.hit()
	
	""" furtiveness """
	def updateFurtiveness(self):
		self.furtive = not self.furtive
	