from math import pi, e, tau
from .node import Node

CONSTANTS = {
	"pi": pi,
	"e": e,
	"tau": tau
}

class ConstantNode(Node):
	def __init__(self, value, start, end) -> None:
		super().__init__(start, end)
		self.value = value
	
	@staticmethod
	def is_valid(value) -> bool:
		return value in CONSTANTS.keys()
	
	def __repr__(self) -> tuple:
		return f"(CONST {self.value})"

	def execute(self) -> float:
		return (CONSTANTS[self.value], None)