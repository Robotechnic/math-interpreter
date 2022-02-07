from .binaryNode import BinaryNode
from .node import Node
# from .. import error

class ModNode(BinaryNode):
	def __init__(self, right : Node, left : Node, start : int, end : int) -> None:
		super().__init__(right, left, start, end, "%")
	
	def execute(self) -> tuple:
		leftValue = self.left.execute()
		rightValue = self.right.execute()
		
		if leftValue[1] != None:
			return (None, leftValue[1])
		elif rightValue[1] != None:
			return (None, rightValue[1])
		elif rightValue[0] == 0:
			return (None, "Div per 0")#error.ErrorType.ZeroDivisionError)
		else:
			return (leftValue[0] % rightValue[0], None)