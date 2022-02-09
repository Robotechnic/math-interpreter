from errorTypes import ErrorType
from dataclasses import dataclass


@dataclass
class NodeResult:
	value : int | float | bool
	error : ErrorType = None
	message : str = None
	pos : int | range = None