def make_str_ints_when_applicable(my_str):
	if my_str == 'x':
		return my_str
	else:
		return int(my_str)


def parse_shuttles():
	with open('input.txt', 'r') as f:
		earliest_time = int(f.readline()[:-1])
		bus_id_list = f.readline()[:-1].split(',')
		bus_id_num_list = [make_str_ints_when_applicable(id_val) 
			for id_val in bus_id_list]
	return (earliest_time, bus_id_num_list)

def find_early_leave_product(parsed_shuttles):
	earliest_leave = parsed_shuttles[0]
	id_list = parsed_shuttles[1]

	id_list_wo_x = [id_val for id_val in id_list if id_val != 'x']

	id_wait_list = [(id_val, id_val - earliest_leave % id_val)
		for id_val in id_list_wo_x]

	min_tuple = min(id_wait_list, key=lambda tup: tup[1])
	return min_tuple[0]*min_tuple[1]

def find_adjacent_leave_timestamp(parse_shuttles):
	id_list = parse_shuttles[1]

	base_rem = 0
	curr_mod = id_list[0]
	tar_id_mod = 0
	print(id_list)
	for id_val in id_list[1:]:
		tar_id_mod -= 1
		if id_val != 'x':
			adj_tar_id_mod = tar_id_mod
			while adj_tar_id_mod < 0:
				adj_tar_id_mod = adj_tar_id_mod + id_val
			while base_rem % id_val != adj_tar_id_mod:
				base_rem = (base_rem + curr_mod)
			curr_mod *= id_val
			print(id_val)
			print(curr_mod)
			print(base_rem)

	return base_rem



if __name__ == '__main__':
	parsed_shuttles = parse_shuttles()
	early_leave_prod = find_early_leave_product(parsed_shuttles)
	print('The answer to the puzzle on Day 13 Part 1 is {}.'.format(early_leave_prod))

	adjacent_leave_timestamp = find_adjacent_leave_timestamp(parsed_shuttles)
	print('The answer to the puzzle on Day 13 Part 2 is {}.'.format(adjacent_leave_timestamp))