from function import Function
from functionProps.functionResult import FunctionResult

def help(function : Function, symbol_table):
	print(f"Help ({function.name}):")
	usage = f"Usage :\n\t{function.name}("
	for i,arg in enumerate(function.args):
		usage += f"{arg.name}"
		if i != len(function.args) - 1:
			usage += ", "
	
	usage += ")"
	print(usage)
	for arg in function.args:
		if arg.arg_range:
			print(f"\t{arg.name} : {arg.arg_range}")
	
	return FunctionResult(None)