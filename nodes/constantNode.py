from math import pi, e, tau
from .node import Node

class ConstantNode(Node):
	def __init__(self, value) -> None:
		super().__init__()
		self.value = value
	
	def is_valid(self) -> bool:
		return self.value in ["pi", "e", "tau"]
