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

			for child in children:
				subst(s, child)

	return a

def unify(a, b):
	# Grab root node's label
	if type(a) == Node and type(b) == Node:
		aLabel = a.keys()[0]
		bLabel = b.keys()[0]

	# Convert int/bool to str (Leaf == str)
	if type(a) != Node: a = str(a)
	if type(b) != Node: b = str(b)

	if type(a) == Leaf and type(b) == Leaf:
		if a == b:
			return {}
		else:
			return None
	if type(a) == Node and "Variable" in a:
		name = a["Variable"][0]
		return {name: b}
	if type(b) == Node and "Variable" in b:
		name = b["Variable"][0]
		return {name: a}
	if aLabel == bLabel and len(a[aLabel]) == len(b[bLabel]):
		sub = None

		for index in range(0, len(a[aLabel])):
			u = unify(a[aLabel][index], b[bLabel][index])

			# Found unification
			if not u == None:
				# initialize sub with found substition
				if sub == None:
					sub = u
				# update sub with substition
				else:
					sub.update(u)

		return sub

def build(m, d):
	if type(d) == Node:
		for label in d:
			children = d[label]

			name = children[0]["Variable"][0]
			pattern = children[1]
			expression = children[2]
			rest = children[3]

			t = (pattern, expression)

			if name in m:
				m[name] += [t]
			else:
				m.update({name: [t]})

			return build(m, rest)
	elif type(d) == Leaf:
		if d == "End":
			return m

def evaluate(m, env, e):
	if type(e) == Node:
		for label in e:
			children = e[label]

			if label == "Number":
				return children[0]
			elif label == "ConBase":
				return e
			elif label == "ConInd":
				con = children[0]
				arg1 = evaluate(m, env, children[1])
				arg2 = evaluate(m, env, children[2])

				return {"ConInd": [con, arg1, arg2]}
			elif label == "Plus":
				left = children[0]
				v1 = evaluate(m, env, left)

				right = children[1]
				v2 = evaluate(m, env, right)

				return v1 + v2
			elif label == "Apply":
				name = children[0]["Variable"][0]
				arg = evaluate(m, env, children[1])

				if name in m:
					for item in m[name]:
						sub = unify(arg, item[0])

						# Returned a substition
						if not sub == None:
							env.update(sub)
							return evaluate(m, env, item[1])


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
