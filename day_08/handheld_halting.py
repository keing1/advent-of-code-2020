def parse_instruction(instruction):
	[instr_name, instr_val] = instruction.split(' ')

	return (instr_name, int(instr_val))

def parse_instructions():
	with open('input.txt', 'r') as f:
		instruction_list = f.read().split('\n')[:-1]

	parsed_instruction_list = [parse_instruction(instruction) 
		for instruction in instruction_list]
	
	return parsed_instruction_list

def take_step(parsed_instructions, curr_line, curr_acc):
	curr_line_tuple = parsed_instructions[curr_line]
	curr_instr_name = curr_line_tuple[0]
	curr_instr_value = curr_line_tuple[1]

	if curr_instr_name == 'acc':
		curr_acc += curr_instr_value
		curr_line += 1
	elif curr_instr_name == 'jmp':
		curr_line += curr_instr_value
	elif curr_instr_name == 'nop':
		curr_line += 1
	else:
		raise InvalidArgumentError
	return curr_line, curr_acc

def find_instruction_loop_acc(parsed_instructions):
	visited_lines = set()

	curr_line = 0
	curr_acc = 0
	while True:
		if curr_line in visited_lines:
			break
		else:
			visited_lines.add(curr_line)
		curr_line, curr_acc = take_step(parsed_instructions, curr_line, curr_acc)

	return curr_acc

def create_reverse_edge_graph(parsed_instructions):
	edge_graph = {}

	for line, instruction in enumerate(parsed_instructions):
		instr_name = instruction[0]
		instr_val = instruction[1]

		if instr_name == 'jmp':
			dest_line = line + instr_val
		else:
			dest_line = line + 1

		if dest_line in edge_graph:
			edge_graph[dest_line] += [line]
		else:
			edge_graph[dest_line] = [line]

	return edge_graph

def find_reachable_instructions(parsed_instructions):
	reachable_instructions = set()
	curr_line = 0
	curr_acc = 0
	while True:
		if curr_line in reachable_instructions:
			break
		else:
			reachable_instructions.add(curr_line)
		curr_line, curr_acc = take_step(parsed_instructions, curr_line, curr_acc)
	return reachable_instructions

def find_backwards_reachable_instructions(parsed_instructions):
	reverse_edge_graph = create_reverse_edge_graph(parsed_instructions)
	backwards_reachable_instructions = set()

	current_instructions = [len(parsed_instructions)]

	while len(current_instructions) > 0:
		active_instr = current_instructions.pop()
		if active_instr in reverse_edge_graph:
			next_instrs = reverse_edge_graph[active_instr]

		next_instr_set = set(next_instrs)
		cleaned_next_instr_set = \
			next_instr_set.difference(backwards_reachable_instructions)

		current_instructions += list(cleaned_next_instr_set)
		backwards_reachable_instructions = \
			backwards_reachable_instructions.union(cleaned_next_instr_set)

	return backwards_reachable_instructions


def find_switched_instruction(parsed_instructions):
	# find instructions reachable from the start
	reachable_instructions = find_reachable_instructions(parsed_instructions)

	# find instructions that are 'backwards reachable' from the end
	# that is, lines that will eventually make their way to one line after
	# the last line of the program
	backwards_reachable_instructions = \
		find_backwards_reachable_instructions(parsed_instructions)

	# find which instruction in reachable_instructions, if switched
	# from a nop to jmp or from a jmp to a nop, would move to an
	# instruction in backwards reachable instructions
	buggy_instr = None
	for line in reachable_instructions:
		line_instr = parsed_instructions[line]
		instr_name = line_instr[0]
		instr_val = line_instr[1]
		
		if instr_name == 'nop':
			if line + instr_val in backwards_reachable_instructions:
				buggy_instr = line
				break
		elif instr_name == 'jmp':
			if line + 1 in backwards_reachable_instructions:
				buggy_instr = line
				break
	return buggy_instr


def find_altered_code_acc(parsed_instructions):
	buggy_instr_line = find_switched_instruction(parsed_instructions)

	buggy_instr = parsed_instructions[buggy_instr_line]
	buggy_instr_type = buggy_instr[0]
	buggy_instr_acc = buggy_instr[1]
	if buggy_instr_type == 'nop':
		parsed_instructions[buggy_instr_line] = ('jmp', buggy_instr_acc)
	else:
		parsed_instructions[buggy_instr_line] = ('nop', buggy_instr_acc)

	curr_line = 0
	curr_acc = 0
	while True:
		if curr_line == len(parsed_instructions):
			break
		curr_line, curr_acc = take_step(parsed_instructions, curr_line, curr_acc)

	return curr_acc

if __name__ == '__main__':
	parsed_instructions = parse_instructions()

	acc_loop_value = find_instruction_loop_acc(parsed_instructions)
	print('The answer to the puzzle on Day 8 Part 1 is {}.'.format(acc_loop_value))

	acc_final_value = find_altered_code_acc(parsed_instructions)
	print('The answer to the puzzle on Day 8 Part 2 is {}.'.format(acc_final_value))