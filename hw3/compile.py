#####
# Tyler Waltze
# CS 320
# HW3
#####

import random

def freshStr():
	return str(random.randint(0,100000))

def compileTerm(env, t, heap):
	if type(t) == Node:
		for label in t:
			children = t[label]

			if label == "Number":
				num = children[0]
				heap += 1;
				inst = "set {} {}".format(str(heap), num)

				return ([inst], heap, heap)
			elif label == "Plus":
				(instLeft, addrLeft, heapLeft) = compileTerm(env, children[0], heap)
				(instRight, addrRight, heapRight) = compileTerm(env, children[1], heapLeft)

				heapPlus = heapRight + 1
				instPlus = \
					copy(addrLeft, 1) +\
					copy(addrRight, 2) +[\
					"add"] +\
					copy(0, heapPlus)

				return (instLeft + instRight + instPlus, heapPlus, heapPlus)
			elif label == "Variable":
				x = children[0]
				if x in env:
					return ([], env[x], heap)
				else:
					print(x + " is unbound.")
					exit()

def compileFormula(env, f, heap):
	if type(f) == Leaf:
		if f == "True":
			heap += 1
			inst = "set {} 1".format(str(heap))

			return ([inst], heap, heap)
		if f == "False":
			heap += 1
			inst = "set {} 0".format(str(heap))

			return ([inst], heap, heap)
	if type(f) == Node:
		for label in f:
			children = f[label]
			if label == "Variable":
				x = children[0]
				if x in env:
					return ([], env[x], heap)
				else:
					print(x + " is unbound.")
					exit()
			elif label == "Not":
				# Compile the subtree f to obtain the list of
				# instructions that computes the value represented
				# by f.
				f = children[0]
				(insts, addr, heap) = compileFormula(env, f, heap)

				# Generate more instructions to change the memory
				# location in accordance with the definition of the
				# Not operation.
				fresh = freshStr();
				instsNot = [\
					"branch setZero{} {}".format(fresh, str(heap)),\
					"set " + str(heap) + " 1",\
					"branch finish" + fresh,\
					"label setZero" + fresh,\
					"set " + str(heap) + " 0",\
					"label finish" + fresh\
				]

				return (insts + instsNot, heap, heap)
			elif label == "Or":
				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				f1 = children[0]
				f2 = children[1]
				(insts1, addr1, heap2) = compileFormula(env, f1, heap)
				(insts2, addr2, heap3) = compileFormula(env, f2, heap2)
				# Increment the heap counter so we store the
				# result of computing Or in a new location.
				heap4 = heap3 + 1

				# Add instructions that compute the result of the
				# Or operation.
				fresh = freshStr();
				instsOr = \
					copy(addr1, 1) +\
					copy(addr2, 2) +\
					["add",\
					"branch setOne" + fresh + " 0",\
					"goto finish" + fresh,\
					"label setOne" + fresh,\
					"set 0 1",\
					"label finish" + fresh] +\
					copy(0, heap4)

				return (insts1 + insts2 + instsOr, heap4, heap4)
			elif label == "And":
				f1 = children[0]
				f2 = children[1]
				(insts1, addr1, heap2) = compileFormula(env, f1, heap)
				(insts2, addr2, heap3) = compileFormula(env, f2, heap2)
				heap4 = heap3 + 1

				fresh = freshStr();
				instsAnd = [\
					"label checkFirst" + fresh] +\
					copy(addr1, 1) +\
					["set 2 0",\
					"add",\
					"branch checkSecond" + fresh + " 0",\
					"goto finish" + fresh,\
					"label checkSecond" + fresh] +\
					copy(addr2, 1) +\
					["set 2 0",\
					"add",\
					"branch setOne" + fresh + " 0",\
					"goto finish" + fresh,\
					"label setOne" + fresh,\
					"set 0 1",\
					"label finish" + fresh] +\
					copy(0, heap4)

				return (insts1 + insts2 + instsAnd, heap4, heap4)

def compileExpression(env, e, heap):
	return compileTerm(env, e, heap) or compileFormula(env, e, heap)

def compileProgram(env, s, heap):
	if type(s) == Leaf:
		if s == "End":
			return (env, [], heap)
	elif type(s) == Node:
		for label in s:
			children = s[label]
			if label == "Print":
				expression = children[0]
				rest = children[1]
				(insts, addr, heap) = compileExpression(env, expression, heap)

				instsPrint = copy(heap, 5)

				(envRest, instsRest, heapRest) = compileProgram(env, rest, heap)

				return (envRest, insts + instsPrint + instsRest, heapRest)
			elif label == "Assign":
				name = children[0]["Variable"][0]
				expression = children[1]
				rest = children[2]

				(insts, addr, heap) = compileExpression(env, expression, heap)
				# If updating a preexisting variable,
				# don't reassign to heap. Instead,
				# update current heap location
				if name in env:
					instAssign = copy(heap, env[name])
				else:
					env[name] = addr
					instAssign = []

				(envRest, instsRest, heapRest) = compileProgram(env, rest, heap)

				return (envRest, insts + instAssign + instsRest, heapRest)
			elif label == "If":
				condition = children[0]
				body = children[1]
				rest = children[2]

				(instCond, addrCond, heapCond) = compileExpression(env, condition, heap)
				(envBody, instBody, heapBody) = compileProgram(env, body, heapCond)

				fresh = freshStr()
				instIf = [\
					"branch startIf{} {}".format(fresh, addrCond),\
					"goto endIf" + fresh,\
					"label startIf" + fresh] +\
					instBody + [\
					"label endIf" + fresh
				]

				(envRest, instRest, heapRest) = compileProgram(envBody, rest, heapBody)

				return (envRest, instCond + instIf + instRest, heapRest)
			elif label == "While":
				condition = children[0]
				body = children[1]
				rest = children[2]

				(instCond, addrCond, heapCond) = compileExpression(env, condition, heap)
				(envBody, instBody, heapBody) = compileProgram(env, body, heapCond)

				fresh = freshStr()
				instIf = [\
					"label whileCondition" + fresh,\
					"branch startWhile{} {}".format(fresh, addrCond),\
					"goto endWhile" + fresh,\
					"label startWhile" + fresh] +\
					instBody + [\
					"goto whileCondition" + fresh,\
					"label endWhile" + fresh
				]

				(envRest, instRest, heapRest) = compileProgram(envBody, rest, heapBody)

				return (envRest, instCond + instIf + instRest, heapRest)
			elif label == "Procedure":
				name = children[0]["Variable"][0]
				body = children[1]
				rest = children[2]

				(envBody, instBody, heapBody) = compileProgram(env, body, heap)

				instProcedure = procedure(name, instBody)

				(envRest, instRest, heapRest) = compileProgram(envBody, rest, heapBody)

				return (envRest, instProcedure + instRest, heapRest)
			elif label == "Call":
				name = children[0]["Variable"][0]
				rest = children[1]

				instCall = call(name)

				(envRest, instRest, heapRest) = compileProgram(env, rest, heap)

				return (envRest, instCall + instRest, heapRest)

def compile(s):
	startOfHeap = 8
	setup = [\
		"set 7 -1"\
	]

	(env, insts, heap) = compileProgram({}, tokenizeAndParse(s), startOfHeap)
	return setup + insts