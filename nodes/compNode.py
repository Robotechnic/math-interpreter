import imp
from lib2to3.pgen2.token import NOTEQUAL
from .binaryNode import BinaryNode
from .node import Node
from enum import Enum, auto

class ComparisionType(Enum):
	EQUAL = auto()
	NOTEQUAL = auto()
	LESS = auto()
	GREATER = auto()
	LESSEQUAL = auto()
	GREATEREQUAL = auto()

class ComparisonTypeError(Exception):
	pass

class CompNode(BinaryNode):
	def __init__(self, left : Node, right : Node, type : ComparisionType, start : int, end : int) -> None:
		super().__init__(left, right, start, end)
		self._type = None
		self.type = type
	
	@property
	def type(self) -> ComparisionType:
		return self._type
	
	@type.setter
	def type(self, comparison_type : ComparisionType) -> None:
		if type(comparison_type) != ComparisionType:
			raise ComparisonTypeError(message=f"{comparison_type} is not a ComparisionType")
		if not comparison_type in ComparisionType:
			raise ComparisonTypeError(message=f"{comparison_type} is not a valid ComparisionType")
		self._type = comparison_type
	
	def process(self) -> bool:
		"""Compare value of the child nodes based on the comparision type

		Returns:
			bool: the comparision reslt
		"""
		left = self.left.process()
		right = self.right.process()
		if left[1]:
			return (None, left[1])
		elif right[1]:
			return (None, right[1])
		elif self.type == ComparisionType.EQUAL:
			return (left[0] == right[0], None)
		elif self.type == ComparisionType.NOTEQUAL:
			return (left[0] != right[0], None)
		elif self.type == ComparisionType.LESS:
			return (left[0] < right[0], None)
		elif self.type == ComparisionType.GREATER:
			return (left[0] > right[0], None)
		elif self.type == ComparisionType.LESSEQUAL:
			return (left[0] <= right[0], None)
		elif self.type == ComparisionType.GREATEREQUAL:
			return (left[0] >= right[0], None)
	
	def __str__(self) -> str:
		return f"{self.left} {self.type.name} {self.right}"

	def __repr__(self) -> str:
		return self.__str__()
