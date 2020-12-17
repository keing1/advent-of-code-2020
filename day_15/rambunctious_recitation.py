def find_next_num(visited_dict, last_num, last_ind):
	if last_num not in visited_dict:
		return 0
	else:
		return last_ind - visited_dict[last_num]

def find_nth_num(n):
	input_list = [8,0,17,4,1,12]
	visited_dict = {}

	for i, v in enumerate(input_list[:-1]):
		visited_dict[v] = i+1

	last_ind = len(input_list)
	last_num = input_list[-1]

	for ind in range(len(input_list)+1, n+1):
		next_num = find_next_num(visited_dict, last_num, last_ind)
		visited_dict[last_num] = last_ind
	
		last_ind += 1
		last_num = next_num

	return last_num

if __name__ == '__main__':
	num_2020 = find_nth_num(2020)
	print('The answer to the puzzle on Day 15 Part 1 is {}.'.format(num_2020))

	num_30000000 = find_nth_num(30000000)
	print('The answer to the puzzle on Day 15 Part 2 is {}.'.format(num_30000000))
