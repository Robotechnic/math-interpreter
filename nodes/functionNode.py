from errorTypes import ErrorType
from nodes.nodeResult import NodeResult
from .node import Node
import function

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
			int: 0 if function is defined, 1 if function name is in symbol table but not a function, 2 otherwise
		"""
		if self.function in symbol_table:
			if isinstance(symbol_table[self.function], function.Function):
				return 0
			return 1

		return 2
	
	def execute(self, args : list, symbol_table = dict()) -> NodeResult:
		"""
		Run function call

		Args:
			args (list): list of arguments
			symbol_table (dict, optional): symbol table to use

		Returns:
			NodeResult: result of the function call
		"""
		existence = self.check_existence(symbol_table)

		if existence:
			error = f"\"{self.function}\" is not a function"
			if function == 2:
				error = f"Function \"{self.function}\" not defined"
				
			return NodeResult(
				None,
				range(self.start, self.end),
				ErrorType.FunctionNameError,
				error
			)
		
		runnedFunction = symbol_table[self.function]
		
		if not runnedFunction.check_args(args):
			return NodeResult(
				None,
				range(self.start, self.end),
				ErrorType.FunctionArgumentError,
				f"Function '{self.function}' expects {len(runnedFunction.args)} arguments ({len(self.args)} given)"
			)
		

		result = runnedFunction(symbol_table, args)
		if result.error:
			if result.error == ErrorType.DomainError:
				return result
			else:
				return NodeResult(None, range(self.start, self.end), ErrorType.FunctionError)
		else:
			return NodeResult(result.value, range(self.start, self.end))