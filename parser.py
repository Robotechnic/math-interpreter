from nodes import *
from error import displayError, ErrorType
from nodes import constantNode
from tokens import Token, TokenType, token

class Parser:
	"""
	A class that parses a list of tokens and interprets them
	"""
	def __init__(self, tokens : list, line : str) -> None:
		self.i = 0
		self._tokens = list()
		self.tokens = tokens
		self.tree = None
		self.line = line
		self.error = False
		self.expressions = [
			[TokenType.PLUS, TokenType.MINUS],
			[AddNode,        SubNode]
		]
		self.terms = [
			[TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.POW],
			[MulNode,       DivNode,       ModNode,       PowNode]
		]
	
	@property
	def tokens(self) -> list:
		return self._tokens
	
	@tokens.setter
	def tokens(self, tokens : list) -> None:
		for t in tokens:
			if type(t) != Token:
				raise TypeError("tokens must be a list of Token objects")
		
		self._tokens = tokens
	
	def check_index(self) -> bool:
		return self.i < len(self.tokens)

	def factor(self) -> Node:
		"""
		Parses factors and parenthesis in token list
		"""
		if self.error:
			return
		elif not self.check_index():
			displayError(self.line, ErrorType.ArithmeticExpressionError, self.i, "Missing operator")
			self.error = True
		elif self.tokens[self.i].type == TokenType.KEYWORD:
			constant_node = ConstantNode(self.tokens[self.i].value)
			if not constant_node.is_valid():
				self.error = True
				error_range = range(
					self.tokens[self.i].start,
					self.tokens[self.i].end
				)
				displayError(self.line, ErrorType.UnknownConstError, error_range)
			else:
				self.i += 1
				return constant_node
		elif self.tokens[self.i].type == TokenType.LPAREN:
			self.i += 1
			node = self.expression()
			if self.check_index() and self.tokens[self.i].type == TokenType.RPAREN:
				self.i += 1
			else:
				displayError(self.line, ErrorType.MissingParentesisError, self.i)
				self.error = True
			return node
		elif self.tokens[self.i].type == TokenType.RPAREN:
			self.error = True
			self.i += 1
			displayError(self.line, ErrorType.MissingParentesisError, self.i)
		elif self.tokens[self.i].type == TokenType.MINUS:
			self.i += 1
			return NegNode(self.factor())
		elif self.tokens[self.i].type == TokenType.PLUS:
			self.i += 1
			return self.factor()
		elif self.tokens[self.i].type == TokenType.NUMBER:
			node = NumberNode(self.tokens[self.i].value)
			self.i += 1
			return node
		else:
			self.error = True
			displayError(self.line, ErrorType.UnexpectedCharacterError, self.i)

	def term(self) -> Node:
		"""
		Parses terms in token list
		"""
		node = self.factor()

		while self.i < len(self.tokens) and self.tokens[self.i].type in self.terms[0] and not self.error:
			term = self.terms[1][self.terms[0].index(self.tokens[self.i].type)]
			self.i += 1
			fact = self.factor()
			if fact != None:
				node = term(node, fact)
			
		return node

	def expression(self) -> Node:
		"""
		Parses expressions in token list
		"""
		node = self.term()
		while self.i < len(self.tokens) and self.tokens[self.i].type in self.expressions[0] and not self.error:
			expression = self.expressions[1][self.expressions[0].index(self.tokens[self.i].type)]
			self.i += 1
			term = self.term()
			if term != None:
				node = expression(node, term)
			
		return node


	def parse(self) -> Node:
		self.i = 0
		self.tree = self.expression()
		
		if self.error:
			return None
		
		return self.tree


if __name__ == "__main__":
	# test parenthesis priority
	p = Parser([
		Token(TokenType.NUMBER, 1, 0),
		Token(TokenType.MUL, "*", 2),
		Token(TokenType.LPAREN, "(", 4),
		Token(TokenType.NUMBER, 258, 5),
		Token(TokenType.PLUS, "+", 8),
		Token(TokenType.NUMBER, 3.5, 9),
		Token(TokenType.RPAREN, ")", 12)
	], "1*(258+3.5)")
	result = p.parse()
	assert type(result) == MulNode
	assert type(result.left) == NumberNode
	assert result.left.value == 1
	assert type(result.right) == AddNode
	assert type(result.right.left) == NumberNode
	assert result.right.left.value == 258
	assert type(result.right.right) == NumberNode
	assert result.right.right.value == 3.5

	# test priority with no parenthesis
	p = Parser([
		Token(TokenType.NUMBER, 1, 0),
		Token(TokenType.MUL, "*", 2),
		Token(TokenType.NUMBER, 258, 4),
		Token(TokenType.PLUS, "+", 7),
		Token(TokenType.NUMBER, 3.5, 8)
	],"1*258+3.5")
	result = p.parse()
	assert type(result) == AddNode
	assert type(result.left) == MulNode
	assert type(result.left.left) == NumberNode
	assert result.left.left.value == 1
	assert type(result.left.right) == NumberNode
	assert result.left.right.value == 258
	assert type(result.right) == NumberNode
	assert result.right.value == 3.5

	

