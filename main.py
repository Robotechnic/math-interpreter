import readline
from interpreter import Interpreter

try:
	readline.read_history_file()
except FileNotFoundError:
	pass

i = Interpreter()
while True:
	l = input(">>> ")
	readline.write_history_file()
	if l == "exit":
		break
	print(i.evaluate(l))