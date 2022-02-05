from .unaryNode import UnaryNode
from .node import Node

class NegNode(UnaryNode):
	def __init__(self, value : Node):
		super().__init__(value, "-")