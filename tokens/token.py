from enum import Enum, unique
from lib2to3.pgen2.token import EQUAL
import string
from .tokenErrors import *

@unique
class TokenType(str, Enum):
	NUMBER = "0123456789." #last char is decimal separator
	KEYWORD = string.ascii_lowercase + NUMBER
	PLUS = "+"
	MINUS = "-"
	MUL = "*"
	DIV = "/"
	MOD = "%"
	POW = "^"
	COMMA = ","
	EQUAL = "="
	FACT = "!"
	LPAREN = "("
	RPAREN = ")"


class Token:
	"""
	This class represents a token in the input text.
	"""
	def __init__(self, type : TokenType, value : str, start : int) -> None:
		"""Token constructor

		Args:
			type (TokenType): type of the token
			value (str): value taken by the token
			start (int): start of the token for error reporting
		"""
		self.checkTokenType(type)
		self._type = type
		self._value = value
		self._start = 0
		self.start = start
	
	@property
	def value(self) -> str:
		return self._value
	
	@value.setter
	def value(self, value : str) -> None:
		self._value = value
		self.end = self.start + len(str(value))

	@property
	def type(self) -> TokenType:
		return self._type
	
	@type.setter
	def type(self, type : TokenType) -> None:
		self.checkTokenType(type)
		self._type = type

	@property
	def start(self) -> int:
		return self._start
	
	@start.setter
	def start(self, start : int) -> None:
		self._start = start
		self.end = self.start + len(str(self.value))

	def checkTokenType(self, token_type : TokenType) -> None:
		"""Check if a given value is a TokenType and if it is valid
		tokentype value.

		Args:
			token_type (TokenType): value to test

		Raises:
			TokenTypeError: If the value is not a TokenType
			TokenTypeError: If the value is not a valid TokenType
		"""
		if type(token_type) != TokenType:
			raise TokenTypeError(message=f"{token_type} is not a TokenType")
		if not token_type in TokenType:
			raise TokenTypeError(message=f"{token_type} is not a valid TokenType")
	
	def check_if_mergeable(self, token : "Token") -> None:
		"""Check if two tokens can be merged.

		Args:
			token (Token): token to merge with this token

		Raises:
			MergingError: if the tokens cannot be merged
		"""
		if token.start != self.end:
			raise MergingError(self, token)
		
		if token.type != self.type:
			raise TokenTypeError(self, token)
	
	def __add__(self, token) -> "Token":
		"""Merge two tokens or add a string to the token

		Args:
			token (Token | str): token to merge with this token or a string to add

		Raises:
			TypeError: if the token is not a Token or a string

		Returns:
			Token: the resulting token after the merge
		"""
		if type(token) == Token:
			self.check_if_mergeable(token)
			return Token(self.type, self.value + token.value, self.start)
		elif type(token) == str:
			return Token(self.type, self.value + token, self.start)
		else:
			raise TypeError(f"Cannot add {type(token)} to {type(self)}")
	
	def __iadd__(self, token) -> "Token":
		"""Merge token with this token or add a string to the token

		Args:
			token (Token | str): token to merge with this token or a string to add

		Raises:
			TypeError: if the token is not a Token or a string

		Returns:
			Token: the resulting token after the merge
		"""
		if type(token) == Token:
			self.check_if_mergeable(token)
			self.value += token.value
		elif type(token) == str:
			self.value += token
		else:
			raise TypeError(f"Cannot add {type(token)} to {type(self)}")

		return self
	
	def __eq__(self, other : "Token") -> bool:
		"""Check if two tokens are equal

		Args:
			other (Token): token to compare to this token

		Returns:
			bool: True if the tokens are equal, False otherwise
		"""
		return self.type == other.type and self.value == other.value and self.start == other.start

	def __str__(self):
		return f"({self.type.name}, {self.value}, {self.start})"
	
	def __repr__(self):
		return self.__str__()


# test error handling
if __name__ == "__main__":
	first = Token(TokenType.NUMBER, "1", 0)
	second = Token(TokenType.PLUS, "2", 1)
	third = Token(TokenType.NUMBER, "3", 2)
	fourth = Token(TokenType.NUMBER, "4", 1)
	fifth = Token(TokenType.NUMBER, "5", 3)

	result = False
	print("Testing MergingError")
	try:
		first + third
	except MergingError as e:
		result = True
		print(e)
	
	assert result, "MergingError not raised"

	result = False
	print("Testing TokenTypeError")
	try:
		first + second
	except TokenTypeError as e:
		result = True
		print(e)
	
	assert result, "TokenTypeError not raised"

	result = False
	print("Testing TokenTypeError with invalid type")
	try:
		test = Token(None, "1", 0)
	except TokenTypeError as e:
		result = True
		print(e)
	
	assert result, "TokenTypeError not raised"


	third += fifth
	assert third.value == "35", "Token value not updated"
	assert third.start == 2, "Token start is modified"
	assert third.end == 4, "Token end not updated"
	assert third.type == TokenType.NUMBER, "Token modified"

	fifth += "6"
	assert fifth.value == "56", "Token value not updated"
	assert fifth.start == 3, "Token start is modified"
	assert fifth.end == 5, "Token end not updated"
	assert fifth.type == TokenType.NUMBER, "Token modified"