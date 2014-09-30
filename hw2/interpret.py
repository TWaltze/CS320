#####
# Tyler Waltze
# CS 320
# HW2
#####

import math

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

Node = dict
Leaf = str

def evalTerm(env, t):
	if type(t) == Node:
		for label in t:
			children = t[label]
			if label == "Number":
				f1 = children[0]
				return f1
			elif label == "Parens":
				f1 = children[0]
				v1 = evalTerm(env, f1)
				return v1
			elif label == "Plus":
				f1 = children[0]
				v1 = evalTerm(env, f1)
				f2 = children[1]
				v2 = evalTerm(env, f2)
				return v1 + v2
			elif label == "Mult":
				f1 = children[0]
				v1 = evalTerm(env, f1)
				f2 = children[1]
				v2 = evalTerm(env, f2)
				return v1 * v2
			elif label == "Log":
				f1 = children[0]
				v1 = evalTerm(env, f1)
				return math.floor(math.log2(v1))
			elif label == "Variable":
				x = children[0]
				if x in env:
					return env[x]
				else:
					print(x + " is unbound.")
					exit()

def evalFormula(env, f):
	if type(f) == Node:
		for label in f:
			children = f[label]
			if label == "Parens":
				f1 = children[0]
				v1 = evalFormula(env, f1)
				return v1
			elif label == "Not":
				f = children[0]
				v = evalFormula(env, f)
				return vnot(v)
			elif label == "Xor":
				f1 = children[0]
				v1 = evalFormula(env, f1)
				f2 = children[1]
				v2 = evalFormula(env, f2)
				return xor(v1, v2)
			elif label == "Variable":
				x = children[0]
				if x in env:
					return env[x]
				else:
					print(x + " is unbound.")
					exit()
	elif type(f) == Leaf:
		if f == "True":
			return True
		if f == "False":
			return False

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
				v = evalFormula(env, f)
				(env, o) = execProgram(env, p)
				return (env, [v] + o)
			if label == "Assign":
				children = s[label]
				x = children[0]["Variable"][0]
				f = children[1]
				p = children[2]
				v = evalFormula(env, f)
				env[x] = v
				(env, o) = execProgram(env, p)
				return (env, o)
			if label == "IfFalse":
				children = s[label]
				x = children[0]["Variable"][0]
				f = children[1]
				p = children[2]
				v = evalFormula(env, f)
				env[x] = v
				(env, o) = execProgram(env, p)
				return (env, o)