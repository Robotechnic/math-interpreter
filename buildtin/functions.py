from functionProps import FunctionArg, ArgRange
from function import Function
from math import sin, cos, tan, sqrt, tan, atan, atan2, acos, asin, radians, degrees, factorial, log, log10, exp
from .plot import plot
from .plot2d import plot2d
from .help import help
from .sum import sum
from .integral import integral

functions = {
	"sin": Function(
		"sin", 
		[
			FunctionArg("x")
		],
		sin
	),
	"cos": Function(
		"cos",
		[
			FunctionArg("x")
		],
		cos
	),
	"tan": Function(
		"tan",
		[
			FunctionArg("x")
		],
		tan
	),
	"sqrt": Function(
		"sqrt",
		[
			FunctionArg("x", ArgRange(0, False))
		],
		sqrt
	),
	"atan": Function(	
		"atan",
		[
			FunctionArg("x")
		],
		atan
	),
	"atan2": Function(
		"atan2",
		[
			FunctionArg("x", [ArgRange(None, False, 0, False), ArgRange(0, False)]),
			FunctionArg("y", [ArgRange(None, False, 0, False), ArgRange(0, False)])
		],
		atan2
	),
	"acos": Function(
		"acos",
		[
			FunctionArg("x", ArgRange(min_bound=-1, max_bound=1))
		],
		acos
	),
	"asin": Function(
		"asin",
		[
			FunctionArg("x", ArgRange(min_bound=-1, max_bound=1))
		],
		asin
	),
	"rad": Function(
		"rad",
		[
			FunctionArg("x")
		],
		radians,
		description = "Convert angles from degrees to radians"
	),
	"deg": Function(
		"deg",
		[
			FunctionArg("x")
		],
		degrees,
		description = "Convert angles from radians to degrees"
	),
	"abs": Function(
		"abs",
		[
			FunctionArg("x")
		],
		abs
	),
	"plot": Function(
		"plot",
		[
			FunctionArg("function"),
			FunctionArg("min"),
			FunctionArg("max"),
			FunctionArg("step", ArgRange(0, False))
		],
		plot,
		description = "Plot a function in a graph between min and max and with a precision of step"
	),
	"plot2d": Function(
		"plot2d",
		[
			FunctionArg("function"),
			FunctionArg("x_min"),
			FunctionArg("y_min"),
			FunctionArg("x_max"),
			FunctionArg("y_max"),
			FunctionArg("step", ArgRange(0, False))
		],
		plot2d,
		description = "Plot a two arguments function into a 2d graph with x between x_min and x_max and y between y_min and y_max, precision is given by step"
	),
	"help": Function(
		"help",
		[
			FunctionArg("function")
		],
		help,
		description = "Display this help message"
	),
	"factorial": Function(
		"factorial",
		[
			FunctionArg("x", ArgRange(0, True))
		],
		factorial,
		description = "Calculate factorial value of a number"
	),
	"ln": Function (
		"ln",
		[
			FunctionArg("x",ArgRange(0, False))
		],
		log10,		
	),
	"log": Function(
		"log",
		[
			FunctionArg("x", ArgRange(0,False)),
			FunctionArg("base", ArgRange(0,False))
		],
		log
	),
	"exp": Function(
		"exp",
		[
			FunctionArg("x")
		],
		exp
	),
	"sum": Function(
		"sum",
		[
			FunctionArg("function"),
			FunctionArg("min"),
			FunctionArg("max"),
			FunctionArg("step", ArgRange(0, False))
		],
		sum,
		description = "Sum the value of a function between min and max with a precision of step"
	),
	"integral": Function(
		"integral",
		[
			FunctionArg("function"),
			FunctionArg("min"),
			FunctionArg("max"),
			FunctionArg("step", ArgRange(0, False, 1, False))
		],
		integral,
		description = "Calculate the integral of a function between min and max with a precision of step"
	)
}
