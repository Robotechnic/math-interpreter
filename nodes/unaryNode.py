from .node import Node

class UnaryNode(Node):
	def __init__(self, value : Node, start : int, end : int, prefix = "") -> None:
		super().__init__(start, end)
		self._value = None
		self.value = value
		self.__prefix = prefix
	
	@property
	def value(self) -> Node:
		return self._value
	
	@value.setter
	def value(self, value : Node) -> None:
		if not self.is_node(value):
			raise TypeError("value must be a Node")
		self._value = value
	
	def __str__(self) -> str:
		return self.__prefix + str(self.value)
	
	def __repr__(self) -> str:
		return self.__str__()