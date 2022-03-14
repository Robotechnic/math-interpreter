from matplotlib import pyplot as plt
from _tkinter import TclError
from function import Function
from functionProps.functionResult import FunctionResult
from errorTypes import ErrorType
from nodes import NumberNode


def float_range(min, max, step = 1):
	if max < min:
		min, max = max, min
	while min < max:
		yield min
		min += step

def plot2d(function : Function, x_min : int, x_max : int, y_min : int, y_max : int, step_x : int, step_y : int, symbol_table : dict) -> FunctionResult:
	if len(function.args) != 2:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"Function {function.name} must have 2 argument to be plotted")
	
	values = []
	for x in float_range(x_min, x_max, step_x):
		values.append([])
		for y in float_range(y_max, y_min, step_y):
			if function.check_arg_range(0, x) and function.check_arg_range(1, y):
				function_result = function(symbol_table, [NumberNode(x,None,None), NumberNode(y,None,None)]).value
				if type(function_result) == bool:
					if function_result:
						values[-1].append(1)
					else:
						values[-1].append(float("nan"))
				else:
					values[-1].append(function_result)
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