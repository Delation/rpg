import sys
import time
import uuid
import enum

Entities = enum.Enum('Entities', 'human')
BaseStats = {
	Entities.human: lambda object : [ i[0](i[1]) for i in ( (object.setHP,20), (object.setMP,5), (object.setATK,10), (object.setINT,30), (object.setSPD,2), (object.setLUC,0), ) ],
}
Tiles = enum.Enum('Tiles', 'air grass dirt stone')
Levels = (
	{
		'name': 'Tutorial',
		'maps': (
			{
				'id': 0,
				'data': lambda map : [ i[0](**i[1]) for i in ( (map.setTile, {'x': 0, 'y': 0, 'tile': Tiles.grass,}), ) ],
			},
		),
		'mapIndex': 0,
		'uuid': uuid.uuid4(),
	},
)
Classes = {
	'Melee': lambda a : a+b,
	'Ranger': lambda a : a+b,
	'Mage': lambda a : a+b,
	'Support': lambda a : a+b,
}
Directions = enum.Enum('Directions', 'up down left right')
Commands = enum.Enum('Commands', 'exit help stats')

sleep = 0.05
punctuation = '?!.,;:-'

def log(*args, **kwargs):
	print(*args, **kwargs)
		
def clear():
	log('\x1B[2J\x1B[H')
	
def type(input:str = '', multiplier = 1, end = '\n') -> None:
	if multiplier < 0:
		log(input, end = end)
		return
	for i in input:
		sys.stdout.write(i)
		sys.stdout.flush()
		time.sleep(sleep / multiplier)
		if i in punctuation or i == '\n':
			time.sleep(sleep / multiplier * 6)
	log('', end = end)
	return

def rInput(inp:str = '', multiplier = 1, end = '\n') -> str:
	type(inp, multiplier, end)
	return input()

class Map():
	def __init__(self, id:int):
		self.id = id
		self.uuid = uuid.uuid4()
		self.data = []
	
	# Map().setSize() may or may not be implemented in the future
	#def setSize(self, **args) -> None:
		#self.size = args
		## Note: This does not validate the dict before passing it, so     #
		## please make sure you do not pass anything other than the below  #
		## dict: {'x': x, 'y': y}. The origin will always remain (0,0)     #
		#return
	
	def setTile(self, **args) -> None:
		self.data.append(args)
		# Note: If you are creating your own levels, make sure it follows #
		# the guidelines, because Map().setTile() has no checks, so the   #
		# program will crash upon read failure.                           #
		return
	
	def showMap(self, user) -> str:
		text = ''
		for y in range(user.y - 2, user.y + 3):
			for x in range(user.x - 2, user.x + 3):
				hit = '_'
				for tile in self.data:
					if user.x == x and user.y == y:
						hit = '+'
					elif tile['x'] == x and tile['y'] == y:
						hit = '#'
				text = text + '|' + hit + '|'
			text = text + '\n'
		return text
		

class Coordinates():
	def __init__(self, x:int = 0, y:int = 0):
		self.setCoordinates(x = x, y = y)

	def setCoordinates(self, **coordinates) -> list:
		x = coordinates.get('x')
		y = coordinates.get('y')
		if not x is None:
			self.x = x
		if not y is None:
			self.y = y
		return x, y
	
	def checkCoordinates(self, x:int, y:int) -> bool:
		return self.x == x and self.y == y

class Stats():
	def __init__(self):
		# Regnerable stats
		self.setHP(0)
		self.setMP(0)
		
		# Individual abilites
		self.setATK(0)
		self.setINT(0)
		self.setSPD(0)
		self.setLUC(0)
	
	# Regenerable stats
	def setHP(self, health:int) -> int:
		self.HP = int(health)
		return self.HP
	
	def setMP(self, mana:int) -> int:
		self.MP = int(mana)
		return self.MP
	
	# Individual abilities
	def setATK(self, attack:int) -> int:
		self.ATK = int(attack)
		return self.ATK
	
	def setINT(self, intelligence:int) -> int:
		self.INT = int(intelligence)
		return self.INT
	
	def setSPD(self, speed:int) -> int:
		self.SPD = int(speed)
		return self.SPD
	
	def setLUC(self, luck:float) -> float:
		self.LUC = float(luck)
		return self.LUC	

	# Various functions
	def getStats(self):
		return '\n'.join([ '%s: %s' % (i, self.__dict__[i]) for i in self.__dict__.keys() if i in dir(Stats()) ])

class Entity(Stats, Coordinates):
	def __init__(self):
		super().__init__()
		# Identification
		self.setName('')
		self.uuid = uuid.uuid4()
		self.setEntity(Entities.human)
		self.setCoordinates(x = 0, y = 0)
	
	def setName(self, name:str) -> str:
		self.name = str(name)
		return self.name
	
	def setEntity(self, entity:Entities) -> Entities:
		self.entity = Entities(entity)
		BaseStats[self.entity](self)
		return self.entity
	
	def input(self, inputs:list) -> str:
		if not isinstance(inputs, list):
			inputs = (inputs,)
		for input in inputs:
			if isinstance(input, Directions):
				if input == Directions.up:
					self.y -= 1
				elif input == Directions.down:
					self.y += 1
				elif input == Directions.left:
					self.x -= 1
				elif input == Directions.right:
					self.x += 1
			elif isinstance(input, Commands):
				if input == Commands.exit:
					quit()
				elif input == Commands.help:
					return ':)'
				elif input == Commands.stats:
					return 'Your stats:\n\n%s\n' % self.getStats().replace('\n','\n'*2)
			else:
				return False
		return ''

class Player(Entity):
	def __init__(self):
		super().__init__()
		
		# Most players will be human
		self.setEntity(Entities.human)

class Level():
	def __init__(self, level:dict = next(i for i in Levels if i['name'] == 'Tutorial')):
		self.level = self.load(level)
	
	def load(self, level:dict):
		self.name = level['name']
		self.uuid = level['uuid']
		
		# Map
		self.maps = [ Map(map['id']) for map in level['maps'] ]
		[ level['maps'][i]['data'](self.maps[i]) for i in range(len(level['maps'])) ]
		self.mapIndex = level['mapIndex']
	
	def showMap(self, user:Player) -> str:
		return self.maps[self.mapIndex].showMap(user)

def main() -> None:
	user = Player()
	name = rInput('What\'s your name, young one?', 1, ' ')
	user.setName(name)
	type('Ah, so your name is %s. I\'ve heard very much about you.\nYes, very much indeed.' % user.name, 1)
	
	rInput('Press enter to continue!', 2)
	
	level = Level()
	next = ''
	while True:
		clear()
		log('--- %s LEVEL ---\nRoom: %s' % (level.name, level.maps[level.mapIndex].id))
		input = rInput(level.showMap(user) + ('' if not next else '\n%s\n' % next), -1, '>>> ').lower()
		next = ''
		if input in Directions._member_names_:
			next = user.input(Directions(Directions._member_names_.index(input) + 1))
		elif input in Commands._member_names_:
			next = user.input(Commands(Commands._member_names_.index(input) + 1))
		else:
			next = 'Type \'help\' to see all the available commands!'
	
if __name__ == '__main__':
	main()
