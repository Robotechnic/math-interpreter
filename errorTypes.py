from enum import Enum, auto, unique

@unique
class ErrorType(Enum):
	SyntaxError = auto()
	UnexpectedTokenError = auto()
	MissingParentesisError = auto()

	ArithmeticExpressionError = auto()
	ZeroDivisionError = auto()
	DomainError = auto()

	FunctionArgumentError = auto()
	FunctionNameError = auto()
	FunctionError = auto()
	
	VariableNameError = auto()
	UnsupportedNode = auto()