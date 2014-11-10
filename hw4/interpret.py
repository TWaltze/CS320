#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def subst(s, a):
	if "Variable" in a:
		name = a["Variable"][0]

		if name in s:
			del a["Variable"]
			a.update(s[name])
	elif type(a) == Node:
		for label in a:
			children = a[label]

			# print(children)
			# for child in children:
			# 	if "Variable" in child:
			# 		name = child["Variable"][0]

			# 		if name in s:
			# 			del child["Variable"]
			# 			child.update(s[name])
			# 	else:
			# 		subst(s, child)

			for child in children:
				subst(s, child)

	return a

def unify(a, b):
	pass # Complete for Problem #1, part (b).

def build(m, d):
	pass # Complete for Problem #2, part (a).

def evaluate(m, env, e):
	pass # Complete for Problem #2, part (b).

def interact(s):
	# Build the module definition.
	m = build({}, parser(grammar, 'declaration')(s))

	# Interactive loop.
	while True:
		# Prompt the user for a query.
		s = input('> ') 
		if s == ':quit':
			break
		
		# Parse and evaluate the query.
		e = parser(grammar, 'expression')(s)
		if not e is None:
			print(evaluate(m, {}, e))
		else:
			print("Unknown input.")

#eof