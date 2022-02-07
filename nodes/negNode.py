from .unaryNode import UnaryNode
from .node import Node

class NegNode(UnaryNode):
	def __init__(self, value : Node, start : int, end : int) -> None:
		super().__init__(value, start, end, "-")
	
	def execute(self) -> tuple:
		value = self.value.execute()
		
		if value[1] != None:
			return (None, value[1])
		else:
			return (-value[0], None)