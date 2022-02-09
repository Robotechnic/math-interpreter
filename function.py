from dataclasses import dataclass
from nodes import Node, NodeResult
import types
from errorTypes import ErrorType

@dataclass
class FunctionArg:
	name : str
	range : range = None

class Function:
	def __init__(self, name : str, args : list, body : Node | types.FunctionType | types.BuiltinFunctionType) -> None:
		"""
		Function object to handle various functions in the language

		Args:
			name (str): name of the function
			args (list<FunctionArg>): list of arguments names with their range
			body (Node | types.FunctionType | types.BuiltinFunctionType): function to run when called
		"""
		self.name = name
		self.args = args
		self.body = body
	
	def check_args(self, args : list) -> bool:
		"""
		Checks if the arguments passed to the function are valid

		Args:
			args (list<NodeResult>): list of arguments passed to the function

		Returns:
			bool: True if the arguments are valid, False otherwise
		"""
		return len(args) == len(self.args)
	
	def check_args_range(self, args : list) -> tuple:
		"""
		Checks if the arguments passed to the function are within their range

		Args:
			args (list<NodeResult>): list of arguments passed to the function

		Returns:
			tuple: (bool, list<NodeResult>): (True if the arguments are valid, list of arguments)
		"""
		
		for i in range(len(args)):
			arg = args[i]
			if self.args[i] != None:
				if arg.value in self.args[i].range:
					return False, ErrorType.DomainError
		
		return True, None

	def __call__(self, symbolTable : dict, args : list) -> NodeResult:
		"""
			Run the function with given arguments or interpret the function body

			Args:
				symbolTable (dict): parent symbol table
				args (list): arguments to pass to the function
			
			Returns:
				NodeResult: result or error of the function
		"""
		
		check = self.check_args_range(args)
		if not check[0]:
			return NodeResult(None, check[1])
		
		