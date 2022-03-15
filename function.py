import types
from error.displayError import displayError
from nodes import Node, NodeResult
from errorTypes import ErrorType
from functionProps import FunctionResult
import interpreter as inter

class Function:
	def __init__(self, name : str, args : list, body : Node | types.FunctionType | types.BuiltinFunctionType, expression = "", description="") -> None:
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
		self.description = description
	
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
			if self.args[i].arg_range:
				in_range = self.args[i].check_arg_range(arg.value)

				if not in_range:
					return False, NodeResult(
						None,
						arg.pos,
						ErrorType.DomainError,
						f"Argument {i} of function {self.name} with value {arg.value} is out of {self.args[i].arg_range}"
					)
		
		return True, None
	
	def check_arg_range(self, arg_index : int, arg_value : int | float | bool) -> bool:
		if self.args[arg_index].arg_range:
			return self.args[arg_index].check_arg_range(arg_value)
		else:
			return True

	def __call__(self, symbol_table : dict, args : list) -> NodeResult:
		"""
			Run the function with given arguments or interpret the function body

			Args:
				symbol_table (dict): parent symbol table
				args (list<NodeResult>): arguments to pass to the function
			
			Returns:
				NodeResult: result or error of the function
		"""
		check = self.check_args_range(args)
		if not check[0]:
			return check[1]

		if issubclass(type(self.body), Node):
			symbol_table = symbol_table.copy()
			for i in range(len(self.args)):
				symbol_table[self.args[i].name] = args[i].value

			i = inter.Interpreter(symbol_table)
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
			if isinstance(self.body, types.BuiltinFunctionType):
				return FunctionResult(self.body(*args_value))
			else:
				return self.body(*args_value, symbol_table)
	
	def __str__(self) -> str:
		return f"{self.name}({', '.join(map(lambda x : str(x), self.args))}) = {self.body}"
	
	def __repr__(self) -> str:
		return self.__str__()