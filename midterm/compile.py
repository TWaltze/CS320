#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
	return str(randint(0,10000000))

def compileExpression(env, e, heap):
	# Complete 'True', 'False', 'Array', and 'Plus' cases for Problem #3.
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == "Number":
				n = children[0]
				heap = heap + 1
				return (["set " + str(heap) + " " + str(n)], heap, heap)
			elif label == "Plus":
				(instLeft, addrLeft, heapLeft) = compileExpression(env, children[0], heap)
				(instRight, addrRight, heapRight) = compileExpression(env, children[1], heapLeft)

				heapPlus = heapRight + 1
				instPlus = \
					copy(addrLeft, 1) +\
					copy(addrRight, 2) +[\
					"add"] +\
					copy(0, heapPlus)

				return (instLeft + instRight + instPlus, heapPlus, heapPlus)
			elif label == "Array":
				(instVar, addrVar, heapVar) = compileExpression(env, children[0], heap);
				(instIndex, addrIndex, heapIndex) = compileExpression(env, children[1], heapVar)
				addrValue = addrVar + addrIndex

				heapValue = heapVar + 1
				instArray = \
					copy(addrIndex, 1) + [\
					"set 2 " + str(addrVar),\
					"add"] +\
					copy(0, 3) + [\
					"set 4 " + str(heapValue),\
					"copy"]

				return (instVar + instIndex + instArray, heapValue, heapValue)
			elif label == "Variable":
				x = children[0]
				if x in env:
					return ([], env[x], heap)
				else:
					print(x + " is unbound.")
					exit()
	if type(e) == Leaf:
		if e == "True":
			heap += 1
			inst = "set {} 1".format(str(heap))

			return ([inst], heap, heap)
		if e == "False":
			heap += 1
			inst = "set {} 0".format(str(heap))

			return ([inst], heap, heap)

def compileProgram(env, s, heap = 8): # Set initial heap default address.
	# Complete 'Assign' case for Problem #3.
	if type(s) == Leaf:
		if s == "End":
			return (env, [], heap)

	if type(s) == Node:
		for label in s:
			children = s[label]
			if label == "Print":
				[e, p] = children
				(instsE, addr, heap) = compileExpression(env, e, heap)
				(env, instsP, heap) = compileProgram(env, p, heap)
				return (env, instsE + copy(addr, 5) + instsP, heap)
			elif label == "Assign":
				name = children[0]["Variable"][0]
				heapStartOfArray = heap + 1
				heapEndOfArray = heapStartOfArray + 3
				(instFirst, addrFirst, heapFirst) = compileExpression(env, children[1], heapEndOfArray)
				(instSecond, addrSecond, heapSecond) = compileExpression(env, children[2], heapFirst)
				(instThird, addrThrd, heapThird) = compileExpression(env, children[3], heapSecond)
				rest = children[4]

				env[name] = heapStartOfArray
				instAssign = copy(addrFirst, heapStartOfArray) +\
					copy(addrSecond, heapStartOfArray + 1) +\
					copy(addrThrd, heapStartOfArray + 2)

				(envRest, instsRest, heapRest) = compileProgram(env, rest, heapThird)
				return (envRest, instFirst + instSecond + instThird + instAssign + instsRest, heapRest)

def compile(s):
	p = tokenizeAndParse(s)
	# Add call to type checking algorithm for Problem #4.

	# Add calls to optimization algorithms for Problem #3.
	op = foldConstants(p)
	op = unrollLoops(op)

	(env, insts, heap) = compileProgram({}, op)
	return insts

def compileAndSimulate(s):
	return simulate(compile(s))

# exec(open("compile.py").read())
# Various test cases
# compileAndSimulate("assign x := [2, 4, 6]; for i {print i;}")
# compileAndSimulate("assign x := [2, 4, 6]; for i {print @ x [i];}")

# compileAndSimulate("assign x := [100, 200, 500]; assign y := [600, @ x [1 + 1] + @ x [1], 800]; print @ y [0]; print @ y [1]; print @ y [2]; assign x := [1000, 1000, 1000]; print @ x [0]; print @ x [1]; print @ x [2]; for i { print i; for j { print @ y [j]; } }")
# Output: 600, 700, 800, 1000, 1000, 1000, 0, 600, 700, 800, 1, 600, 700, 800, 2, 600, 700, 800

# compileAndSimulate("assign x := [100, 200, 500]; assign y := [@ x [0], @ x [1 + 1] + @ x [1], 800]; print @ y [0];")
# compileAndSimulate("assign x := [100, 200, 500]; assign y := [600, @ x [1 + 1] + @ x [1], 800]; print @ y [1];")

#eof
