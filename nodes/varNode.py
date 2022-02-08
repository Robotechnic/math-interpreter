from .node import Node

class VarNode(Node):
	def __init__(self, name, start, end) -> None:
		super().__init__(start, end)
		self.name = name
	
	def __str__(self) -> str:
		return f"(VAR {self.name})"

	def __repr__(self) -> str:
		return self.__str__()

	def execute(self, symbol_table = dict()) -> float:
		if self.name in symbol_table:
			return (symbol_table[self.name], None)
		else:
			return (0, "Undefined variable '{}'".format(self.name))