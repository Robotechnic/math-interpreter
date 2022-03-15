from functionProps.functionResult import FunctionResult
from nodes import NumberNode
from errorTypes import ErrorType
from .floatRange import float_range

def integral(f, min, max, step, symbol_table):
	if len(f.args) != 1:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"Function {f.name} must have 1 argument to be integrated")
	
	if min > max:
		return FunctionResult(None, ErrorType.FunctionArgumentError, f"min ({min}) must be less than max ({max})")

	result = 0
	for i in float_range(min, max, step):
		if f.check_arg_range(0, i):
			result += f(symbol_table, [NumberNode(i,None,None)]).value
		else:
			result += 0
		
	result *= (max - min) * step
	
	return FunctionResult(result)