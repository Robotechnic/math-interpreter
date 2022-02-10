from .node import Node

class FunctionDeclarationNode(Node):
	def __init__(self, name : str, args : list, body : Node, expression : str, start : int, end : int) -> None:
		super().__init__(start, end)
		self.name = name
		self.args = args
		self.body = body
		self.expression = expression
	
	def __str__(self) -> str:
		return f"({self.name}({', '.join(list(map(lambda x : x.name, self.args)))}) = {self.body})"