from .binaryNode import BinaryNode
from .node import Node
from .nodeResult import NodeResult

class PowNode(BinaryNode):
	def __init__(self, right : Node, left : Node, start : int, end : int) -> None:
		super().__init__(right, left, start, end, "^")
	
	def execute(self, left : NodeResult, right : NodeResult) -> tuple:
		return NodeResult(left.value ** right.value)