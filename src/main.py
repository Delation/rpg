import sys
import time
import uuid
import enum

Entities = enum.Enum('Entities', 'human')
BaseStats = {
	Entities.human: lambda object : [ i[0](i[1]) for i in ( (object.setHP,20), (object.setMP,5), (object.setATK,10), (object.setDEF,5), (object.setINT,30), (object.setSPD,2), (object.setLUC,0) ) ],
}
Tiles = enum.Enum('Tiles', 'grass dirt stone air')
Levels = (
	{
		'name': 'Tutorial',
		'map': {
			'size': (10, 5),
			'data': (
				
			)
		},
		'data': (
			[ Tiles.stone for i in range(10) ],
		),
		'uuid': uuid.uuid4(),
	},
)
Classes = {
	#'Melee': lambda#
	#''
}

sleep = 0.05
punctuation = '?!.,;:-'

def type(input:str = '', multiplier = 1, end = '\n') -> None:
	for i in input:
		sys.stdout.write(i)
		sys.stdout.flush()
		time.sleep(sleep / multiplier)
		if i in punctuation or i == '\n':
			time.sleep(sleep / multiplier * 10)
	print('', end = end)
	return

def rInput(inp:str = '', multiplier = 1, end = '\n'):
	type(inp, multiplier, end)
	return input()

class Stats():
	def __init__(self):
		# Regnerable stats
		self.setHP(0)
		self.setMP(0)
		
		# Individual abilites
		self.setATK(0)
		self.setDEF(0)
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
	
	def setDEF(self, defense:int) -> int:
		self.DEF = int(defense)
		return self.DEF
	
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

class Entity(Stats):
	def __init__(self):
		super().__init__()
		# Identification
		self.setName('')
		self.uuid = uuid.uuid4()
		self.setEntity(Entities.human)
	
	def setName(self, name:str) -> str:
		self.name = str(name)
		return self.name
	
	def setEntity(self, entity:Entities) -> Entities:
		self.entity = Entities(entity)
		BaseStats[self.entity](self)
		return self.entity

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
		self.map = level['map']
		
		# Data
		self.data = level['data']

def main():
	user = Player()
	name = rInput('What\'s your name, young one?', 2, ' ')
	user.setName(name)
	#type('Ah, so your name is %s. Never come near me or my family ever again.' % user.name, 2)
	
	type('Your stats:\n\n%s\n' % user.getStats().replace('\n','\n'*2), 30)
	
	level = Level()
	print('--- %s LEVEL ---\n' % level.name)
	
if __name__ == '__main__':
	main()
