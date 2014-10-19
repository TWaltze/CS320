#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# machine.py
#

def simulate(s):
	instructions = s if type(s) == list else s.split("\n")
	instructions = [l.strip().split(" ") for l in instructions]
	mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
	control = 0
	outputs = []
	while control < len(instructions):
		# Update the memory address for control.
		mem[6] = control

		# Retrieve the current instruction.
		inst = instructions[control]

		# Handle the instruction.
		if inst[0] == "label":
			pass
		if inst[0] == "goto":
			control = instructions.index(["label", inst[1]])
			continue
		if inst[0] == "branch" and mem[int(inst[2])]:
			control = instructions.index(["label", inst[1]])
			continue
		if inst[0] == "jump":
			control = mem[int(inst[1])]
			continue
		if inst[0] == "set":
			mem[int(inst[1])] = int(inst[2])
		if inst[0] == "copy":
			mem[mem[4]] = mem[mem[3]]
		if inst[0] == "add":
			mem[0] = mem[1] + mem[2]

		# Push the output address's content to the output.
		if mem[5] > -1:
			outputs.append(mem[5])
			mem[5] = -1

		# Move control to the next instruction.
		control = control + 1

	print("memory: "+str(mem))
	return outputs

# Copy and store int value stored
# at address <frm> to address <to>
def copy(frm, to):
	return [\
		"set 3 " + str(frm),\
		"set 4 " + str(to),\
		"copy"\
	]

# Copy int value stored at address <frm>
# to address value stored in address <addr>
#
# Example:
# Address   Value
# 30        45
# 31        50
#
# copyFromToAddr(30, 31) =>
#
# Address   Value
# 30        45
# 31        50
# ...
# 50        45
def copyFromToAddr(frm, addr):
	return \
		copy(addr, 4) + [\
		"set 3 " + str(frm),\
		"copy"
	]

def add(addr, amount):
	return \
		copy(addr, 1) + [\
		"set 2 " + str(amount),\
		"add"] +\
		copy(0, addr) + [\
		"set 0 0",\
		"set 1 0",\
		"set 2 0"\
	]

# Add <amount> to the value at the address
# stored in address <addr>
#
# Example:
# Address   Value
# 30        31
# 31        50
#
# addAddr(30, 3) =>
#
# Address   Value
# 30        31
# 31        53
'''
set 3 <addr> (30)
set 4 3
copy
	=> Mem[3] = 31
	= copy(<addr>, 3)

set 4 1
copy
	=> Mem[1] = 50

set 2 <amount> (3)
add
	=> Mem[0] = 53

set 3 <addr> (30)
set 4 4
copy
	=> Mem[4] = 31
	= copy(<addr>, 4)

set 3 0
copy
	=>Mem[31] = 53

Clean up:
set 0 0
set 1 0
set 2 0
'''
def addAddr(addr, amount):
	return \
		copy(addr, 3) + [\
		"set 4 1",\
		"copy",\
		"set 2 " + str(amount),\
		"add"] + \
		copy(addr, 4) + [\
		"set 3 0",\
		"copy",\
		"set 0 0",\
		"set 1 0",\
		"set 2 0"\
	]


def increment(addr):
	return add(addr, 1)

# Increment the value at the address
# stored in address <addr>
def incrementAddr(addr):
	return addAddr(addr, 1)

def decrement(addr):
	return add(addr, -1)

# Decrement the value at the address
# stored in address <addr>
def decrementAddr(addr):
	return addAddr(addr, -1)

def call(name):
	calls = decrement(7) + copyFromToAddr(6, 7) + add(7, 1) + increment(7)

	return \
		decrement(7) +\
		copyFromToAddr(6, 7) +\
		add(7, len(calls) + 1) + [\
		"goto " + name] +\
		increment(7)

def procedure(name, body):
	return [\
		"goto " + name + "End",\
		"label " + name] +\
		body + [\
		"jump 7",\
		"label " + name + "End",\
	]

# exec(open("hw3-tests.py").read())
# eof
