from .argRanges import ArgRange

class FunctionArg:
	def __init__(self, name : str, arg_range : ArgRange = None, start : int = 0, end : int = 0) -> None:
		self.name = name
		self._range = None
		self.arg_range = arg_range
		self.start = start
		self.end = end
	
	@property
	def arg_range(self) -> range | ArgRange:
		return self._range
	
	@arg_range.setter
	def arg_range(self, arg_range : range | ArgRange) -> None:
		if arg_range != None:
			if type(arg_range) == ArgRange:
				self._range = arg_range
			else:
				raise TypeError(f"range must be a range or ArgRange, not {type(arg_range)}")
	
	def __str__(self) -> str:
		return f"{self.name}({self.arg_range})"
	
	def __repr__(self) -> str:
		return self.__str__()

if __name__ == "__main__":
	assert FunctionArg("a", 0, 1, ArgRange(min_bound = 0, max_bound = 1)).arg_range == ArgRange(min_bound = 0, max_bound = 1)
	assert FunctionArg("b",0,1,ArgRange("pos*")).arg_range == ArgRange("pos*")
	print(FunctionArg("c",0,1,ArgRange("pos")))