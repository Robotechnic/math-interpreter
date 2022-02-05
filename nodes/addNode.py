from .binaryNode import BinaryNode
from .node import Node

class AddNode(BinaryNode):
	def __init__(self, right : Node, left : Node) -> None:
		super().__init__(right, left, "+")