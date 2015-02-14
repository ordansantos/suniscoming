

class Person:
	
	def __init__(self):
		self.x = 0;
		self.y = 0;
		self.path = '../characters/dante.png'
		self.px = 8

		
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
		
	def moveUp(self):
		self.y += -self.px
		
	def moveDown(self):
		self.y += self.px
		
	def moveLeft(self):
		self.x += -self.px
	
	def moveRight(self):
		self.x += self.px
	
	def getPath(self):
		return self.path;
	
	def getPosition(self):	
		return (self.x, self.y)
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y
	
	