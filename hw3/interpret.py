######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
# interpret.py
#
# Tyler Waltze

exec(open("parse.py").read())

Node = dict
Leaf = str

def vnot(v):
	if v == True:  return False
	if v == False: return True

def vand(v1, v2):
	if v1 == True  and v2 == True:  return True
	if v1 == True  and v2 == False: return False
	if v1 == False and v2 == True:  return False
	if v1 == False and v2 == False: return False

def vor(v1, v2):
	if v1 == True  and v2 == True:  return True
	if v1 == True  and v2 == False: return True
	if v1 == False and v2 == True:  return True
	if v1 == False and v2 == False: return False

def xor(v1, v2):
	if v1 == True  and v2 == True:  return False
	if v1 == True  and v2 == False: return True
	if v1 == False and v2 == True:  return True
	if v1 == False and v2 == False: return False

def evalTerm(env, t):
	if type(t) == Node:
		for label in t:
			children = t[label]
			if label == "Number":
				f1 = children[0]
				return f1
			elif label == "Plus":
				f1 = children[0]
				v1 = evalTerm(env, f1)
				f2 = children[1]
				v2 = evalTerm(env, f2)
				return v1 + v2
			elif label == "Variable":
				x = children[0]
				if x in env:
					return evalExpression(env, x)
				else:
					print(x + " is unbound.")
					exit()

def evalFormula(env, f):
	if type(f) == Node:
		for label in f:
			children = f[label]
			if label == "Not":
				f = children[0]
				v = evalFormula(env, f)
				return vnot(v)
			elif label == "And":
				f1 = children[0]
				v1 = evalFormula(env, f1)

				# Short And:
				# Don't eval second term
				# if first is already false
				if not v1:
					return False

				f2 = children[1]
				v2 = evalFormula(env, f2)

				return vand(v1, v2)
			elif label == "Or":
				f1 = children[0]
				v1 = evalFormula(env, f1)

				# Short Or:
				# Don't eval second term
				# if first is already true
				if v1:
					return True

				f2 = children[1]
				v2 = evalFormula(env, f2)

				return vand(v1, v2)
			elif label == "Variable":
				x = children[0]
				if x in env:
					return evalExpression(env, x)
					# return env[x]
				else:
					print(x + " is unbound.")
					exit()
	elif type(f) == Leaf:
		if f == "True":
			return True
		if f == "False":
			return False

def evalExpression(env, e):
	if type(e) == Leaf:
		# e is either a variable name or boolean value
		if e == "True":
			return True
		elif e == "False":
			return False
		else:
			# Get expression assigned to variable name
			x = env[e]
	else:
		# e is a tree
		x = e

	# Could be referencing
	# a term, formula, or program
	# so check for all.
	return evalTerm(env, x) or \
		evalFormula(env, x) or \
		execProgram(env, x)

def execProgram(env, s):
	if type(s) == Leaf:
		if s == "End":
			return (env, [])
	elif type(s) == Node:
		for label in s:
			if label == "Print":
				children = s[label]
				f = children[0]
				p = children[1]

				# Could be referencing either
				# a term or a formula, so check
				# for both.
				v = evalTerm(env, f)
				if v == None:
					v = evalFormula(env, f)

				(env, o) = execProgram(env, p)
				return (env, [v] + o)
			elif label == "Assign":
				children = s[label]
				x = children[0]["Variable"][0]
				f = children[1]
				p = children[2]
				env[x] = f
				(env, o) = execProgram(env, p)
				return (env, o)
			elif label == "If":
				children = s[label]
				x = children[0]
				f = children[1]
				p = children[2]
				v = evalExpression(env, x)
				if v:
					(env, o) = execProgram(env, f)

				(env, o2) = execProgram(env, p)
				return (env, o + o2)
			elif label == "While":
				children = s[label]
				x = children[0]
				f = children[1]
				p = children[2]
				v = evalExpression(env, x)
				o = []
				while v:
					(env, o_loop) = execProgram(env, f)
					o += o_loop
					v = evalExpression(env, x)

				(env, o2) = execProgram(env, p)
				return (env, o + o2)
			elif label =="Procedure":
				children = s[label]
				x = children[0]["Variable"][0]
				f = children[1]
				p = children[2]
				env[x] = f
				(env, o) = execProgram(env, p)
				return (env, o)
			elif label == "Call":
				children = s[label]
				x = children[0]["Variable"][0]
				p = children[1]
				v = evalExpression(env, x)
				(env, o) = execProgram(env, p)
				return (env, v[1] + o)

def interpret(s):
	(env, o) = execProgram({}, tokenizeAndParse(s))
	return o

#eof
