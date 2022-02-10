from dataclasses import dataclass
from errorTypes import ErrorType

@dataclass
class FunctionResult:
	value : int | float | bool
	error : ErrorType = None
	message : str = ""