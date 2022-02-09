from errorTypes import ErrorType
from .node import Node
from .nodeResult import NodeResult

class VarNode(Node):
	def __init__(self, name, start, end) -> None:
		super().__init__(start, end)
		self.name = name
	
	def __str__(self) -> str:
		return f"(VAR {self.name})"

	def __repr__(self) -> str:
		return self.__str__()

	def execute(self, symbol_table = dict()) -> NodeResult:
		if self.name in symbol_table:
			return NodeResult(symbol_table[self.name], range(self.start, self.end))
		else:
			return NodeResult(
				None,
				range(self.start, self.end),
				ErrorType.VariableNameError,
				f"Undefined variable '{self.name}'"
			)