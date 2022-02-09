from errorTypes import ErrorType
from function import Function, FunctionArg
from nodes import Node, BinaryNode, UnaryNode, NumberNode, VarNode, FunctionNode, NodeResult
from lexer import Lexer
from parser import Parser
from error import displayError
from buildtin import buildtin_symbol_table

class Interpreter:
	def __init__(self, symbol_table = dict()) -> None:
		if not symbol_table:
			self.symbol_table = buildtin_symbol_table
		else:
			self.symbol_table = symbol_table

		self.init_parse()
	
	def init_parse(self) -> None:
		"""
		Reset parser variables to interpret a new line
		"""
		self.line = ""
		self.tokens = []
		self.tree = None
		self.finished = False

	def convert_into_tokens(self) -> None:
		"""
		Convert current line into tokens
		"""
		self.tokens = Lexer(self.line).tokenize()
		if not self.tokens:
			self.finished = True
	
	def parse_tokens(self) -> None:
		"""
		Convert token list into a executable tree
		"""
		p = Parser(self.tokens, self.line)
		self.tree = p.parse()
		if not self.tree:
			self.finished = True
	
	def visit_binary_node(self, node : BinaryNode) -> NodeResult:
		"""
		Take a binary node and process it

		Args:
			node (BinaryNode): node to process

		Returns:
			NodeResult: result of the process
		"""
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
		"""
		Take a unary node and process it

		Args:
			node (UnaryNode): node to process

		Returns:
			NodeResult: result of the process
		"""
		value = self.visit_node(node.value)
		if value.error:
			self.finished = True
			return value
			
		return node.execute(value)

	def visit_function_node(self, node : FunctionNode) -> NodeResult:
		"""
		Take a function node, process arguments and process function

		Args:
			node (FunctionNode): node to process

		Returns:
			NodeResult: result of the process
		"""
		args = []
		for arg in node.args:
			arg_result = self.visit_node(arg)
			if arg_result.error:
				self.finished = True
				return arg_result
			
			args.append(arg_result)
		
		return node.execute(args, self.symbol_table)

	def visit_node(self, node : Node) -> NodeResult:
		"""
		Visit a node process it and return the result

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
			return node.execute(self.symbol_table)
		elif issubclass(node_type, FunctionNode):
			return self.visit_function_node(node)
			
		return NodeResult(
			None,
			range(node.start, node.end),
			ErrorType.UnsupportedNode,
			"Unknown node type",
		)

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