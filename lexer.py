from ast import keyword
from tokens import Token, TokenType
from error import displayError, ErrorType

WHITESPACE = " \t\r"

class Lexer:
	def __init__(self, line : str) -> None:
		self.line = line
		self.i = 0
		self.decimal_count = 0
		self.tokens = []
	
	def index_valid(self) -> bool:
		"""Check if the current index is valid

		Returns:
			bool: if the current index is valid
		"""
		return self.i < len(self.line)

	def end(self) -> None:
		"""End the tokenize process"""
		self.i = len(self.line)
		self.decimal_count = 0
		self.tokens = []
	
	def is_number(self, char : str) -> bool:
		"""Check if a given character is a number bases on number token

		Args:
			char (str): char to test

		Returns:
			bool: if the char is a number
		"""
		return char in TokenType.NUMBER.value
	
	def check_decimal(self) -> bool:
		"""Check if current number has only one decimal point

		Returns:
			bool: if the number has only one decimal point
		"""
		if self.line[self.i] == TokenType.NUMBER.value[-1]:
			self.decimal_count += 1
			if self.decimal_count > 1:
				displayError(
					self.line, 
					ErrorType.ArithmeticExpressionError,
					self.i,
					"Too many decimal points"
				)
				self.end()
				return False
		
		return True
		

	def get_number(self) -> Token:
		"""Get a number token

		Returns:
			Token: number token
		"""
		number = Token(TokenType.NUMBER, self.line[self.i], self.i)
		self.decimal_count = 0
		numberEnd = False
		self.i += 1
		while self.index_valid() and not numberEnd:
			if not self.check_decimal():
				return
			elif not self.is_number(self.line[self.i]):
				numberEnd = True
			else:
				number += self.line[self.i]
				self.i += 1
		
		if self.decimal_count == 1:
			number.value = float(number.value)
		else:
			number.value = int(number.value)

		return number

	def is_keyword(self, char : str) -> bool:
		"""Check if a given char is a keyword

		Args:
			char (str): char to check

		Returns:
			bool: if the char is a keyword
		"""
		return char in TokenType.KEYWORD.value
	
	def get_keyword(self) -> str:
		"""
			Get a keyword token in the line

			Returns:
				str: keyword token
		"""
		keyword = Token(TokenType.KEYWORD, self.line[self.i], self.i)
		self.i += 1
		while self.index_valid() and self.is_keyword(self.line[self.i]):
			keyword += self.line[self.i]
			self.i += 1
		
		return keyword
	
	def is_comparison_operator(self, char : str) -> bool:
		"""Check if a given char is a comparison operator

		Args:
			char (str): char to test

		Returns:
			bool: if the char is a comparison operator
		"""
		return char in [
			TokenType.LESS,
			TokenType.EQUAL,
			TokenType.GREATER,
		]
	
	def get_comparison_operator(self) -> Token:
		if self.line[self.i] == TokenType.LESS.value:
			self.i += 1
			if self.index_valid():
				if self.line[self.i] == TokenType.EQUAL.value:
					self.i += 1
					return Token(TokenType.LESSEQUAL, "<=", self.i - 2)
				elif self.line[self.i] == TokenType.GREATER.value:
					self.i += 1
					return Token(TokenType.NOTEQUAL, "<>", self.i - 2)
				else:
					return Token(TokenType.LESS, "<", self.i - 1)
		elif self.line[self.i] == TokenType.GREATER.value:
			self.i += 1
			if self.index_valid():
				if self.line[self.i] == TokenType.EQUAL.value:
					self.i += 1
					return Token(TokenType.SUPEQUAL, ">=", self.i - 2)
				else:
					return Token(TokenType.SUP, ">", self.i - 1)
		elif self.line[self.i] == TokenType.EQUAL.value:
			self.i += 1
			return Token(TokenType.EQUAL, "=", self.i - 1)
		
			

	def get_char_type(self, char : str) -> tuple:
		"""Check if given char is valid or not

		Args:
			char (str): char to check

		Returns:
			(bool, TokenType): type of the char
		"""
		if char in WHITESPACE:
			return (True, None)
		
		for token_type in TokenType:
			if char == token_type.value[0]:
				return (True, token_type)
		
		return (False, None)
	
	def get_error_range(self) -> range:
		start = self.i
		while self.index_valid() and not self.get_char_type(self.line[self.i])[0]:
			self.i += 1
		
		return range(start, self.i)
	
	def tokenize(self) -> list:
		"""Tokenize the line

		Returns:
			list: list of token in line

		"""
		self.i = 0
		self.tokens = []
		while self.index_valid():
			c = self.line[self.i]
			
			if c in WHITESPACE:
				self.i += 1
			elif self.is_number(c):
				self.tokens.append(self.get_number())
			elif self.is_keyword(c):
				self.tokens.append(self.get_keyword())
			elif self.is_comparison_operator(c):
				self.tokens.append(self.get_comparison_operator())
			else:
				tokenExists, token_type = self.get_char_type(c)
				
				if not tokenExists:
					error_range = self.get_error_range()
					displayError(
						self.line,
						ErrorType.SyntaxError,
						error_range
					)
					self.end()
				else:
					self.tokens.append(Token(token_type, c, self.i))
					self.i += 1
		
		return self.tokens

if __name__ == "__main__":
	l = Lexer("1 + (258*3.5)")
	print(l.tokenize())
	assert l.tokenize() == [
		Token(TokenType.NUMBER, 1, 0),
		Token(TokenType.PLUS, "+", 2),
		Token(TokenType.LPAREN, "(", 4),
		Token(TokenType.NUMBER, 258, 5),
		Token(TokenType.MUL, "*", 8),
		Token(TokenType.NUMBER, 3.5, 9),
		Token(TokenType.RPAREN, ")", 12)
	]

	l = Lexer("")
	assert l.tokenize() == []