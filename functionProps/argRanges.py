from enum import Enum

class StringRanges(str, Enum):
	pos = "pos"
	neg = "neg"
	pos_ = "pos*"
	neg_ = "neg*"
	notnull = "notnull"

	def check_range(self, value : int | float) -> bool:
		if self.value == "pos":
			return value >= 0
		elif self.value == "neg":
			return value <= 0
		elif self.value == "pos*":
			return value > 0
		elif self.value == "neg*":
			return value < 0
		elif self.value == "notnull":
			return value != 0

class ArgRange:
	def __init__(self, range_type : StringRanges = None, min_bound : int = None, max_bound : int = None):
		if not range_type:
			self.range_type = range_type
			if not min_bound and not max_bound:
				raise ValueError("ArgRange: min_bound or max_bound must be specified")
		else:
			self.range_type = StringRanges(range_type)
			
		self.min_bound = min_bound
		self.max_bound = max_bound

	def check_value(self, value : int | float) -> bool:
		if self.range_type:
			return self.range_type.check_range(value)
		elif not self.min_bound is None and not self.max_bound is None:
			return self.min_bound <= value <= self.max_bound
		elif not self.min_bound is None:
			return self.min_bound <= value
		elif not self.max_bound is None:
			return value <= self.max_bound
	
	def __eq__(self, other: "ArgRange") -> bool:
		if type(other) == ArgRange:
			return self.range_type == other.range_type and self.min_bound == other.min_bound and self.max_bound == other.max_bound
		else:
			return False
	
	def __str__(self) -> str:
		if self.range_type:
			return self.range_type
		else:
			return f"[{self.min_bound if self.min_bound != None else '-inf'};" + \
				   f"{self.max_bound if self.max_bound != None else 'inf'}]"

	def __repr__(self) -> str:
		return self.__str__()

if __name__ == "__main__":
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(5)
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(0)
	assert ArgRange(min_bound = 0, max_bound = 10).check_value(10)
	assert not ArgRange(min_bound = 0, max_bound = 10).check_value(-1)
	assert not ArgRange(min_bound = 0, max_bound = 10).check_value(11)
	
	assert not ArgRange(StringRanges.notnull).check_value(0)
	assert ArgRange(StringRanges.notnull).check_value(1)
	assert ArgRange(StringRanges.notnull).check_value(-1)

	assert ArgRange(StringRanges.pos).check_value(1)
	assert not ArgRange(StringRanges.pos).check_value(-1)
	assert ArgRange(StringRanges.pos).check_value(0)

	assert ArgRange(StringRanges.neg).check_value(-1)
	assert not ArgRange(StringRanges.neg).check_value(1)
	assert ArgRange(StringRanges.neg).check_value(0)

	assert ArgRange(StringRanges.pos_).check_value(1)
	assert not ArgRange(StringRanges.pos_).check_value(0)
	assert not ArgRange(StringRanges.pos_).check_value(-1)

	assert ArgRange(StringRanges.neg_).check_value(-1)
	assert not ArgRange(StringRanges.neg_).check_value(0)
	assert not ArgRange(StringRanges.neg_).check_value(1)

