#!/usr/bin/env python

"""
The MIT License

Copyright (c) 2011 Konstantin Tcholokachvili

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
CREDITS:
Parts of signature() and body() are courtesy of codegen.py
copyright: Copyright 2008 by Armin Ronacher.
license: BSD

TODO:
- Generate uniq internal names for no named variables
- Remove the junk code "var1 = var2" generated for for loops
- Make tuple immutable
"""

import ast
from _ast import *
import sys
#TODO
sys.argv.append("test_suit/binop.py")
COMPARISON_SYMBOLS = {
    Lt:".__lt__(",
    Gt:".__gt__(",
    Eq:".__eq__(",
    LtE:".__le__(",
    GtE:".__ge__(",
    NotEq:".__ne__(",
    NotIn:"NOT_IMPLEMENTED",
    In:"NOT_IMPLEMENTED",
    Is:"NOT_IMPLEMENTED",
    IsNot:"NOT_IMPLEMENTED"
}

BOOLEAN_OP_SYMBOLS = {
    And:"&&",
    Or:"||"
}

BUILTIN_FUNCTIONS = {
    "abs":"NOT_IMPLEMENTED",
    "all":"NOT_IMPLEMENTED",
    "any":"NOT_IMPLEMENTED",
    "ascii":"NOT_IMPLEMENTED",
    "basestring":"NOT_IMPLEMENTED",
    "bin":"NOT_IMPLEMENTED",
    "bool":"NOT_IMPLEMENTED",
    "bytearray":"NOT_IMPLEMENTED",
    "bytes":"NOT_IMPLEMENTED",
    "callable":"NOT_IMPLEMENTED",
    "chr":"NOT_IMPLEMENTED",
    "classmethod":"NOT_IMPLEMENTED",
    "compile":"NOT_IMPLEMENTED",
    "complex":"NOT_IMPLEMENTED",
    "delattr":"NOT_IMPLEMENTED",
    "dict":"NOT_IMPLEMENTED",
    "dir":"__dir__",
    "divmod":"NOT_IMPLEMENTED",
    "enumerate":"NOT_IMPLEMENTED",
    "eval":"NOT_IMPLEMENTED",
    "exec":"NOT_IMPLEMENTED",
    "filter":"NOT_IMPLEMENTED",
    "float":"NOT_IMPLEMENTED",
    "format":"NOT_IMPLEMENTED",
    "frozenset":"NOT_IMPLEMENTED",
    "getattr":"NOT_IMPLEMENTED",
    "globals":"NOT_IMPLEMENTED",
    "hasattr":"NOT_IMPLEMENTED",
    "hash":"NOT_IMPLEMENTED",
    "help":"NOT_IMPLEMENTED",
    "hex":"NOT_IMPLEMENTED",
    "id":"NOT_IMPLEMENTED",
    "input":"NOT_IMPLEMENTED",
    "int":"NOT_IMPLEMENTED",
    "isinstance":"NOT_IMPLEMENTED",
    "issubclass":"NOT_IMPLEMENTED",
    "iter":"NOT_IMPLEMENTED",
    "len":"__len__",
    "list":"NOT_IMPLEMENTED",
    "locals":"NOT_IMPLEMENTED",
    "map":"NOT_IMPLEMENTED",
    "max":"NOT_IMPLEMENTED",
    "memoryview":"NOT_IMPLEMENTED",
    "min":"NOT_IMPLEMENTED",
    "next":"NOT_IMPLEMENTED",
    "object":"NOT_IMPLEMENTED",
    "oct":"NOT_IMPLEMENTED",
    "open":"NOT_IMPLEMENTED",
    "ord":"NOT_IMPLEMENTED",
    "pow":"NOT_IMPLEMENTED",
    "print":"$print",
    "property":"NOT_IMPLEMENTED",
    "range":"NOT_IMPLEMENTED",
    "repr":"NOT_IMPLEMENTED",
    "reversed":"NOT_IMPLEMENTED",
    "round":"NOT_IMPLEMENTED",
    "set":"NOT_IMPLEMENTED",
    "setattr":"NOT_IMPLEMENTED",
    "slice":"NOT_IMPLEMENTED",
    "sorted":"NOT_IMPLEMENTED",
    "staticmethod":"NOT_IMPLEMENTED",
    "str":"NOT_IMPLEMENTED",
    "sum":"NOT_IMPLEMENTED",
    "super":"NOT_IMPLEMENTED",
    "tuple":"NOT_IMPLEMENTED",
    "type":"NOT_IMPLEMENTED",
    "vars":"NOT_IMPLEMENTED",
    "zip":"NOT_IMPLEMENTED",
    "__import__()":"NOT_IMPLEMENTED"
}

