#####
# Tyler Waltze
# CS 320
# HW3
#####

import random

def freshStr():
	return str(random.randint(0,100000))

def compileTerm(env, t, heap):
	print("enter term")
	print("env", env)
	print("t", t)
	print("heap", heap)
	print("\n")
	if type(t) == Node:
		for label in t:
			children = t[label]

			if label == "Number":
				print("enter number")
				print("children", children)
				print("\n")
				num = children[0]
				heap += 1;
				inst = "set {} {}".format(str(heap), num)

				return ([inst], heap, heap)
			elif label == "Variable":
				blah = lbah

def compileFormula(env, f, heap):
	print("enter formula")
	print("env", env)
	print("f", f)
	print("heap", heap)
	print("\n")
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
			if label == "Not":
				# Compile the subtree f to obtain the list of
				# instructions that computes the value represented
				# by f.
				f = children[0]
				(insts, addr, heap) = compileFormula(env, f, heap)

				# Generate more instructions to change the memory
				# location in accordance with the definition of the
				# Not operation.
				fresh = freshStr();
				instsNot = \
				   ["branch setZero{} {}".format(fresh, str(heap)),\
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
				instsOr = [\
					"copy " + str(addr1) + " 1",\
					"copy " + str(addr2) + " 2",\
					"add",\
					"branch setOne" + fresh + " 0",\
					"goto finish" + fresh,\
					"label setOne" + fresh,\
					"set 0 1",\
					"label finish" + fresh,\
					"copy 0 " + str(heap4)\
				]

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

def compileProgram(env, s, heap):
	print("enter program")
	print("env", env)
	print("s", s)
	print("heap", heap)
	print("\n")
	if type(s) == Leaf:
		if s == "End":
			return (env, [], heap)
	elif type(s) == Node:
		for label in s:
			children = s[label]
			if label == "Print":
				print("enter print")
				print("children", children)
				print("\n")
				f = children[0]
				rest = children[1]
				(insts, addr, heap) = compileTerm(env, f, heap) or compileFormula(env, f, heap)
				print("insts", insts)
				print("addr", addr)
				print("heap", heap)
				print("\n")

				instsPrint = copy(heap, 5)
				print("instsPrint", instsPrint)

				(envRest, instsRest, heapRest) = compileProgram(env, rest, heap)
				print("envRest", envRest)
				print("instsRest", instsRest)
				print("heapRest", heapRest)
				print("\n")

				return (envRest, insts + instsPrint + instsRest, heapRest)

def compile(s):
	startOfHeap = 8
	setup = [\
		"set 7 -1"\
	]

	(env, insts, heap) = compileProgram({}, tokenizeAndParse(s), startOfHeap)
	print("final instructions", setup + insts)
	print("\n")
	return setup + insts