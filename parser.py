from operator import le
from typing import Callable

from numpy import cumprod
from nodes import *
from error import displayError
from tokens import Token, TokenType
from errorTypes import ErrorType
from functionProps import FunctionArg, ArgRange, StringRanges
from buffer import Buffer


OPERATOR_CHAIN = [
	{
		TokenType.EQUAL: CompNode(ComparisionType.EQUAL),
		TokenType.NOTEQUAL: CompNode(ComparisionType.NOTEQUAL),
		TokenType.LESS: CompNode(ComparisionType.LESS),
		TokenType.LESSEQUAL: CompNode(ComparisionType.LESSEQUAL),
		TokenType.GREATER: CompNode(ComparisionType.GREATER),
		TokenType.GREATEREQUAL: CompNode(ComparisionType.GREATEREQUAL)
	},
	{
		TokenType.PLUS: AddNode,
		TokenType.MINUS: SubNode
	},
	{
		TokenType.MUL: MulNode,
		TokenType.DIV: DivNode,
		TokenType.MOD: ModNode
	},
	{
		TokenType.POW: PowNode
	}
]


class Parser:
	"""
	A class that parses a list of tokens and interprets them
	"""
	def __init__(self, tokens : list, line : str) -> None:
		self._tokens = Buffer()
		self.tokens = tokens
		self.line = line

		self.tree = None
		
		self.error = False
	

	@property
	def tokens(self) -> list:
		return self._tokens
	
	@tokens.setter
	def tokens(self, tokens : list) -> None:
		self._tokens.clear()
		for t in tokens:
			if type(t) != Token:
				raise TypeError("tokens must be a list of Token objects")
			self._tokens.append(t)

	def missing_operator_error(self) -> None:
		self.error = True
		displayError(
			self.line,
			ErrorType.ArithmeticExpressionError,
			self.buffer.currentRange(),
			"Missing operator"
		)
	
	def get_arg_range_bound(self) -> int | float:
		"""
		Return range bound of a range
		"""
		if self.tokens.current() in [TokenType.SEMICOLON, TokenType.RBRACKET]:
			self.tokens.pop()
			return None
		
		bound = self.parse_operators(0)
		if self.error:
			return None
		if not bound:
			self.error = True
			displayError(
				self.line,
				ErrorType.SyntaxError,
				self.tokens.current().start,
				"Missing range bound"
			)
		
		if isinstance(bound, NumberNode):
			return bound.value
		elif isinstance(bound, NegNode) and isinstance(bound.value, NumberNode):
			return -bound.value.value
		
		self.error = True
		displayError(
			self.line,
			ErrorType.UnexpectedTokenError,
			bound.start,
			"Range bounds must be numbers"
		)
		return None
		
	
	def get_range_min_bound(self) -> int | float:
		min_bound = self.get_arg_range_bound()
		if self.error:
			return None

		if self.tokens.pop() != TokenType.SEMICOLON:
			self.error = True
			displayError(
				self.line,
				ErrorType.SyntaxError,
				self.tokens.current().start,
				"Missing semicolon"
			)
			return None

		return min_bound
	
	def get_range_max_bound(self) -> int | float:
		max_bound = self.get_arg_range_bound()
		if self.error:
			return None
		return max_bound
	
	def parse_args_range_bounds(self) -> ArgRange:
		min_bound = self.get_range_min_bound()
		max_bound = self.get_range_max_bound()
		
		if self.error or (min_bound is None and max_bound is None):
			return None
		
		return ArgRange(min_bound = min_bound, max_bound = max_bound)

	def parse_arg_range(self) -> list:
		"""
		Parse all ranges applied to a function argument

		Returns:
			list<ArgRange>: list of all ranges
		"""
		result = []
		while self.tokens.current() == TokenType.LBRACKET:
			self.tokens.pop()
			bounds =  self.parse_args_range_bounds()
			if self.error:
				return None
			if not bounds:
				self.error = True
				displayError(
					self.line,
					ErrorType.ArithmeticExpressionError,
					self.tokens.current().start,
					"Missing range"
				)
				return None	

			if self.tokens.current() != TokenType.RBRACKET:
				self.error = True
				displayError(
					self.line,
					ErrorType.MissingParentesisError,
					self.tokens.current().start,
					"Missing closing bracket"
				)
				return None
			
			self.tokens.pop()
			result.append(bounds)

		return result
	
	def parse_function_declaration_arg(self) -> FunctionArg:
		"""
		Parse function declaration argument
		Get name and validity ranges
		
		Returns:
			FunctionArg: parsed argument
		"""
		arg = self.parse_operators(0)
		if not arg:
			return None
		if not isinstance(arg, VarNode):
			self.error = True
			displayError(
				self.line,
				ErrorType.UnexpectedTokenError,
				range(arg.start, arg.end),
				"Function arguments must be variables"
			)
			return None

		arg_range = self.parse_arg_range()
		if self.error:
			return None
		
		return FunctionArg(arg.name, arg_range, arg.start, arg.end)
	
	def parse_function_call_arg(self) -> Node:
		return self.parse_operators(0)

	def parse_function_args(self, arg_parse : Callable) -> list:
		"""
		Parse function aguments

		Args:
			arg_parse (Callable): function to parse arguments

		Returns:
			list: list of processed arguments
		"""
		args = []
		while not self.tokens.empty() and \
			  self.tokens.current() != TokenType.RPAREN:

			if self.tokens.current() == TokenType.COMMA:
				self.tokens.pop()
			
			arg = arg_parse()
			if arg is None:
				return None
			args.append(arg)
			
			
		if self.tokens.pop() != TokenType.RPAREN:
			self.error = True
			displayError(
				self.line,
				ErrorType.MissingParentesisError,
				self.tokens.current().end,
				"Missing closing parenthesis"
			)
			return None

		return args
	
	def parse_function_declaration(self) -> tuple:
		"""
		Parse function declaration: get name and arguments of the function

		Returns:
			tuple: function name and function args
		"""
		if self.tokens.current() != TokenType.KEYWORD:
			self.error = True
			displayError(
				self.line,
				ErrorType.UnexpectedTokenError,
				range(self.tokens.current().start, self.tokens.current().end),
				"Function name expected"
			)
			return None

		function_name = self.tokens.pop().value
		if self.tokens.pop() != TokenType.LPAREN:
			self.error = True
			displayError(
				self.line,
				ErrorType.FunctionDeclarationError,
				self.tokens.current().end,
				"Opening parenthesis expected"
			)
			return None
		
		function_args = self.parse_function_args(self.parse_function_declaration_arg)
		if self.error:
			return None

		if function_args is not None:
			self.tokens.pop() # pass = character
			return function_name, function_args

		return None
	
	def parse_function_body(self) -> Node:
		"""
		Convert remaining tokens into function body

		Returns:
			Node: Body of the function
		"""
		body = self.tokens.remainds()
		if not body:
			return None
		
		start = body[0].start
		for token in body:
			token.start -= start
		
		p = Parser(body, self.line[start:])
		node = p.parse_operators(0)
		if p.error:
			self.error = True
			return None
		
		if not p.tokens.empty():
			self.error = True
			displayError(
				self.line,
				ErrorType.SyntaxError,
				range(p.tokens.current().start + start, len(self.line)),
				"Unexpected token"
			)
		
		return node, self.line[start:]

	def manage_parenthesis(self) -> Node:
		node = self.parse_operators(0)
		if self.tokens.current() == TokenType.RPAREN:
			self.tokens.pop()
			return node
		
		else:
			self.error = True
			displayError(
				self.line,
				ErrorType.MissingParentesisError,
				self.tokens.current().start,
				"Closing parenthesis expected"
			)
			return None
	
	def call(self, node) -> Node:
		if self.tokens.current() == TokenType.LPAREN:
			if not self.tokens.pop():
				return None
			if isinstance(node, VarNode):
				args = self.parse_function_args(self.parse_function_call_arg)
				if args:
					return FunctionNode(node.name, args, node.start, args[-1].end)
			
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

	def atom(self) -> Node:
		"""
		Parse atomic expression: number, variable, function call, parenthesis

		Returns:
			Node: atomic node or None if error
		"""
		token = self.tokens.pop()
		
		if token == TokenType.LPAREN:
			node = self.manage_parenthesis()

		elif token == TokenType.NUMBER:
			node = NumberNode(
				token.value,
				token.start,
				token.end
			)

		elif token == TokenType.KEYWORD:
			node = VarNode(
				token.value,
				token.start,
				token.end
			)
		else:
			self.error = True
			displayError(
				self.line, 
				ErrorType.UnexpectedTokenError, 
				range(token.start, token.end),
				f"Number or oppening parenthesis expected, got {token.value}"
			)
			return None

		return self.call(node)
			

	def parse_operators(self, level : int, acc : Node = None) -> Node:
		"""
		Parses expressions in token list

		Args:
			level(int): index of operators to parse
			acc(Node): Accumulator node
		
		Returns:
			Node: Node representing parsed expression
		"""
		if self.error:
			return acc

		if level >= len(OPERATOR_CHAIN):
			return self.atom()

		if acc is None:
			acc = self.parse_operators(level + 1)
			if self.error:
				return acc
		
		if not self.tokens.empty() and self.tokens.current().type in OPERATOR_CHAIN[level]:
			op = self.tokens.pop()
			if self.tokens.empty():
				return displayError(
					self.line,
					ErrorType.ArithmeticExpressionError,
					self.tokens.current().end,
					"Missing number or expression"
				)

			right_elem = self.parse_operators(level + 1)
			if right_elem is None or self.error:
				self.error = True
				return None

			return self.parse_operators(
				level,
				OPERATOR_CHAIN[level][op.type](acc, right_elem, acc.start, right_elem.end)
			)
		
		return acc

	def function_declaration(self) -> Node:
		if TokenType.AFFECT in self.tokens:
			start = self.tokens.current().start
			declaration =  self.parse_function_declaration()
			if self.error:
				return None
			body = self.parse_function_body()
			if self.error:
				return None
			if body is None:
				displayError(
					self.line,
					ErrorType.FunctionDeclarationError,
					len(self.line) - 1,
					"Missing function body"
				)
				return None
			return FunctionDeclarationNode(declaration[0], declaration[1], body[0], body[1], start, body[0].end)
		else:
			return self.parse_operators(0)

	def parse(self) -> Node:
		"""Convert token list into node tree

		Returns:
			Node: Top node of the Tree
		"""
		self.i = 0
		self.tree = self.function_declaration()

		if self.error:
			return None
		elif self.tokens.current():
			displayError(
				self.line,
				ErrorType.SyntaxError,
				range(self.tokens.current().end, len(self.line))
			)
		else:
			return self.tree


def test():
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

if __name__ == "__main__":
	test()
	print("All tests passed")

	from lexer import Lexer
	while True:
		line = input(">>> ")
		t = Lexer(line).tokenize()
		if len(t) == 0:
			print("Error")
			continue
		p = Parser(t, line)
		result = p.parse()
		if result:
			print(result)
		else:
			print("Error")