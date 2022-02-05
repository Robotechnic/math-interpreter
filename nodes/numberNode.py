from .node import Node

class NumberNode(Node):
	def __init__(self, value : int) -> None:
		self._value = None
		self.value = value
	
	@property
	def value(self) -> int | float:
		return self._value
	
	@value.setter
	def value(self, value : int | float) -> None:
		if not isinstance(value, (int, float)):
			raise TypeError("value must be int or float")
		self._value = value
	
	def __str__(self) -> str:
		return f"{str(self.value)}"
	
	def __repr__(self) -> str:
		return f"{str(self)}"