#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
	if type(e) == Leaf:
		if e == "True" or e == "False":
			return "Boolean"
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == "Number":
				return "Number"

			elif label == "Variable":
				name = children[0]

				if env[name] == "Number":
					return "Number"

			elif label == "Array":
				[x, e] = children
				x = x["Variable"][0]
				if x in env and env[x] == "Array" and typeExpression(env, e) == "Number":
					return "Number"

			elif label == "Plus":
				[left, right] = children
				if typeExpression(env, left) == "Number" and\
					typeExpression(env, right) == "Number":
					return "Number"

def typeProgram(env, s):
	if type(s) == Leaf:
		if s == "End":
			return "Void"
	elif type(s) == Node:
		for label in s:
			children = s[label]
			if label == "Print":
				[expression, rest] = children
				if (typeExpression(env, expression) == "Number" or\
					typeExpression(env, expression) == "Boolean") and\
					typeProgram(env, rest) == "Void":
					return "Void"

			elif label == "Assign":
				[x, e0, e1, e2, p] = children
				x = x["Variable"][0]
				if typeExpression(env, e0) == "Number" and\
				   typeExpression(env, e1) == "Number" and\
				   typeExpression(env, e2) == "Number":
					 env[x] = "Array"
					 if typeProgram(env, p) == "Void":
						   return "Void"

			elif label == "For":
				[name, body, rest] = children
				name = name["Variable"][0]

				env[name] = "Number"
				if typeProgram(env, body) == "Void" and\
					typeProgram(env, rest) == "Void":
					return "Void"

#eof