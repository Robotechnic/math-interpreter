class Node:
	def __init__(self) -> None:
		pass

	def is_node(self, node : "Node") -> bool:
		return issubclass(type(node),Node) or type(node) == Node

	