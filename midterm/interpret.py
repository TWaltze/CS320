#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
	if type(e) == Node:
		for label in e:
			children = e[label]

			if label == "Number":
				return children[0]
			elif label == "Plus":
				left = children[0]
				v1 = evaluate(env, left)

				right = children[1]
				v2 = evaluate(env, right)

				return v1 + v2
			elif label == "Array":
				var = evaluate(env, children[0]);
				index = evaluate(env, children[1])

				return var[index]
				# return evaluate(env, var[index])
			elif label == "Variable":
				x = children[0]
				if x in env:
					return env[x]
				else:
					print(x + " is unbound.")
					exit()
	elif type(e) == Leaf:
		if e == "True":
			return True
		if e == "False":
			return False

def execute(env, s):
	if type(s) == Leaf:
		if s == "End":
			return (env, [])
	elif type(s) == Node:
		for label in s:
			children = s[label]
			if label == "Print":
				exp = children[0]
				rest = children[1]

				value = evaluate(env, exp)

				(env, o) = execute(env, rest)
				return (env, [value] + o)
			elif label == "Assign":
				name = children[0]["Variable"][0]
				firstIndex = evaluate(env, children[1])
				secondIndex = evaluate(env, children[2])
				thirdIndex = evaluate(env, children[3])
				# firstIndex = children[1]
				# secondIndex = children[2]
				# thirdIndex = children[3]
				rest = children[4]

				env[name] = [firstIndex, secondIndex, thirdIndex]

				(env, o) = execute(env, rest)
				return (env, o)
			elif label == "For":
				var = children[0]
				body = children[1]
				rest = children[2]

				# first loop
				(env, o1) = execute(env, body)
				# second loop
				(env, o2) = execute(env, body)
				# third loop
				(env, o3) = execute(env, body)

				(env, o4) = execute(env, rest)
				return (env, o1 + o2 + o3 + o4)

def interpret(s):
	(env, o) = execute({}, tokenizeAndParse(s))
	return o

'''
Input:
assign x := [true, 2, 5]; assign y := [@ x [0], @ x [1 + 1] + @ x [1], false]; print @ y [0]; print @ y [1]; print @ y [2]; assign x := [1, 1, 1]; print @ x [0]; print @ x [1]; print @ x [2]; for x { for y { print @ y [1]; } print true; }

Expanded:
assign x := [true, 2, 5];
assign y := [@ x [0], @ x [1 + 1] + @ x [1], false];

print @ y [0];
print @ y [1];
print @ y [2];
# true, 7, false

assign x := [1, 1, 1];

print @ x [0];
print @ x [1];
print @ x [2];
# 1, 1, 1

for x {
	for y {
		print @ y [1];
		# true
		# OR
		# 1
	}
	print true;
}

Output: true, 7, false, 1, 1, 1, 7, 7, 7, true, 7, 7, 7, true, 7, 7, 7, true

OR

Output: true, 7, false, 1, 1, 1, 2, 2, 2, true, 2, 2, 2, true, 2, 2, 2, true
'''

#eof
