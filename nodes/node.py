class Node:
	def __init__(self, start, end) -> None:
		self.start = start
		self.end = end

	def is_node(self, node : "Node") -> bool:
		return issubclass(type(node),Node) or type(node) == Node

	