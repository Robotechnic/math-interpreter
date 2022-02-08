from enum import Enum, auto, unique

@unique
class ErrorType(Enum):
	SyntaxError = auto()
	ArithmeticExpressionError = auto()
	ZeroDivisionError = auto()
	MissingParentesisError = auto()
	UnexpectedTokenError = auto()
	FunctionArgumentError = auto()
