from functionProps.functionResult import FunctionResult
from nodes import NumberNode
from errorTypes import ErrorType
from .floatRange import float_range

def sum_func(function, min, max, step, symbol_table):
	if len(function.args) != 1:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"Function {function.name} must have 1 argument to be summed")
	
	if min > max:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"min ({min}) must be less than max ({max})")

	result = 0
	for i in float_range(min, max, step):
		if function.check_arg_range(0, i):
			result += function(symbol_table, [NumberNode(i,None,None)]).value
		else:
			result += 0
	
	return FunctionResult(result)

def sum_val(val, min, max, step, symbol_table):
	return FunctionResult(val * (max - min) / step)

def sum(function, min, max, step, symbol_table):
	if isinstance(function, int) or isinstance(function, float):
		return sum_val(function, min, max, step, symbol_table)
	else:
		return sum_func(function, min, max, step, symbol_table)