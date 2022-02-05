from lexer import Lexer
from parser import Parser

while True:
	l = input(">> ")
	t = Lexer(l)
	p = Parser(t.tokenize(), l)
	print(p.parse())