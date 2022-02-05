class MergingError(Exception):
	"""
	Error when trying to merge two tokens which are not adjacent
	"""
	def __init__(self, baseToken : "Token", mergedToken : "Token"):
		self.baseToken = baseToken
		self.mergedToken = mergedToken
	
	def __str__(self) -> str:
		return f"Token {self.baseToken} which end at {self.baseToken.end} does not follow {self.mergedToken} which starts at {self.mergedToken.start}"
	
	def __repr__(self) -> str:
		return self.__str__()

class TokenTypeError(Exception):
	"""
	Error when trying to merge two tokens which are not same type
	or set invalid token type
	"""
	def __init__(self, baseToken = None, mergedToken = None, message = "") -> None:
		self.baseToken = baseToken
		self.mergedToken = mergedToken
		self.message = message
	
	def __str__(self) -> str:
		if self.message:
			return self.message
		else:
			return f"Token {self.baseToken} has a different type than {self.mergedToken}"
	
	def __repr__(self) -> str:
		return self.__str__()