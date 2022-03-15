
class ArgRange:
	def __init__(self, min_bound : int = None, min_included : bool = False, max_bound : int = None, max_included : bool = False) -> None:
		self.min_bound = min_bound
		self.min_included = min_included
		self.max_bound = max_bound
		self.max_included = max_included

	def check_value(self, value : int | float) -> bool:
		if not self.min_bound is None and not self.max_bound is None:
			return self.min_bound <= value <= self.max_bound
		elif not self.min_bound is None:
			return self.min_bound <= value
		elif not self.max_bound is None:
			return value <= self.max_bound
	
	def __eq__(self, other: "ArgRange") -> bool:
		if other is None:
			return False
		if type(other) == ArgRange:
			return self.range_type == other.range_type and self.min_bound == other.min_bound and self.max_bound == other.max_bound
		
		raise TypeError(f"ArgRange can't be compared to {type(other)}")
	
	def __str__(self) -> str:
		return ("[" if self.min_included else "]") + \
			   f"{self.min_bound if self.min_bound != None else '-∞'};" + \
			   f"{self.max_bound if self.max_bound != None else '∞'}" + \
			   ("]" if self.max_included else "[")
	
	def __repr__(self) -> str:
		return self.__str__()

if __name__ == "__main__":
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(5)
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(0)
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(10)
	assert not ArgRange(min_bound = 0, max_bound = 10).check_value(-1)
	assert not ArgRange(min_bound = 0, max_bound = 10).check_value(11)