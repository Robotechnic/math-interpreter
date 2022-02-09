from function import Function, FunctionArg
from math import sin, cos, tan, sqrt, tan, atan, atan2, acos, asin, radians, degrees

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
			FunctionArg("x", "pos")
		],
		sqrt
	),
	"atan": Function(	
		"atan",
		[
			FunctionArg("x", range(-1, 1))
		],
		atan
	),
	"atan2": Function(
		"atan2",
		[
			FunctionArg("y", "notnul"),
			FunctionArg("x", "notnul")
		],
		atan2
	),
	"acos": Function(
		"acos",
		[
			FunctionArg("x", range(-1, 1))
		],
		acos
	),
	"asin": Function(
		"asin",
		[
			FunctionArg("x", range(-1, 1))
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
	)
}