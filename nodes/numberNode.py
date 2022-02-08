from .node import Node
from .nodeResult import NodeResult

class NumberNode(Node):
	def __init__(self, value : int, start : int, end : int) -> None:
		super().__init__(start, end)
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
	
	
	def execute(self) -> tuple:
		return NodeResult(self.value)
	
	def __str__(self) -> str:
		return f"{str(self.value)}"
	
	def __repr__(self) -> str:
		return f"{str(self)}"