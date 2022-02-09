from nodes import Node, BinaryNode, UnaryNode, NumberNode, VarNode, FunctionNode, NodeResult
from lexer import Lexer
from parser import Parser
from error import displayError

class Interpreter:
	def __init__(self) -> None:
		self.symbolTable = {}
		self.init_parse()
	
	def init_parse(self) -> None:
		"""
		Reset parser variables to interpret a new line
		"""
		self.line = ""
		self.tokens = []
		self.tree = None
		self.finished = False

	def convert_into_tokens(self) -> list:
		self.tokens = Lexer(self.line).tokenize()
		if not self.tokens:
			self.finished = True
	
	def parse_tokens(self) -> None:
		"""Convert token list into a executable tree
		"""
		p = Parser(self.tokens, self.line)
		self.tree = p.parse()
		if not self.tree:
			self.finished = True
	
	def visit_binary_node(self, node : BinaryNode) -> NodeResult:
		left = self.visit_node(node.left)
		if left.error:
			self.finished = True
			return left
			
		right = self.visit_node(node.right)
		if right.error:
			self.finished = True
			return right
		
		return node.execute(left, right)
	
	def visit_unary_node(self, node : UnaryNode) -> NodeResult:
		value = self.visit_node(node.value)
		if value.error:
			self.finished = True
			return value
			
		return node.execute(value)

	def visit_function_node(self, node : FunctionNode) -> NodeResult:
		args = []
		for arg in node.args:
			arg_result = self.visit_node(arg)
			if arg_result.error:
				self.finished = True
				return arg_result
			
			args.append(arg_result.value)
		
		return node.execute(args, self.symbolTable)

	def visit_node(self, node : Node) -> NodeResult:
		"""
		Visit a node and return the result

		Args:
			node (Node): node to visit

		Returns:
			
		"""
		node_type = type(node)
		if issubclass(node_type, BinaryNode):
			return self.visit_binary_node(node)
		elif issubclass(node_type, UnaryNode):
			return self.visit_unary_node(node)
		elif issubclass(node_type, NumberNode):
			return node.execute()
		elif issubclass(node_type, VarNode):
			return node.execute(self.symbolTable)
		elif issubclass(node_type, FunctionNode):
			return self.visit_function_node(node)
			
		return 0

	def evaluate(self, line : str) -> None:
		"""Convert line into tree and evaluate it

		Args:
			line (str): line to evaluate
		"""
		self.init_parse()

		self.line = line
		self.convert_into_tokens()
		if self.finished:
			return
		
		self.parse_tokens()
		if self.finished:
			return
		
		result = self.visit_node(self.tree)

		if result.error:
			displayError(self.line, result.error, result.pos, result.message)
			return ""
		elif self.finished:
			return ""
		else:
			return result.value