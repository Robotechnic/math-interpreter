from nodes.nodeResult import NodeResult
from .unaryNode import UnaryNode
from .node import Node
from .nodeResult import NodeResult

class NegNode(UnaryNode):
	def __init__(self, value : Node, start : int, end : int) -> None:
		super().__init__(value, start, end, "-")
	
	def execute(self, value : NodeResult) -> tuple:
		return NodeResult(-value.value)