from .node import Node
from math import cos, sin, tan, sqrt, pow, acos, asin, atan, atan2

FUNCTION = {
	"sin": (sin,1),
	"cos": (cos,1),
	"tan": (tan,1),
	"sqr": (sqrt,1),
	"pow": (pow,2),
	"acos": (acos,1),
	"asin": (asin,1),
	"atan": (atan,1),
	"atan2": (atan2, 2)
}

class FunctionNode(Node):
	def __init__(self, function : str, nodes : list, start : int, end : int) -> None:
		super().__init__(start, end)
		self.function = function
		self.nodes = nodes
	
	@staticmethod
	def is_valid(function : str) -> bool:
		return function in FUNCTION.keys()
	
	@staticmethod
	def check_args(function : str, args : int) -> bool:
		return FUNCTION[function][1] == args
	
	@staticmethod
	def get_args(function : str) -> int:
		return FUNCTION[function][1]

	def __repr__(self) -> tuple:
		args_str = ""
		for i, node in enumerate(self.nodes):
			args_str += str(node)
			if i < len(self.nodes) - 1:
				args_str += ", "
		return f"(FUNCTION {self.function}({args_str}))"
	
	def __str__(self) -> str:
		return self.__repr__()
	
	def execute(self) -> float:
		args = []
		for node in self.nodes:
			result = node.execute()
			if result[1]:
				return (None, result[1])
			args.append(result[0])
		
		return (FUNCTION[self.function](*args), None)