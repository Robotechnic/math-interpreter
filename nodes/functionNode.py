from errorTypes import ErrorType
from nodes.nodeResult import NodeResult
from .node import Node

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
	
	def check_existence(self, symbol_table : dict) -> "Function":
		"""
		Check if function exists in symbol table

		Args:
			symbol_table (dict): symbol table to use

		Returns:
			Function: function if exists else None
		"""
		if self.function in symbol_table:
			return symbol_table[self.function]

		return None
	
	def execute(self, args : list, symbol_table = dict()) -> NodeResult:
		"""
		Run function call

		Args:
			args (list): list of arguments
			symbol_table (dict, optional): symbol table to use

		Returns:
			NodeResult: result of the function call
		"""
		function = self.check_existence(symbol_table)
		if not function:
			return NodeResult(
				None,
				range(self.start, self.end),
				ErrorType.FunctionNameError,
				f"Function '{self.function}' not defined"
			)
		
		if not function.check_args(args):
			return NodeResult(
				None,
				range(self.start, self.end),
				ErrorType.FunctionArgumentError,
				f"Function '{self.function}' expects {len(function.args)} arguments ({len(self.args)} given)"
			)
		

		result = function(symbol_table, args)
		if result.error:
			return NodeResult(None, range(self.start, self.end), ErrorType.FunctionError)
		else:
			return NodeResult(result.value, range(self.start, self.end))