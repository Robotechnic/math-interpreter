from .binaryNode import BinaryNode
from .node import Node

class MulNode(BinaryNode):
	def __init__(self, right : Node, left : Node) -> None:
		super().__init__(right, left, "*")