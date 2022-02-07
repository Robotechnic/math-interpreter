from lexer import Lexer
from parser import Parser

while True:
	l = input(">> ")
	t = Lexer(l)
	tokens = t.tokenize()
	print(tokens)
	p = Parser(tokens, l)
	tree = p.parse()
	print(tree)
