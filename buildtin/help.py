from function import Function
from functionProps import FunctionResult, ArgRange

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
			print(f"\t{arg.name} : {ArgRange.format_range(arg.arg_range)}")
	
	return FunctionResult(None)