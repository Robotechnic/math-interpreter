from ast import keyword
from numpy import true_divide
from nodes import *
from error import displayError, ErrorType
from nodes import constantNode
from nodes import functionNode
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
	
	def manage_parenthesis(self) -> Node:
		if self.tokens[self.i].type == TokenType.RPAREN:
			self.error = True
			self.i += 1
			displayError(self.line, ErrorType.MissingParentesisError, self.i)
			return None
		elif self.tokens[self.i].type == TokenType.LPAREN:
			self.i += 1
			node = self.expression()
			if self.check_index() and self.tokens[self.i].type == TokenType.RPAREN:
				self.i += 1
				return node
			else:
				displayError(self.line, ErrorType.MissingParentesisError, self.i)
				self.error = True
				return None
		else:
			self.error = True
			displayError(self.line, ErrorType.MissingParentesisError, self.i, "Open parenthesis expected")
			return None
		
	def parse_function_args(self) -> list:
		args = []
		while self.check_index() and \
				self.tokens[self.i].type != TokenType.RPAREN:
			arg = self.expression()
			if arg != None:
				args.append(arg)
			else:
				return None
			
			if not self.check_index():
				self.error = True
				displayError(
					self.line,
					ErrorType.MissingParentesisError,
					args[-1].end,
					"Closing parenthesis expected"
				)
				return None
			elif self.tokens[self.i].type == TokenType.COMMA:
				self.i += 1
	
	def check_function_args(self, args : list) -> Node:
		if FunctionNode.check_args(keyword.value, len(args)):
			return FunctionNode(keyword.value, args, keyword.start, args[-1].end)
		else:
			displayError(
				self.line,
				ErrorType.FunctionArgumentError, 
				range(keyword.end + 1, args[-1].end),
				f"Function {keyword.value} takes {FunctionNode.get_args(keyword.value)} arguments but {len(args)} were given"
			)
			self.error = True
			return None

	def parse_function(self, keyword : Token) -> Node:
		if self.check_index() and self.tokens[self.i].type == TokenType.LPAREN:
			self.i += 1
			args = self.parse_function_args()
			if args:
				return self.check_function_args(args)
			else:
				return None
		else:
			self.error = True
			displayError(self.line, ErrorType.MissingParentesisError, keyword.end, "Open parenthesis expected")
			return None


	def detect_keyword(self) -> Node:
		token = self.tokens[self.i]
		if ConstantNode.is_valid(token.value):
			self.i += 1
			return ConstantNode(token.value, token.start, token.end)
		elif FunctionNode.is_valid(token.value):
			self.i += 1
			return self.parse_function(token)
		else:
			self.error = True
			displayError(
				self.line,
				ErrorType.UnexpectedCharacterError, 
				range(token.start, token.end)	
			)
			return None

	def base_token(self) -> Node:
		token = self.tokens[self.i]
		if token.type == TokenType.MINUS:
			self.i += 1
			return NegNode(self.factor(), token.start, token.end)
		elif token.type == TokenType.PLUS:
			self.i += 1
			return self.factor()
		elif token.type == TokenType.NUMBER:
			node = NumberNode(token.value, token.start, token.end)
			self.i += 1
			return node
		else:
			self.error = True
			displayError(
				self.line, 
				ErrorType.UnexpectedCharacterError, 
				range(token.start, token.end)
			)

	def factor(self) -> Node:
		"""
		Parses factors and parenthesis in token list
		"""
		if self.error:
			return None
		elif not self.check_index():
			displayError(
				self.line,
				ErrorType.ArithmeticExpressionError,
				self.tokens[-1].end,
				"Missing operator"
			)
			self.error = True
			return None
		elif self.tokens[self.i].type == TokenType.KEYWORD:
			return self.detect_keyword()
		elif self.tokens[self.i].type == TokenType.LPAREN or \
			 self.tokens[self.i].type == TokenType.RPAREN:
			return self.manage_parenthesis()
		else:
			return self.base_token()
		

	def term(self) -> Node:
		"""
		Parses terms in token list
		"""
		node = self.factor()

		while self.i < len(self.tokens) and self.tokens[self.i].type in self.terms[0] and not self.error:
			term = self.terms[1][
				self.terms[0].index(self.tokens[self.i].type)
			]
			self.i += 1
			fact = self.factor()
			if fact != None:
				node = term(node, fact, node.start, fact.end)
			
		return node

	def expression(self) -> Node:
		"""
		Parses expressions in token list
		"""
		node = self.term()
		while self.i < len(self.tokens) and self.tokens[self.i].type in self.expressions[0] and not self.error:
			expr = self.expressions[1][
				self.expressions[0].index(self.tokens[self.i].type)
			]
			self.i += 1
			term = self.term()
			if term != None:
				node = expr(node, term, node.start, term.end)
			
		return node


	def parse(self) -> Node:
		"""Convert token list into node tree

		Returns:
			Node: Top node of the Tree
		"""
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

	

