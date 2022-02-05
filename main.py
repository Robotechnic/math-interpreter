from lexer import Lexer

while True:
	l = Lexer(input(">> "))
	print(l.tokenize())