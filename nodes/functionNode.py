from errorTypes import ErrorType
from nodes.nodeResult import NodeResult
from .node import Node
from math import cos, sin, tan, sqrt, pow, acos, asin, atan, atan2, log

FUNCTIONS = {
	"sin": (sin,1),
	"cos": (cos,1),
	"tan": (tan,1),
	"sqrt": (sqrt,1),
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
		elif self.function in FUNCTIONS:
			return FUNCTIONS[self.function]
		return None
	
	def execute(self, args : list, symbol_table = dict()) -> NodeResult:
		function = self.check_existence(symbol_table)
		if not function:
			return NodeResult(
				None, 
				ErrorType.FunctionNameError,
				f"Function '{self.function}' not defined",
				range(self.start, self.end)
			)
		
		if len(args) != function[1]:
			return NodeResult(
				None,
				ErrorType.FunctionArgumentError,
				f"Function '{self.function}' expects {function[1]} arguments ({len(self.args)} given)",
				range(self.start, self.end)
			)
		

		return NodeResult(
			function[0](*args)
		)