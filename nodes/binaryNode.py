from .node import Node

class BinaryNode(Node):
	def __init__(self, left : Node, right : Node, start: int, end : int, separator : str = ",") -> None:
		super().__init__(start, end)
		self._right = None
		self.right = right
		self._left = None
		self.left = left
		self.__separator = separator

	@property
	def right(self) -> Node:
		return self._right
	
	@right.setter
	def right(self, right : Node) -> None:
		if not self.is_node(right):
			raise TypeError("right must be a Node")
		self._right = right
	
	@property
	def left(self) -> Node:
		return self._left
	
	@left.setter
	def left(self, left : Node) -> None:
		if not self.is_node(left):
			raise TypeError("left must be a Node")
		self._left = left
	
	def __str__(self) -> str:
		return f"({self.left}{self.__separator}{self.right})"
	
	def __repr__(self) -> str:
		return self.__str__()