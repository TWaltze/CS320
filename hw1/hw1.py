############
# Tyler Waltze
# CS 320
# Homework 1
# 9/15/14
############

import re
import json

######### QUESTION 1 #########
def tokenize(terminals, s):
	# Safely escape all special characters for regex
	terminals = [re.escape(t) for t in terminals]

	# Use a regular expression to split the string into
	# tokens or sequences of zero or more spaces.
	regex = "(\s+|" + "|".join(map(str, terminals)) + ")"
	tokens = [t for t in re.split(r"" + regex, s)]

	# Throw out the spaces and return the result.
	return [t for t in tokens if not t.isspace() and not t == ""]


####
# BNF Notation
#
# directions	::=	forward ; directions
#				| reverse ; directions
#				| left turn ; directions
#				| right turn ; directions
#				| stop ;
####
def directions(tokens):
	if tokens[0] == "forward" and tokens[1] == ";":
		(e1, tokens) = directions(tokens[2:])
		return ({"Forward": [e1]}, tokens)

	if tokens[0] == "reverse" and tokens[1] == ";":
		(e1, tokens) = directions(tokens[2:])
		return ({"Reverse": [e1]}, tokens)

	if tokens[0] == "left" and tokens[1] == "turn" and tokens[2] == ";":
		(e1, tokens) = directions(tokens[3:])
		return ({"LeftTurn": [e1]}, tokens)

	if tokens[0] == "right" and tokens[1] == "turn" and tokens[2] == ";":
		(e1, tokens) = directions(tokens[3:])
		return ({"RightTurn": [e1]}, tokens)

	if tokens[0] == "stop" and tokens[1] == ";":
		return ("Stop", tokens[2:])

######### QUESTION 2 #########
def number(tokens, top = True):
	if re.match(r"^([1-9][0-9]*)$", tokens[0]):
		return (int(tokens[0]), tokens[1:])

def variable(tokens, top = True):
	if re.match(r"^([a-zA-Z])+$", tokens[0]):
		return (tokens[0], tokens[1:])

def variableWrapped(tokens, top = True):
	if re.match(r"^([a-zA-Z])+$", tokens[0]):
		return ({"Variable": [tokens[0]]}, tokens[1:])

def program(tmp, top = True):
	seqs = [\
		('End', ['end', ";"]), \
		('Assign', ['assign', '@', variableWrapped, ":=", term, ";", program]), \
		('Print', ['print', formula, ";", program]), \
		('Print', ['print', term, ";", program]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens[0] == x:
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

def complete(s):
	terminals = ["print", "assign", "end", "not", "and", "or", "equal", "less", "greater", "than", "plus", "mult", "log", "@", "#", "(", ")", ";", ",", ":=", "&&", "||", "+", "*", "<", ">", "=="]
	tokens = tokenize(terminals, s)

	return program(tokens)

def formula(tmp, top = True):
	seqs = [\
		('True', ['true']), \
		('False', ['false']), \
		('Not', ['not', '(', formula, ')']), \
		('And', ['and', '(', formula, ",", formula, ')']), \
		('And', ['(', formula, "&&", formula, ')']), \
		('Or', ['or', '(', formula, ",", formula, ')']), \
		('Or', ['(', formula, "||", formula, ')']), \
		('Equal', ['equal', '(', term, ",", term, ')']), \
		('Equal', ['(', term, "==", term, ')']), \
		('LessThan', ['less', "than", '(', term, ",", term, ')']), \
		('LessThan', ['(', term, "<", term, ')']), \
		('GreaterThan', ['greater', "than", '(', term, ",", term, ')']), \
		('GreaterThan', ['(', term, ">", term, ')']), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens[0] == x:
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

def term(tmp, top = True):
	seqs = [\
		('Plus', ['plus', '(', term, ",", term, ')']), \
		('Plus', ['(', term, "+", term, ')']), \
		('Mult', ['mult', '(', term, ",", term, ')']), \
		('Mult', ['(', term, "*", term, ')']), \
		('Log', ['log', '(', term, ')']), \
		('Variable', ['@', variable]), \
		('Number', ['#', number]), \
	]

	for (label, seq) in seqs:
		tokens = tmp[0:]

		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if tokens[0] == x:
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