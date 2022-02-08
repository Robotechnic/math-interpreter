from .node import Node
from math import cos, sin, tan, sqrt, pow, acos, asin, atan, atan2, log

FUNCTION = {
	"sin": (sin,1),
	"cos": (cos,1),
	"tan": (tan,1),
	"sqr": (sqrt,1),
	"pow": (pow,2),
	"acos": (acos,1),
	"asin": (asin,1),
	"atan": (atan,1),
	"atan2": (atan2, 2),
	"abs": (abs,1),
	"log": (log,1)
}

class FunctionNode(Node):
	def __init__(self, function : str, args : list, start : int, end : int) -> None:
		super().__init__(start, end)
		self.function = function
		self.args = args

	def __repr__(self) -> tuple:
		args_str = ""
		for i, node in enumerate(self.args):
			args_str += str(node)
			if i < len(self.args) - 1:
				args_str += ", "
		return f"(FUNCTION {self.function}({args_str}))"
	
	def __str__(self) -> str:
		return self.__repr__()
	
	def check_existence(self, symbol_table : dict) -> tuple:
		if self.function in symbol_table:
			return symbol_table[self.function]
		elif self.function in FUNCTION:
			return FUNCTION[self.function]
		return None
	
	def execute(self, symbol_table = dict()) -> float:
		function = self.check_existence(symbol_table)
		if not function:
			return (0, f"Function '{self.function}' not defined")
		
		if len(self.args) != function[1]:
			return (0, f"Function '{self.function}' expected {function[1]} arguments, but {len(self.args)} where given")

		args = []
		for node in self.args:
			result = node.execute()
			if result[1]:
				return (None, result[1])
			args.append(result[0])
		
		return (FUNCTION[self.function](*args), None)