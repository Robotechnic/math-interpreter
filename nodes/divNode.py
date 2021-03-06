from .binaryNode import BinaryNode
from .node import Node
from errorTypes import ErrorType
from .nodeResult import NodeResult

class DivNode(BinaryNode):
	def __init__(self, right : Node, left : Node, start : int, end : int) -> None:
		super().__init__(right, left, start, end, "/")
	
	def execute(self, left : NodeResult, right : NodeResult) -> tuple:
		if right.value == 0:
			return NodeResult(
				None,
				range(self.right.start, self.right.end),
				ErrorType.ZeroDivisionError,
				""
			)
		return NodeResult(left.value / right.value, range(self.left.start, self.right.end))