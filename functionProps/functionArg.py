from .argRanges import ArgRange

class FunctionArg:
	def __init__(self, name : str, start : int, end : int, arg_range : range | ArgRange = None) -> None:
		self.name = name
		self._range = None
		self.arg_range = arg_range
		self.start = start
		self.end = end
	
	@property
	def arg_range(self) -> range | ArgRange:
		return self._range
	
	@arg_range.setter
	def arg_range(self, value : range | ArgRange) -> None:
		if value is not None:
			if type(value) == range or type(value) == ArgRange:
				self._range = value
			else:
				raise TypeError(f"range must be a range or ArgRange, not {type(value)}")
		else:
			value = None