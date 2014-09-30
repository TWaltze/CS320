#####
# Tyler Waltze
# CS 320
# HW2
#####

from math import log, floor
import re

def number(tokens, top = True):
	if re.match(r"^(0|(-?[1-9][0-9]*))$", tokens[0]):
		return (int(tokens[0]), tokens[1:])

def variable(tokens, top = True):
	# Exclude reserved words from variable list
	if re.match(r"^(true|false)$", tokens[0]):
		return None

	if re.match(r"^([a-z])+([a-zA-Z0-9])*$", tokens[0]):
		return (tokens[0], tokens[1:])

def variableWrapped(tokens, top = True):
	v = variable(tokens, top)

	return ({"Variable": [v[0]]}, v[1])

def formula(tmp, top = True):
	seqs = [\
		("Xor", [formulaLeft, "xor", formula]), \
		("Left", [formulaLeft]) \
		]

	# Try each choice sequence.
	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = [] # To store matched terminals.
		es = [] # To collect parse trees from recursive calls.

		# Walk through the sequence and either
		# match terminals to tokens or make
		# recursive calls depending on whether
		# the sequence entry is a terminal or
		# parsing function.
		for x in seq:
			if type(x) == type(""): # Terminal.

				if tokens and tokens[0] == x: # Does terminal match token?
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break # Terminal did not match token.

			else: # Parsing function.

				# Call parsing function recursively
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]

		# Check that we got either a matched token
		# or a parse tree for each sequence entry.
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				if label == "Left":
					return (es[0], tokens)
				else:
					return ({label:es} if len(es) > 0 else label, tokens)


def formulaLeft(tmp, top = True):
	seqs = [\
		("True", ["true"]), \
		("False", ["false"]), \
		("Not", ["not", "(", formula, ")"]), \
		("Parens", ["(", formula, ")"]), \
		("Variable", [variable]) \
		]

	# Try each choice sequence.
	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = [] # To store matched terminals.
		es = [] # To collect parse trees from recursive calls.

		# Walk through the sequence and either
		# match terminals to tokens or make
		# recursive calls depending on whether
		# the sequence entry is a terminal or
		# parsing function.
		for x in seq:
			if type(x) == type(""): # Terminal.

				if tokens and tokens[0] == x: # Does terminal match token?
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break # Terminal did not match token.

			else: # Parsing function.

				# Call parsing function recursively
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]

		# Check that we got either a matched token
		# or a parse tree for each sequence entry.
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				return ({label:es} if len(es) > 0 else label, tokens)

def term(tmp, top = True):
	seqs = [\
		("Plus", [factor, "+", term]), \
		("Factor", [factor]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens and tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				if label == "Factor":
					return (es[0], tokens)
				else:
					return ({label:es} if len(es) > 0 else label, tokens)

def factor(tmp, top = True):
	seqs = [\
		("Mult", [factorLeft, "*", factor]), \
		("Left", [factorLeft,]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens and tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				if label == "Left":
					return (es[0], tokens)
				else:
					return ({label:es} if len(es) > 0 else label, tokens)

def factorLeft(tmp, top = True):
	seqs = [\
		("Log", ["log", "(", factor, ")"]), \
		("Parens", ["(", formula, ")"]), \
		("Variable", [variable]), \
		("Number", [number]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens and tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				return ({label:es} if len(es) > 0 else label, tokens)

def program(tmp, top = True):
	seqs = [\
		("Print", ["print", expression, ";", program]), \
		("Assign", ["assign", variableWrapped, ":=", expression, ";", program]), \
		("If", ["if", expression, "{", program, "}", program]), \
		("While", ["while", expression, "{", program, "}", program]), \
		("End", []) \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens and tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				return ({label:es} if len(es) > 0 else label, tokens)

def expression(tmp, top = True):
	seqs = [\
		("Formula", [formula]), \
		("Term", [term]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens and tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if not top or len(tokens) == 0:
				return (es[0], tokens)