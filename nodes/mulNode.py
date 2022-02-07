from .binaryNode import BinaryNode
from .node import Node

class MulNode(BinaryNode):
	def __init__(self, right : Node, left : Node, start : int, end : int) -> None:
		super().__init__(right, left, start, end, "*")
	
	def execute(self) -> tuple:
		leftValue = self.left.execute()
		rightValue = self.right.execute()
		
		if leftValue[1] != None:
			return (None, leftValue[1])
		elif rightValue[1] != None:
			return (None, rightValue[1])
		else:
			return (leftValue[0] * rightValue[0], None)