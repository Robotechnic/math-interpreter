from errorTypes import ErrorType
from dataclasses import dataclass


@dataclass
class NodeResult:
	value : int | float | bool
	pos : int | range
	error : ErrorType = None
	message : str = ""