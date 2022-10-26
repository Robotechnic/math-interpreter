from matplotlib import pyplot as plt
from _tkinter import TclError
from function import Function
from functionProps.functionResult import FunctionResult
from errorTypes import ErrorType
from nodes import NumberNode
from .floatRange import float_range

def plot2d(function : Function, x_min : int, x_max : int, y_min : int, y_max : int, step : int, symbol_table : dict) -> FunctionResult:
	if len(function.args) != 2:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"Function {function.name} must have 2 argument to be plotted")

	if x_min > x_max:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"x_min ({x_min}) must be less than x_max ({x_max})")
	
	if y_min > y_max:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"y_min ({y_min}) must be less than y_max ({y_max})")
	
	values = []
	for x in float_range(x_min, x_max, step):
		values.append([])
		for y in float_range(y_max, y_min, step):
			if function.check_arg_range(0, x) and function.check_arg_range(1, y):
				function_result = function(symbol_table, [NumberNode(x,None,None), NumberNode(y,None,None)])
				if function_result.error:
					return function_result
				if type(function_result.value) == bool:
					if function_result.value:
						values[-1].append(1)
					else:
						values[-1].append(float("nan"))
				else:
					values[-1].append(function_result.value)
			else:
				values[-1].append(float("nan"))
			
	
	plt.imshow(values, extent=[x_min, x_max, y_min, y_max], interpolation=None)
	plt.colorbar()
	plt.title(function.expression)

	try:
		plt.show()
	except TclError:
		pass

	return FunctionResult(None)