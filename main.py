import readline
from interpreter import Interpreter

i = Interpreter()
while True:
	l = input(">>> ")
	print(i.evaluate(l))
