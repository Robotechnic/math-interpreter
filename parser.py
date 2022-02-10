from nodes import *
from error import displayError
from tokens import Token, TokenType
from errorTypes import ErrorType
from functionProps import FunctionArg, ArgRange, StringRanges
from typing import Callable

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
		self._token = None

		self.comparisons = [
			[TokenType.EQUAL, TokenType.NOTEQUAL, TokenType.GREATER, TokenType.LESS, TokenType.GREATEREQUAL, TokenType.LESSEQUAL],
			[ComparisionType.EQUAL,  ComparisionType.NOTEQUAL, ComparisionType.GREATER, ComparisionType.LESS, ComparisionType.GREATEREQUAL, ComparisionType.LESSEQUAL]
		]
		self.expressions = [
			[TokenType.PLUS, TokenType.MINUS],
			[AddNode,        SubNode]
		]
		self.terms = [
			[TokenType.MUL, TokenType.DIV, TokenType.MOD],
			[MulNode,       DivNode,       ModNode]
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
	
	@property
	def token(self) -> Token:
		return self.tokens[self.i]

	def check_index(self) -> bool:
		return self.i < len(self.tokens)
	
	def manage_parenthesis(self) -> Node:
		if self.token == TokenType.RPAREN:
			self.error = True
			self.i += 1
			displayError(self.line, ErrorType.MissingParentesisError, self.i)
			return None
		elif self.token == TokenType.LPAREN:
			self.i += 1
			node = self.expression()
			if self.check_index() and self.token == TokenType.RPAREN:
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
	
	def parse_keyword_range(self) -> ArgRange:
		"""
		If the range is a keyword, check if it is a valid range

		Returns:
			ArgRange: keyword range
		"""
		if self.token.value in StringRanges.__members__:
			arg_range = ArgRange(StringRanges(self.token.value))
			self.i += 1
			return arg_range
		else:
			self.error = True
			displayError(
				self.line,
				ErrorType.UnexpectedTokenError,
				range(self.token.start, self.token.end)
			)
	
	def get_arg_range_bound(self) -> int | float:
		"""
		Return range bound of a range
		"""
		if self.token == TokenType.SEMICOLON or self.token == TokenType.RBRACKET:
			return None
		
		bound = self.factor()
		if bound:
			if isinstance(bound, NumberNode):
				return bound.value
			elif isinstance(bound, NegNode) and isinstance(bound.value, NumberNode):
				return -bound.value.value
			else:
				self.error = True
				displayError(
					self.line,
					ErrorType.UnexpectedTokenError,
					bound.start,
					"Range bounds must be numbers"
				)
		else:
			self.error = True
			displayError(
				self.line,
				ErrorType.SyntaxError,
				self.token.end,
				"Missing range bound"
			)
	
	def get_range_min_bound(self) -> int | float:
		min_bound = self.get_arg_range_bound()
		if self.error:
			return None
		if self.check_index() and self.token != TokenType.SEMICOLON:
			self.error = True
			displayError(
				self.line,
				ErrorType.SyntaxError,
				self.token.end,
				"Missing semicolon"
			)
			return None

		self.i += 1

		return min_bound
	
	def get_range_max_bound(self) -> int | float:
		max_bound = self.get_arg_range_bound()
		if self.error:
			return None
		if self.check_index() and self.token != TokenType.RBRACKET:
			self.error = True
			displayError(
				self.line,
				ErrorType.MissingParentesisError,
				self.token.end,
				"Missing closing bracket"
			)
			
			return None
		
		self.i += 1
		
		return max_bound
	
	def parse_args_range_bounds(self) -> ArgRange:
		min_bound = self.get_range_min_bound()
		max_bound = self.get_range_max_bound()
		
		if min_bound is None and max_bound is None or self.error:
			return None
		
		return ArgRange(min_bound = min_bound, max_bound = max_bound)

	def parse_arg_range(self) -> Node:
		if self.check_index() and self.token == TokenType.LBRACKET:
			self.i += 1
			if self.token == TokenType.KEYWORD:
				bounds = self.parse_keyword_range()
			else:
				bounds =  self.parse_args_range_bounds()
			
			if bounds:
				return bounds
			elif not self.error:
				self.error = True
				displayError(
					self.line,
					ErrorType.ArithmeticExpressionError,
					self.token,
					"Missing range"
				)		

		return None
	
	def parse_function_declaration_arg(self) -> FunctionArg:
		"""
		Parse function declaration argument
		Get name and validity ranges
		
		Returns:
			FunctionArg: parsed argument
		"""
		arg = self.expression()
		if arg:
			if not isinstance(arg, VarNode):
				self.error = True
				displayError(
					self.line,
					ErrorType.UnexpectedTokenError,
					range(arg.start, arg.end),
					"Function arguments must be variables"
				)
			else:
				arg_range = self.parse_arg_range()
				if not self.error:
					return FunctionArg(arg.name, arg.start, arg.end, arg_range)

		return None

	
	def parse_function_call_arg(self) -> Node:
		return self.expression()

	def parse_function_args(self, arg_parse : Callable) -> list:
		"""
		Parse function aguments

		Args:
			arg_parse (Callable): function to parse arguments

		Returns:
			list: list of processed arguments
		"""
		args = []
		while self.check_index() and \
			  self.token.type != TokenType.RPAREN:
			arg = arg_parse()
			if arg:
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
			elif self.token == TokenType.COMMA:
				self.i += 1
			elif self.token.type != TokenType.RPAREN:
				self.error = True
				displayError(
					self.line,
					ErrorType.ArithmeticExpressionError,
					args[-1].end,
					"Missing comma"
				)
				return None	
		self.i += 1

		return args
	
	def parse_function_declaration(self) -> tuple:
		"""
		Parse function declaration: get name and arguments of the function

		Returns:
			tuple: function name and function args
		"""
		if self.token != TokenType.KEYWORD:
			self.error = True
			displayError(
				self.line,
				ErrorType.UnexpectedTokenError,
				0
			)
		else:
			function_name = self.token.value
			self.i += 1
			if self.check_index() and self.token == TokenType.LPAREN:
				self.i += 1
				function_args = self.parse_function_args(self.parse_function_declaration_arg)

				if function_args:
					return function_name, function_args
			else:
				self.error = True
				displayError(
					self.line,
					ErrorType.FunctionDeclarationError,
					self.token.start,
					"Opening parenthesis expected"
				)
		
		return None
	
	def make_function_call(self, functionName : Node) -> Node:
		args = self.parse_function_args(self.parse_function_call_arg)
		if args != 	None:
			return FunctionNode(functionName.name, args, functionName.start, args[-1].end)
		else:
			return None


	def base(self) -> Node:
		if self.check_index():
			if self.token == TokenType.LPAREN or \
				self.token == TokenType.RPAREN:
				node = self.manage_parenthesis()
			elif self.token == TokenType.NUMBER:
				node = NumberNode(self.token.value, self.token.start, self.token.end)
				self.i += 1
			elif self.token == TokenType.KEYWORD:
				node = VarNode(self.token.value, self.token.start, self.token.end)
				self.i += 1

			else:
				self.error = True
				displayError(
					self.line, 
					ErrorType.UnexpectedTokenError, 
					range(self.token.start, self.token.end)
				)
				return None
			return node
		else:
			self.error = True
			displayError(
				self.line,
				ErrorType.ArithmeticExpressionError,
				self.tokens[-1].end,
				"Missing number or expression"
			)
			return None
	
	def call(self) -> Node:
		node = self.base()
		if node:
			if self.check_index() and self.token == TokenType.LPAREN:
				self.i += 1
				if isinstance(node, VarNode):
					node = self.make_function_call(node)
				else:
					self.error = True
					displayError(
						self.line,
						ErrorType.ArithmeticExpressionError,
						range(
							node.start,
							node.end
						),
						f"{node.value} is not callable"
					)
					return None
		return node
	
	def power(self) -> Node:
		node = self.call()
		if node:
			while self.check_index() and self.token == TokenType.POW:
				self.i += 1
				call = self.call()
				if call:
					node = PowNode(node, call, call.start, call.end)
				else:
					self.error = True
					displayError(
						self.line,
						ErrorType.ArithmeticExpressionError,
						node.end + 1,
						"Number or expression required"
					)
					return None
		
		return node

	def factor(self) -> Node:
		"""
		Parses factors and parenthesis in token list
		"""
		if self.error:
			return None
		elif not self.check_index():
			if len(self.tokens) > 0:
				displayError(
					self.line,
					ErrorType.ArithmeticExpressionError,
					self.tokens[-1].end,
					"Missing operator"
				)
			self.error = True
			return None
		else:
			token = self.token
			if self.token == TokenType.MINUS or self.token == TokenType.PLUS:
				self.i += 1
			node = self.power()
			if node and token == TokenType.MINUS:
				node =  NegNode(node, token.start, node.end)
			
			return node

	def term(self) -> Node:
		"""
		Parses terms in token list
		"""
		node = self.factor()

		while self.check_index() and self.token.type in self.terms[0] and not self.error:
			term = self.terms[1][
				self.terms[0].index(self.token.type)
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
		while self.check_index() and self.token.type in self.expressions[0] and not self.error:
			expr = self.expressions[1][
				self.expressions[0].index(self.token.type)
			]
			self.i += 1
			term = self.term()
			if term != None:
				node = expr(node, term, node.start, term.end)
			
		return node
	
	def comparison(self) -> Node:
		expr = self.expression()
		if expr:
			if self.check_index() and self.token.type in self.comparisons[0] and not self.error:
				compType = self.comparisons[1][
					self.comparisons[0].index(self.token.type)
				]
				self.i += 1
				expr2 = self.expression()
				if expr2:
					expr = CompNode(expr, expr2, compType, expr.start, expr2.end)
				elif not self.error:
					self.error = True
					displayError(
						self.line,
						ErrorType.ArithmeticExpressionError,
						expr.end + 1,
						"Missing expression"
					)
					expr = None
		
		return expr
	
	def function_declaration(self) -> Node:
		if TokenType.AFFECT in self.tokens:
			affect_index = self.tokens.index(TokenType.AFFECT)
			affect = self.tokens[affect_index]

			function_body = self.tokens[affect_index + 1:]
			function_body = list(
				map (
					lambda token : Token(token.type, token.value, token.start - affect_index - 1),
					function_body
				)
			)

			p = Parser(function_body, self.line[affect.start + 1:])
			function_body = p.parse()
			if not p.error:
				function = self.parse_function_declaration()

				if not self.error:
					self.i = len(self.tokens)
					return FunctionDeclarationNode(
						function[0],
						function[1],
						function_body,
						self.line[affect.start + 1:],
						0,
						len(self.tokens) - 1,

					)
		else:
			return self.comparison()


	def parse(self) -> Node:
		"""Convert token list into node tree

		Returns:
			Node: Top node of the Tree
		"""
		self.i = 0
		self.tree = self.function_declaration()
		
		if self.error:
			return None
		elif self.check_index():
			displayError(
				self.line,
				ErrorType.SyntaxError,
				range(self.token.end - 1, len(self.line))
			)
		else:
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

	p = Parser([
		Token(TokenType.NUMBER, 2, 0),
		Token(TokenType.POW, "^", 1),
		Token(TokenType.NUMBER, 2, 2),
		Token(TokenType.POW, "^", 3),
		Token(TokenType.NUMBER, 2, 4),
		Token(TokenType.PLUS, "+", 5),
		Token(TokenType.NUMBER, 5, 6)
	], "2^2^2+5")
	result = p.parse()
	assert type(result) == AddNode
	assert type(result.left) == PowNode
	assert type(result.right) == NumberNode
	assert result.right.value == 5
	assert type(result.left.right) == NumberNode
	assert result.left.right.value == 2
	assert type(result.left.left) == PowNode
	assert type(result.left.left.right) == NumberNode
	assert result.left.left.right.value == 2
	assert type(result.left.left.left) == NumberNode
	assert result.left.left.left.value == 2

	from lexer import Lexer
	while True:
		line = input(">>> ")
		t = Lexer(line).tokenize()
		p = Parser(t, line)
		result = p.parse()
		if result:
			print(result)
		else:
			print("Error")