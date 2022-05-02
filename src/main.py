import sys
import time

sleep = 0.05

def type(input:str = '', multiplier = 1, end = '\n') -> None:
	for i in input:
		sys.stdout.write(i)
		sys.stdout.flush()
		time.sleep(sleep / multiplier)
	print('', end = end)
	return

def rInput(inp:str = '', multiplier = 1, end = '\n'):
	type(inp, multiplier, end)
	return input()

def main():
	name = rInput('What\'s your name? -->', 1, ' ')
	type('Ah, so your name is %s. Never get near me or my family ever again.' % name)

if __name__ == '__main__':
	main()