nb_tmp_var = 0
tmp_vars_list = []

def get_tmp_var_name():
	global nb_tmp_var
	global tmp_vars_list

	nb_tmp_var = nb_tmp_var + 1
	tmp_var_name = "tmp" + str(nb_tmp_var)
	tmp_vars_list.append(tmp_var_name)

	return tmp_var_name


def helper_create_object(var_type, var_name):

	allowed_types = ("int", "str", "list", "dict")

	if var_type not in allowed_types:
		return None

	ret_str = "var %s = $new(null)\n" % var_name
	ret_str = ret_str + "$objsetproto(%s, %s)\n" % (var_name, var_type)
	return ret_str

def helper_create_tmp_var(var_type, val):
	var_name = get_tmp_var_name()
	return var_name, helper_create_object(var_type, var_name)


def helper_store(var_type, var_name):

	ret_str = None
	if var_type == "str":
		ret_str = "%s = " % var_name
	elif var_type == "int":
		ret_str = "%s.numerator = " % var_name
	return ret_str

class Py2Neko(ast.NodeVisitor):

	def __init__(self):
		self.code = []
		self.in_for_loop = False
		self.no_named_list = False

		self.current_object_name = ""
		self.current_object_type = ""
		self.objects = {}
		self.in_comparators = False
		self.in_func_def = False
		self.do_create_var = True
		self.in_call = False
		self.method_call = False
		self.display_val = False
		self.values_in_binop = []

	def dump_flags(self):
		print("in_for_loop = %s" % self.in_for_loop)
		print("in_comparators = %s" % self.in_comparators)
		print("in_func_def = %s" % self.in_func_def)
		print("do_create_var = %s" % self.do_create_var)
		print("in_call = %s" % self.in_call)
		print("method_call = %s" % self.method_call)
		print("display_val = %s" % self.display_val)

	def write_code(self, elem):

		if elem != None:
			print("WROTE:", elem)
			self.code.append(elem)

	def get_code(self):
		return self.code

	def generic_visit(self, node):
		print(type(node).__name__)
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Num(self, node):
		print('Num :', repr(node.n))
		if self.in_comparators:
			# value for comparison and the end parenthesis
			self.write_code("%s)" % repr(node.n))
		elif self.do_create_var or self.in_call:
			self.write_code("%s;" % repr(node.n))

		self.current_object_name = repr(node.n)

	def visit_BinOp(self, node):
		print("BinOp :", node.left, node.right)
		
		def get_node_value(node):
			if isinstance(node, ast.Num):
				val = node.n
			elif isinstance(node, ast.Dict):
				print("Not implemented!")
				val = None
			elif isinstance(node, ast.List):
				print("Not implemented!")
				val = None
			elif isinstance(node, ast.Name):
				print("Not implemented!")
				val = None
			elif isinstance(node, ast.Set):
				print("Not implemented!")
				val = None
			elif isinstance(node, ast.Str):
				print("Not implemented!")
				val = None
			elif isinstance(node, ast.Tuple):
				print("Not implemented!")
				val = None
			
			return val
		
		if isinstance(node.op, ast.Add):
			if isinstance(node.left, ast.BinOp):
				# The left node is itself a binary operation
				ast.NodeVisitor.visit(self, node.left)
			else:
				left_node_value = get_node_value(node.left)
				right_node_value = get_node_value(node.right)
				self.write_code("%s.__add__(%s)" % (left_node_value, right_node_value))

	def visit_Str(self, node):
		print("Str :", node.s)

		if self.display_val:
			self.write_code('"' + node.s + '"')
		# for dict
		self.current_object_name = repr(node.s)
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Assign(self, node):
		print("Assign :", node.value)
		self.do_create_var = True
		if 'n' in dir(node.value):
			self.current_object_type = "int"
		elif 's' in dir(node.value):
			self.current_object_type = "str"

		ast.NodeVisitor.generic_visit(self, node)
		self.do_create_var = False

	def visit_Expr(self, node):
		print("Expr :")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Pass(self, node):
		print("Pass :")
		self.write_code(";")

	def visit_Name(self, node):
		print("Name :", node.id)

		self.current_object_name = node.id

		if self.in_call:
			try:
				if node.id in BUILTIN_FUNCTIONS.keys():
					if node.id == "print":
						#self.method_call = True
						print("XXX-FUNC: %s" % BUILTIN_FUNCTIONS[node.id])
						self.write_code("%s" % BUILTIN_FUNCTIONS[node.id])
					else:
						# method's call go here
						print("YYY-FUNC: %s." % BUILTIN_FUNCTIONS[node.id])
						self.write_code("%s." % BUILTIN_FUNCTIONS[node.id])
			except KeyError:
				pass

		# Create an object
		# The name shoudn't be a built-in functions names
		elif node.id not in BUILTIN_FUNCTIONS.keys():
			print("DBG:",self.current_object_name)
			# Avoid name conflict by excluding duplicated names
			if self.current_object_name not in self.objects.keys():
				print("DBG2:",self.current_object_name, self.current_object_type)
				var_declare = helper_create_object(self.current_object_type, self.current_object_name)
				if var_declare != None:
					self.write_code("%s" % var_declare)
					# keep track of this variable
					# CAUTION: type isn't always known
					self.objects[self.current_object_name] = self.current_object_type
					print("DECLARED_OBJECTS", self.objects)
		elif (self.display_val and not self.in_cmp) or self.do_create_var:
			self.write_code("%s" % node.id)
		elif self.display_val and self.in_cmp:
			self.write_code("%s" % node.id)
		# function's parameter
		elif self.in_call:
			print("AZERTY")
			self.write_code(node.id)
		elif node.id in self.objects.keys():
			if self.method_call:
				self.write_code(node.id + ".")
			elif self.in_call:
				self.write_code(node.id)

		#self.dump_flags()

		if self.no_named_list:
			self.write_code("nonamedlist")
		elif node.id == "True":
			self.write_code("true")
		elif node.id == "False":
			self.write_code("false")

		self.method_call = False
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Add(self, node):
		print("Add :")
		self.write_code(".__add__(")

	def visit_Sub(self, node):
		print("Sub :")
		self.write_code(".__sub__(")

	def visit_Mult(self, node):
		print("Mult :")
		self.write_code(".__mul__(")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Pow(self, node):
		print("Pow :")
		self.write_code(".__pow__(")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Div(self, node):
		print("Div :")
		self.write_code(".__truediv__(")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_FloorDiv(self, node):
		print("FloorDiv :")
		self.write_code(".__floordiv__(")
		ast.NodeVisitor.generic_visit(self, node)

	def visit_Store(self, node):
		print("Store :")
		result = helper_store(self.current_object_type, self.current_object_name)

		self.write_code(result)
		ast.NodeVisitor.generic_visit(self, node)

	def visit_List(self, node):
		print("List :")
		# Is the list empty?
		if len(node.elts) == 0:
			s = helper_create_object("list", self.current_object_name)
			self.write_code(s)
		# Does it contains items?
		else:
			self.do_create_var = False
			list_declaration = helper_create_object("list", self.current_object_name)
			self.write_code(list_declaration)
			self.write_code("$array(")
			for i, item in enumerate(node.elts):
				if i:
					self.write_code(",")
				ast.NodeVisitor.visit(self, item)
			self.write_code(")")
			self.do_create_var = True

	def visit_FunctionDef(self, node):
		print("FunctionDef")
		self.in_func_def = True
		self.write_code("%s = function" % node.name)
		self.signature(node.args)
		self.in_func_def = False
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
			self.in_call = True
			self.write_code("(")
			for arg, default in zip(node.args, padding + node.defaults):
				write_comma()
				self.visit(arg)
				if default is not None:
					self.write_code('=')
					self.visit(default)
			self.write_code(")")
			self.in_call = False
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
		print("Call:")
		self.in_call = True

		self.visit(node.func)
		self.write_code("(")

		nb_args = len(node.args)
		self.do_create_var = False
		for i, arg in enumerate(node.args):
			self.visit(arg)
			if i < nb_args - 1:
				self.write_code(",")

		self.do_create_var = True

		self.write_code(")")
		self.in_call = False

	def visit_Attribute(self, node):
		self.method_call = True
		self.visit(node.value)
		self.write_code(node.attr)
		self.method_call = False

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
		self.in_cmp = True
		self.display_val = True
		self.visit(node.left)
		self.in_comparators = True
		self.do_create_var = False
		self.display_val = True
		for op, right in zip(node.ops, node.comparators):
			self.write_code(' %s ' % COMPARISON_SYMBOLS[type(op)])
			self.visit(right)
		self.in_cmp = False
		self.in_comparators = False
		self.do_create_var = True
		self.display_val = False

	def visit_BoolOp(self, node):
		for i, value in enumerate(node.values):
			if i:
				self.write_code(' %s ' % BOOLEAN_OP_SYMBOLS[type(node.op)])
			self.visit(value)

	def visit_Return(self, node):
		self.write_code("return")
		self.visit(node.value)

	def visit_For(self, node):
		if not hasattr(node.iter, "id"):
			self.no_named_list = True
		self.visit(node.target)
		self.in_for_loop = True
		self.visit(node.iter)
		var_declare = helper_create_object("int", node.target.id)
		self.write_code("%s" % var_declare)
		self.write_code("%s.numerator = 0;" % node.target.id)
		if hasattr(node.iter, "id"):
			self.write_code('while ( %s.__lt__(%s.__len__()) )' % (node.target.id, node.iter.id))
		else:
			self.write_code('while ( %s.__lt__(%s.__len__()) )' % (node.target.id, "nonamedlist"))
			self.no_named_list = False
		self.write_code('{')
		self.body_or_else(node)
		self.write_code('%s = %s.__add__(1)' % (node.target.id, node.target.id))
		self.write_code('}')
		self.in_for_loop = False

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
		if not self.in_for_loop:
			self.write_code("break")

	def visit_Continue(self, node):
		if not self.in_for_loop:
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
		self.do_create_var  = False
		self.display_val = False
		dict_name = self.current_object_name
		var_declare = helper_create_object("dict", dict_name)
		self.write_code("%s" % var_declare)
		for (key, value) in zip(node.keys, node.values):
			self.visit(key)
			k = self.current_object_name
			self.visit(value)
			v = self.current_object_name
			self.write_code("%s.__setitem__(%s, %s)\n" % (dict_name, k, v))
		self.do_create_var  = True
		self.display_val = True

	def visit_Subscript(self, node):
		self.do_create_var  = False
		self.visit(node.value)
		self.write_code('%s.__getitem__(' % self.current_object_name)
		self.visit(node.slice)
		self.write_code(')')
		self.do_create_var  = True




# Writes neko code contained in a list into a file
def code2file(code):

	if len(code) == 0:
		print("Error: You must call get_code() after visiting the AST")
		return

	f = open("out.neko", "w")

	for elem in code:
		if elem in [')','}'] or elem[len(elem)-1] == ';':
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
