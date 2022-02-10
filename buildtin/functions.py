from functionProps import FunctionArg, ArgRange
from function import Function
from math import sin, cos, tan, sqrt, tan, atan, atan2, acos, asin, radians, degrees
from .plot import plot

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
			FunctionArg("x", ArgRange("pos*"))
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
			FunctionArg("x", ArgRange("notnull")),
			FunctionArg("y", ArgRange("notnull"))
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
		radians
	),
	"deg": Function(
		"deg",
		[
			FunctionArg("x")
		],
		degrees
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
			FunctionArg("step")
		],
		plot
	)
}