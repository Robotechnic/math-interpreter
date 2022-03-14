import re
from tokenize import Token


class Buffer:
	def __init__(self, buffer = []) -> None:
		self.buffer = buffer
		self.i = 0

	def __iter__(self) -> 'Buffer':
		return self
	
	def __next__(self) -> Token:
		if self.i < len(self.buffer):
			self.i += 1
			return self.buffer[self.i - 1]
		else:
			raise StopIteration
	
	def __len__(self) -> int:
		return len(self.buffer)
	
	def __getitem__(self, index: int) -> Token:
		return self.buffer[index]
	
	def __setitem__(self, index: int, value: Token) -> None:
		self.buffer[index] = value
	
	def append(self, value: Token) -> None:
		self.buffer.append(value)
	
	def empty(self) -> bool:
		return self.i >= len(self.buffer)
	
	def pop(self) -> str:
		if self.i < len(self.buffer):
			token = self.current()
			self.i += 1
			return token
		else:
			return None

	def current(self):
		if self.i < len(self.buffer):
			return self.buffer[self.i]
		return None
	
	def current_range(self):
		if self.i < len(self.buffer):
			return range(self.current().start, self.current().end)
		return None
	
	def clear(self) -> None:
		self.buffer = []
		self.i = 0
	
	def empty(self) -> bool:
		return self.i >= len(self.buffer)
	
	def remainds(self) -> list:
		remainds = self.buffer[self.i:]
		self.clear()
		return remainds

	def __contains__(self, value: Token) -> bool:
		return value in self.buffer
	
	def __str__(self) -> str:
		return f"Buffer({self.buffer})"
	
	def __repr__(self) -> str:
		return self.__str__()

if __name__ == "__main__":
	b = Buffer(["a","b","c"])
	print(b)
	print(b.current())
	b.append("d")
	print(b)
	try:
		print(b[10])
	except IndexError:
		print("IndexError ok")