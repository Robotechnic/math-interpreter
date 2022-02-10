from enum import Enum

class StringRanges(str, Enum):
	pos = "pos"
	neg = "neg"
	pos_ = "pos*"
	neg_ = "neg*"
	notnul = "notnul"

	def check_range(self, value : int | float) -> bool:
		if self.value == "pos":
			return value >= 0
		elif self.value == "neg":
			return value <= 0
		elif self.value == "pos*":
			return value > 0
		elif self.value == "neg*":
			return value < 0
		elif self.value == "notnul":
			return value != 0

class ArgRange:
	def __init__(self, range_type : StringRanges = None, min_bound : int = None, max_bound : int = None):
		self.range_type = range_type
		if not range_type:
			if not min_bound and not max_bound:
				raise ValueError("ArgRange: min_bound or max_bound must be specified")
			
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
	
	def __str__(self) -> str:
		if self.range_type:
			return self.range_type
		else:
			return f"[{self.min_bound or '-inf'};{self.max_bound or 'inf'}]"