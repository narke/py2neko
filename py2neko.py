#!/usr/bin/env python3

"""
CREDITS:
1. Parts of signature() and body() are courtesy of codegen.py
	copyright: Copyright 2008 by Armin Ronacher.
	license: BSD
	
2. py2js for inspiration
"""

import ast
from _ast import *
import sys


class Py2Neko(ast.NodeVisitor):
	
	COMPARISON_SYMBOLS = {
	    Lt    : "<",
	    Gt    : ">",
	    Eq    : "==",
	    LtE   : "<=",
	    GtE   : ">=",
	    NotEq : "!",
	    NotIn : "NOT_IMPLEMENTED",
	    In    : "NOT_IMPLEMENTED",
	    Is    : "NOT_IMPLEMENTED",
	    IsNot : "NOT_IMPLEMENTED"}
	
	BOOLEAN_OP_SYMBOLS = {
	    And : "&&",
	    Or  : "||"}
	        
	BUILTIN_FUNCTIONS = {
	    "abs"         : "abs",
	    "all"         : "NOT_IMPLEMENTED",
	    "any"         : "NOT_IMPLEMENTED",
	    "ascii"       : "NOT_IMPLEMENTED",
	    "basestring"  : "NOT_IMPLEMENTED",
	    "bin"         : "NOT_IMPLEMENTED",
	    "bool"        : "bool",
	    "bytearray"   : "NOT_IMPLEMENTED",
	    "bytes"       : "NOT_IMPLEMENTED",
	    "callable"    : "callable",
	    "chr"         : "NOT_IMPLEMENTED",
	    "classmethod" : "NOT_IMPLEMENTED",
	    "compile"     : "NOT_IMPLEMENTED",
	    "complex"     : "NOT_IMPLEMENTED",
	    "delattr"     : "NOT_IMPLEMENTED",
	    "dict"        : "NOT_IMPLEMENTED",
	    "dir"         : "NOT_IMPLEMENTED",
	    "divmod"      : "divmod",
	    "enumerate"   : "NOT_IMPLEMENTED",
	    "eval"        : "NOT_IMPLEMENTED",
	    "exec"        : "NOT_IMPLEMENTED",
	    "filter"      : "NOT_IMPLEMENTED",
	    "float"       : "float",
	    "format"      : "NOT_IMPLEMENTED",
	    "frozenset"   : "NOT_IMPLEMENTED",
	    "getattr"     : "NOT_IMPLEMENTED",
	    "globals"     : "NOT_IMPLEMENTED",
	    "hasattr"     : "NOT_IMPLEMENTED",
	    "hash"        : "NOT_IMPLEMENTED",
	    "help"        : "NOT_IMPLEMENTED",
	    "hex"         : "NOT_IMPLEMENTED",
	    "id"          : "NOT_IMPLEMENTED",
	    "input"       : "NOT_IMPLEMENTED",
	    "int"         : "int",
	    "isinstance"  : "NOT_IMPLEMENTED",
	    "issubclass"  : "NOT_IMPLEMENTED",
	    "iter"        : "NOT_IMPLEMENTED",
	    "len"         : "NOT_IMPLEMENTED",
	    "list"        : "NOT_IMPLEMENTED",
	    "locals"      : "NOT_IMPLEMENTED",
	    "map"         : "NOT_IMPLEMENTED",
	    "max"         : "max",
	    "memoryview"  : "NOT_IMPLEMENTED",
	    "min"         : "min",
	    "next"        : "NOT_IMPLEMENTED",
	    "object"      : "NOT_IMPLEMENTED",
	    "oct"         : "NOT_IMPLEMENTED",
	    "open"        : "NOT_IMPLEMENTED",
	    "ord"         : "NOT_IMPLEMENTED",
	    "pow"         : "pow",
	    "print"       : "$print",
	    "property"    : "NOT_IMPLEMENTED",
	    "range"       : "NOT_IMPLEMENTED",
	    "repr"        : "NOT_IMPLEMENTED",
	    "reversed"    : "NOT_IMPLEMENTED",
	    "round"       : "NOT_IMPLEMENTED",
	    "set"         : "NOT_IMPLEMENTED",
	    "setattr"     : "NOT_IMPLEMENTED",
	    "slice"       : "NOT_IMPLEMENTED",
	    "sorted"      : "NOT_IMPLEMENTED",
	    "staticmethod": "NOT_IMPLEMENTED",
	    "str"         : "NOT_IMPLEMENTED",
	    "sum"         : "NOT_IMPLEMENTED",
	    "super"       : "NOT_IMPLEMENTED",
	    "tuple"       : "NOT_IMPLEMENTED",
	    "type"        : "NOT_IMPLEMENTED",
	    "vars"        : "NOT_IMPLEMENTED",
	    "zip"         : "NOT_IMPLEMENTED",
	    "__import__()": "NOT_IMPLEMENTED"}
	
	BINARY_OP = {
	    'Add'      : '+',
	    'Sub'      : '-',
	    'Mult'     : '*',
	    'Div'      : '/',
	    'FloorDiv' : '/',
	    'Mod'      : '%',
	    'LShift'   : '<<',
	    'RShift'   : '>>',
	    'BitOr'    : '|',
	    'BitXor'   : '^',
	    'BitAnd'   : '&'}

	def __init__(self):
		self.code = []
		self.imported_modules = []
		

	def write_code(self, elem):

		if elem != None:
			print("WROTE:", elem)
			self.code.append(elem)

	def get_code(self):
		return self.code
		
	def get_binary_op(self, node):
		return self.BINARY_OP[node.op.__class__.__name__]
		
		

	def generic_visit(self, node):
		print(type(node).__name__)
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Num(self, node):
		print('Num :', repr(node.n))
		return node.n

	def visit_BinOp(self, node):
		print("BinOp :")	
		
		left = self.visit(node.left)
		right = self.visit(node.right)
		
		return "(%s) %s (%s)" % (left, self.get_binary_op(node), right)
		

	def visit_Str(self, node):
		print("Str :", node.s)
		
		return '"' + node.s + '"'

	def visit_Assign(self, node):
		value = self.visit(node.value)
		
		if isinstance(node.targets[0], (ast.Tuple, ast.List)):
			self.write_code("var %s = %s;" % ("id", value))
		else:
			var = self.visit(node.targets[0])
			if isinstance(node.targets[0], ast.Name):
				self.write_code("var %s = %s;" % (var, value))
		    
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Expr(self, node):
		print("Expr :")
		self.write_code(self.visit(node.value) + ";")

	def visit_Pass(self, node):
		print("Pass :")
		self.write_code(";")

	def visit_Name(self, node):
		print("Name :", node.id)
		if node.id in ("True", "False"):
			return  node.id.lower()
			
		if node.id in self.BUILTIN_FUNCTIONS.keys():
			if "builtins" not in self.imported_modules:
				self.imported_modules.append("builtins")
				self.write_code('var builtins = $loader.loadmodule("builtins",$loader);')
			return "builtins." + node.id
		return node.id


	def visit_Pow(self, node):
		print("Pow :")
		self.write_code(".__pow__(")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Store(self, node):
		print("Store :")

		ast.NodeVisitor.generic_visit(self, node)

	def visit_List(self, node):
		print("List :")
		# Is the list empty?
		if len(node.elts) == 0:
			return "$make(0);"
		# Does it contains items?
		else:
			list_elms = ", ".join([str(self.visit(elm)) for elm in node.elts])
			return "$array( %s );" % (list_elms)

	def visit_FunctionDef(self, node):
		print("FunctionDef")
		self.write_code("%s = function" % node.name)
		self.signature(node.args)
		self.write_code("{")
		self.body(node.body)
		self.write_code("}")

	def signature(self, node):
		print("Signature:")
		#print(dir(node))
		want_comma = []
		def write_comma():
			if want_comma:
				self.write_code(', ')
			else:
				want_comma.append(True)
		padding = [None] * (len(node.args) - len(node.defaults))
		# Does this function receives arguments?
		if len(node.args) == 0:
			# No
			self.write_code("()")
		else:
			self.write_code("(")
			for arg, default in zip(node.args, padding + node.defaults):
				write_comma()
				self.visit(arg)
				if default is not None:
					self.write_code('=')
					self.visit(default)
			self.write_code(")")
		if node.vararg is not None:
			write_comma()
			self.write_code('*' + node.vararg)
		if node.kwarg is not None:
			write_comma()
			self.write_code('**' + node.kwarg)

	def visit_arg(self, node):
		print("arg:", node.arg)
		self.write_code(node.arg)


	def body(self, statements):
		if hasattr(statements, '__iter__'):
			for stmt in statements:
				self.visit(stmt)
		else:
			# In some cases statements isn't iterable and
			# contains only 'print'
			self.visit(statements)

    # is this still used?
	def visit_arguments(self, node):
		print("arguments :")
		for i, item in enumerate(node.args):
			print(i, item)
			if i:
				self.write_code(",")
			ast.NodeVisitor.visit(self, item)
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Param(self, node):
		print("Param :")

	def visit_Call(self, node):

		function_name = self.visit(node.func)
		
		if function_name in self.BUILTIN_FUNCTIONS.keys():
			function_name = self.BUILTIN_FUNCTIONS[function_name]
			
		print("Called func:", function_name)
		
		if node.keywords:
			return "Call func keywords: Not implemented!"
		else:
			if node.starargs:
				pass
			elif node.kwargs:
				pass
			
			function_args = ",".join([ str(self.visit(arg)) for arg in node.args ])
			return "%s(%s)" % (function_name, function_args)
			

	def visit_Attribute(self, node):
		self.visit(node.value)
		self.write_code(node.attr)

	def visit_If(self, node):
		self.write_code("if (")
		self.visit(node.test)
		self.write_code(")")
		self.write_code("{")
		self.body(node.body)
		self.write_code("}")
		for orelse in node.orelse:
			if isinstance(orelse, If):
				self.write_code("else if (")
				self.visit(orelse.test)
				self.write_code(")")
				self.write_code("{")
				self.body(orelse.body)
				self.write_code("}")
			else:
				self.write_code("else")
				self.write_code("{")
				self.body(orelse)
				self.write_code("}")
				break


	def visit_Compare(self, node):
		for op, right in zip(node.ops, node.comparators):
			self.write_code("%s %s %s" % (self.visit(node.left), self.COMPARISON_SYMBOLS[type(op)], self.visit(right)))
	
	def visit_BoolOp(self, node):
		for i, value in enumerate(node.values):
			if i:
				self.write_code(' %s ' % self.BOOLEAN_OP_SYMBOLS[type(node.op)])
			self.visit(value)

	def visit_Return(self, node):
		self.write_code("return %s" % (self.visit(node.value)))

	def visit_For(self, node):
		for_target = self.visit(node.target)
		for_iter = self.visit(node.iter)
		self.write_code("%s = %s;" % (for_target, for_iter))
		self.write_code("__array_index__ = 0;")
		if hasattr(node.iter, "id"):
			self.write_code('while ( __array_index__ < $asize(%s) )' % (for_target))
		else:
			self.write_code('while ( __array_index__ < $asize(%s) )' % (for_target))
		self.write_code('{')
		self.body_or_else(node)
		self.write_code('__array_index__ = __array_index__ + 1;')
		self.write_code('}')

	def body_or_else(self, node):
		self.body(node.body)
		if node.orelse:
			self.write_code('else {')
			self.body(node.orelse)
			self.write_code('}')

	def visit_While(self, node):
		self.write_code("while (")
		self.visit(node.test)
		self.write_code(")")
		self.write_code("{")
		self.body_or_else(node)
		self.write_code("}")

	def visit_Break(self, node):
		self.write_code("break")

	def visit_Continue(self, node):
		self.write_code("continue")

	def visit_Delete(self, node):
		# Neko seems to not have an equivalent
		pass

	def visit_Tuple(self, node):
		print("Tuple :")
		# Is the list empty?
		if len(node.elts) == 0:
			self.write_code("$amake(0)\n")
		# Does it contains items?
		else:
			self.write_code("$array(")
			for i, item in enumerate(node.elts):
				if i:
					self.write_code(",")
				ast.NodeVisitor.visit(self, item)
			self.write_code(")\n")

	def visit_Dict(self, node):
		self.write_code("%s" % "xxxdico")
		for (key, value) in zip(node.keys, node.values):
			self.visit(key)
			k = "kkk"
			self.visit(value)
			v = "vvv"
			self.write_code("%s.__setitem__(%s, %s)\n" % (dict_name, k, v))


	def visit_Subscript(self, node):
		self.visit(node.value)
		self.write_code('%s.__getitem__(' % self.current_object_name)
		self.visit(node.slice)
		self.write_code(')')




# Writes neko code contained in a list into a file
def code2file(code):

	if len(code) == 0:
		print("Error: You must call get_code() after visiting the AST")
		return

	f = open("out.neko", "w")

	for elem in code:
		if elem in (')','}') or elem[len(elem)-1] == ';':
			f.write(elem + "\n")
		else:
			f.write(str(elem) + " ")

	f.write("\n")
	f.close()

if __name__ == '__main__':
	
	if sys.version_info < (3, 0):
		print("You need Python 3.0 or greater!")
		sys.exit()
	
	if len(sys.argv) != 2:
		print("Usage: %s <python file>" % sys.argv[0])
		sys.exit()

	try:
		f = open(sys.argv[1], "r")
		python_code = f.read()
		f.close()
	except:
		print("Error: Unable to open python file!")
		sys.exit()

	v = Py2Neko()
	node = ast.parse(python_code)
	print(ast.dump(node))
	v.visit(node)

	generated_code = v.get_code()
	code2file(generated_code)
