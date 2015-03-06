
import pygame, time
import Person
import Sound

class Character:
	
	# attack_keys
	NO_ATTACK = 0
	SLASH = pygame.K_SPACE
	REBUKE = pygame.K_e
	
	def __init__(self, (x, y)=(0, 0), image='../characters/ordan.png', movement_range=25):
		# essential
		self.setPosition((x, y))
		self.initial_position = (x, y)
		self.id = 0
		self.name = 'Example'
		self.life = 100
		self.stranger = 5
		# speed
		self.px = 1
		self.fast = False
		# sprites
		self.path = image
		self.sprites = self.readSprites()
		self.life_bar = pygame.image.load(file('../characters/blood.png')).convert()
		self.death_blood = pygame.image.load(file('../characters/death_blood.png')).convert_alpha()
		self.blood_squirt = pygame.image.load(file('../characters/blood_squirt.png')).convert_alpha()
		# sprites controller
		self.interval = 100
		self.cycletime = 0
		self.picnr = [3, 0]  # picture on right
		self.lenPic = 9
		self.squirt_time = 0
		# movement controller
		self.side = 'right'
		self.movement = False
		# attack controller
		self.attack_keys = {
			Character.SLASH: False,
			Character.REBUKE: False
		}
		self.attack_key = Character.NO_ATTACK
		self.attacked = False
		# furtiveness
		self.furtive = False
		# death
		self.death = pygame.time.get_ticks()
		self.death_interval = 7000  # 7 seconds
		
		# bot
		self.movement_range = movement_range
		
		self.enemy = None
	# utilities for the id
	def setId(self, p_id):
		self.id = p_id
	
	def getId(self):
		return self.id
	
	# utilities for the position
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
	
	def getPosition(self):
		return (self.x, self.y)
	
	def getInitialPosition(self):
		return self.initial_position
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y
		
	def getMovementRange(self):
		return self.movement_range
	
	def getEnemy(self):
		return self.enemy
	
	def setEnemy(self, enemy):
		self.enemy = enemy
		
	# handle images
	def readSprites(self):
		# one full day to do this function
		spritesheet = pygame.image.load(file(self.path))
		spritesheet.convert()
		sprites = []
		
		# walk
		for x in range(4):
			sprites.append([])
			for y in range(9):
				sprites[x].append((spritesheet.subsurface((y * 64, (x + 8) * 64, 64, 64))))
		
		# slash
		for x in range(4):
			sprites.append([])
			for y in range(6):
				sprites[x + 4].append((spritesheet.subsurface((y * 64, (x + 12) * 64, 64, 64))))
		
		# rebuke
		for x in range(4):
			sprites.append([])
			for y in range(7):
				sprites[x + 8].append((spritesheet.subsurface((y * 64, x * 64, 64, 64))))
		
		# dying
		sprites.append([])
		for y in range(6):
			sprites[12].append((spritesheet.subsurface((y * 64, 20 * 64, 64, 64))))
		
		return sprites
	
	def getImage(self):
		x, y = self.picnr
		if self.movement or self.attack_key != Character.NO_ATTACK or self.life == 0:
			self.updatePicnr()
			if self.updateTime():
				self.picnr[1] += 1
				if self.picnr[1] == self.lenPic:
					self.updateAttack()
					if self.picnr[0] == 12: self.isDead()
					self.picnr[1] = 0
		return self.sprites[x][y]
	
	def updatePicnr(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
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
		return self.life_bar.subsurface(32 - int(self.life * 0.32), 0, 32, 3)
	
	def getDeathBlood(self):
		if self.life == 0:
			return self.death_blood
		return None
	
	def getBloodSquirt(self):
		time = pygame.time.get_ticks()
		if time - self.squirt_time >= 1500:
			self.attacked = False
			self.squirt_time = time
		if self.attacked and self.life != 0:
			return self.blood_squirt
		return None
	
	# handle movement
	def move(self, arrow):
		if self.attack_key == Character.NO_ATTACK:
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
	
	def doAMovement(self, (x1, y1)):
		x, y = self.getPosition()

		if (x1 > x):
			if (y1 > y):
				self.downRight()
			elif (y1 < y):
				self.upRight()
			else:
				self.right()

		elif (x1 < x):
			if (y1 > y):
				self.downLeft()
			elif (y1 < y):
				self.upLeft()
			else:
				self.left()

		else:
			if (y1 > y):
				self.down()
			elif (y1 < y):
				self.up()
	
	def up(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'up'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x, self.y - self.px);
			self.setPosition(position)
			
	def left(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y)
			self.setPosition(position)
	
	def down(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'down'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x, self.y + self.px);
			self.setPosition(position)
	
	def right(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px , self.y);
			self.setPosition(position)
	
	def upLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y - self.px);
			self.setPosition(position)
	
	def upRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y - self.px);
			self.setPosition(position)
	
	def downLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y + self.px);
			self.setPosition(position)
	
	def downRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y + self.px);
			self.setPosition(position)
	
	def stopped(self):
		self.movement = False
		self.picnr[1] = 0
	
	# handle attack
	def attack(self, key):
		if self.attack_key == Character.NO_ATTACK:
			self.attack_keys[key] = True
			self.attack_key = key
			if key == Character.SLASH:
				Sound.Sound.attackPlay()
				self.slash()
			elif key == Character.REBUKE:
				Sound.Sound.attackPlay()
				self.rebuke()
	
	def updateAttack(self):
		if self.attack_key != Character.NO_ATTACK:
			if self.side == 'up':  # up
				self.picnr = [0, 0]
			elif self.side == 'left':  # left
				self.picnr = [1, 0]
			elif self.side == 'down':  # down
				self.picnr = [2, 0]
			elif self.side == 'right':  # right
				self.picnr = [3, 0]
			self.attack_keys[self.attack_key] = False
			self.lenPic = 9
			self.interval = 100
			self.attack_key = Character.NO_ATTACK
	
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
		if self.getPosition() != (x, y):
			enemy = Person.Person.getPersonByPosition(x, y)
			if enemy != None:
				enemy.setEnemy(self)
				if enemy.life >= self.stranger:
					enemy.attacked = True
					enemy.life -= self.stranger
					if enemy.life == 0:
						enemy.dying()
				if self.life <= 100 - self.stranger:
					self.life += self.stranger
	
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
	
	# furtiveness
	def updateFurtiveness(self):
		self.furtive = not self.furtive
	
	# handle life
	def isDead(self):
		if self.life == 0:
			self.death = -1
			Person.Person.setDead(self)
	
	def dying(self):
		Sound.Sound.deathPlay()
		Person.Person.freeLocation(self)
		self.picnr = [12, 0]
		self.lenPic = 6
		self.interval = 500
	
	# handle speed
	def updateSpeed(self, fast):
		if fast:
			self.fast = True
			self.px = 2
		else:
			self.fast = False
			self.px = 1
	
	def updateDeath(self, period):
		if period == "morning":
			time = pygame.time.get_ticks()
			if time - self.death >= self.death_interval:
				self.life -= self.stranger
				if self.life < 0:
					self.life = 0
				self.death = time
			elif time - self.death >= (self.death_interval / 5):
				if self.fast:
					self.life -= 1
				if self.life < 0:
					self.life = 0
					self.death = time
	
	
