import itertools

def parse_init_code():
	with open('input.txt', 'r') as f:
		init_lines = f.read().split('\n')[:-1]

	init_tuple_line = []
	for line in init_lines:
		if line[:4] == 'mask':
			init_tuple_line += [('mask', line[7:])]
		else:
			split_line = line.split(' = ')
			data_val = split_line[1]
			mem_val = split_line[0].split('[')[1][:-1]
			init_tuple_line += [('mem', int(mem_val), int(data_val))]

	return init_tuple_line

def calc_masked_num_one(mask, inp_num):
	long_bin_str = '{0:036b}'.format(inp_num)

	new_str_list = []
	for a, b in zip(long_bin_str, mask):
		if b == 'X':
			new_str_list += [a]
		else:
			new_str_list += [b]

	new_str = ''.join(new_str_list)
	return int(new_str, 2)

def calc_final_sum_one(parsed_init):
	data_dict = {}

	curr_mask = None
	for line in parsed_init:
		instr_type = line[0]
		if instr_type == 'mask': 
			curr_mask = line[1]
		else:
			mem_val = line[1]
			data_val = line[2]
			masked_num = calc_masked_num_one(curr_mask, data_val)
			data_dict[mem_val] = masked_num

	final_sum = 0
	for key in data_dict:
		final_sum += data_dict[key]

	return final_sum

def calc_mem_list_from_str(mem_str):
	x_indices = [i for i, v in enumerate(mem_str) if v == 'X']
	num_x = len(x_indices)
	if num_x == 0:
		return [mem_str]

	binary_lists = [[0,1]]*num_x
	x_possibilities = list(itertools.product(*binary_lists))

	final_mem_list = []
	for p in x_possibilities:
		last_index = -1
		built_str = ''
		for i, v in enumerate(x_indices):
			built_str += mem_str[last_index+1:v]
			built_str += str(p[i])
			last_index = v
		built_str += mem_str[x_indices[-1]+1:]
		final_mem_list += [built_str]

	return final_mem_list

def calc_masked_mem_list(mask, mem_val):
	long_bin_str = '{0:036b}'.format(mem_val)

	new_str_list = []
	for a, b in zip(long_bin_str, mask):
		if b == 'X':
			new_str_list += ['X']
		elif b == '1':
			new_str_list += [b]
		else:
			new_str_list += [a]

	new_str = ''.join(new_str_list)

	masked_mem_list = calc_mem_list_from_str(new_str)
	return masked_mem_list

def calc_final_sum_two(parsed_init):
	data_dict = {}

	curr_mask = None
	for line in parsed_init:
		instr_type = line[0]
		if instr_type == 'mask': 
			curr_mask = line[1]
		else:
			mem_val = line[1]
			data_val = line[2]
			mem_list = calc_masked_mem_list(curr_mask, mem_val)
			for mem_val in mem_list:
				data_dict[mem_val] = data_val

	final_sum = 0
	for key in data_dict:
		final_sum += data_dict[key]

	return final_sum
			

if __name__ == '__main__':
	parsed_init = parse_init_code()
	final_sum_p_one = calc_final_sum_one(parsed_init)
	print('The answer to the puzzle on Day 14 Part 1 is {}.'.format(final_sum_p_one))

	final_sum_p_two = calc_final_sum_two(parsed_init)
	print('The answer to the puzzle on Day 14 Part 2 is {}.'.format(final_sum_p_two))

