from function import Function
from functionProps.functionResult import FunctionResult

def help(function : Function, symbol_table):
	print(f"Help ({function.name}):")
	if function.description:
		print(function.description)
	usage = f"Usage :\n\t{function.name}("
	for i,arg in enumerate(function.args):
		usage += f"{arg.name}"
		if i != len(function.args) - 1:
			usage += ", "
	
	usage += ")"
	print(usage)
	for arg in function.args:
		if arg.arg_range:
			range = f"\t{arg.name}"
			for i, r in enumerate(arg.arg_range):
				range += f"{r}"
				if i != len(arg.arg_range) - 1:
					range += "∪"
			print(range)
	
	return FunctionResult(None)