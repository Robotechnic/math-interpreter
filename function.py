from dataclasses import dataclass
from error.displayError import displayError
from nodes import Node, NodeResult
import types
from errorTypes import ErrorType
import interpreter as inter

@dataclass
class FunctionArg:
	name : str
	range : range = None

@dataclass
class FunctionResult:
	value : int | float | bool
	error : ErrorType = None

class Function:
	def __init__(self, name : str, args : list, body : Node | types.FunctionType | types.BuiltinFunctionType, expression = "") -> None:
		"""
		Function object to handle various functions in the language

		Args:
			name (str): name of the function
			args (list<FunctionArg>): list of arguments names with their range
			body (Node | types.FunctionType | types.BuiltinFunctionType): function to run when called
			expression (str): literal expression of the function
		"""
		self.name = name
		self.args = args
		self.body = body
		self.expression = expression
	
	def check_args(self, args : list) -> bool:
		"""
		Checks if the arguments passed to the function are valid

		Args:
			args (list<NodeResult>): list of arguments passed to the function

		Returns:
			bool: True if the arguments are valid, False otherwise
		"""
		return len(args) == len(self.args)

	def check_specials_ranges(slef, value : int | float, range : str) -> bool:
		if range == "pos":
			return value >= 0
		elif range == "neg":
			return value <= 0
		elif range == "pos*":
			return value > 0
		elif range == "neg*":
			return value < 0
		elif range == "notnul":
			return value != 0
	
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
			if self.args[i].range:
				in_range = True
				if type(self.args[i].range) == range:
					in_range = arg.value in self.args[i].range
				else:
					in_range = self.check_specials_ranges(arg.value, self.args[i].range)

				if not in_range:
					return False, NodeResult(
						None,
						arg.pos,
						ErrorType.DomainError,
						f"Argument {i} of function {self.name} with value {arg.value} is out of {self.args[i].range}"
					)
		
		return True, None

	def __call__(self, symbolTable : dict, args : list) -> NodeResult:
		"""
			Run the function with given arguments or interpret the function body

			Args:
				symbolTable (dict): parent symbol table
				args (list<NodeResult>): arguments to pass to the function
			
			Returns:
				NodeResult: result or error of the function
		"""
		
		check = self.check_args_range(args)
		if not check[0]:
			return check[1]

		if issubclass(type(self.body), Node):
			for i in range(len(self.args)):
				symbolTable[self.args[i].name] = args[i].value

			i = inter.Interpreter(symbolTable)
			result = i.visit_node(self.body)
			if result.error:
				displayError(
					self.expression,
					result.error,
					result.pos,
					result.message
				)
				return FunctionResult(None, result.error)
			else:
				return FunctionResult(result.value)
		else:
			args_value = list(map(lambda x: x.value, args))
			return FunctionResult(self.body(*args_value))
	
	def __str__(self) -> str:
		return f"{self.name}({', '.join(map(lambda x: x.name, self.args))}) = {self.body}"
	
	def __repr__(self) -> str:
		return self.__str__()