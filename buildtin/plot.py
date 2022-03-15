from _tkinter import TclError
from matplotlib import pyplot as plt
from errorTypes import ErrorType
from function import Function
from functionProps.functionResult import FunctionResult
from nodes import NumberNode
from .floatRange import float_range

def plot(function : Function, min : int, max : int, step : int, symbol_table : dict) -> FunctionResult:
	if len(function.args) != 1:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"Function {function.name} must have 1 argument to be plotted")
	
	if min > max:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"min ({min}) must be less than max ({max})")
	
	x_values = []
	y_values = []
	for x in float_range(min, max + 1, step):
		x_values.append(x)
		if function.check_arg_range(0, x):
			y_values.append(function(symbol_table, [NumberNode(x, None, None)]).value)
		else:
			y_values.append(float("nan"))
			
	plt.plot(x_values, y_values)
	plt.title(function.expression)
	
	try:
		plt.show()
	except TclError:
		pass

	return FunctionResult(None)