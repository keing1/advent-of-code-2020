def parse_input():
	with open('input.txt', 'r') as f:
		cube_lines = f.read().split('\n')[:-1]

	cube_lines = [list(line) for line in cube_lines]

	return cube_lines

def pad_flat_input(cube_input, padding_num):
	num_rows = len(cube_input)
	num_cols = len(cube_input[0])

	updated_input_rows = [(['.'] * padding_num + inp_row + ['.'] * padding_num)
		for inp_row in cube_input]

	input_plane = [['.' for col in range(num_cols + 2*padding_num)]
		for row in range(padding_num)] + updated_input_rows + \
		[['.' for col in range(num_cols + 2*padding_num)]
		for row in range(padding_num)]

	final_space = [[['.'] * (2 * padding_num + num_cols) 
		for r in range(2*padding_num+num_rows)] for p in range(padding_num)] + \
		[input_plane] + \
		[[['.'] * (2 * padding_num + num_cols) 
		for r in range(2*padding_num+num_rows)] for p in range(padding_num)]

	return final_space

def find_valid_neighbor_tuples(curr_tup, dim_tup):
	z_coord, x_coord, y_coord = curr_tup
	z_dim, x_dim, y_dim = dim_tup

	diff_list = [-1,0,1]

	possible_neighbors = [(z_coord + z_diff, x_coord + x_diff, y_coord + y_diff)
		for z_diff in diff_list for x_diff in diff_list for y_diff in diff_list]
	possible_neighbors.remove((z_coord, x_coord, y_coord))

	valid_neighbors = [tup for tup in possible_neighbors if (0 <= tup[0] <= z_dim-1)
		and (0 <= tup[1] <= x_dim-1) and (0 <= tup[2] <= y_dim-1)]

	return valid_neighbors

def calculate_step(padded_space):
	num_z = len(padded_space)
	num_x = len(padded_space[0])
	num_y = len(padded_space[0][0])
	new_padded_space = [[['.']*num_y for x in range(num_x)] for z in range(num_z)]
	for z in range(num_z):
		for x in range(num_x):
			for y in range(num_y):
				neighbor_tuples = find_valid_neighbor_tuples((z, x, y), (num_z, num_x, num_y))
				num_adjacent_active = len([tup for tup in neighbor_tuples
					if padded_space[tup[0]][tup[1]][tup[2]] == '#'])

				curr_position = padded_space[z][x][y]

				if curr_position == '#':
					if 2 <= num_adjacent_active <= 3:
						new_position = '#'
					else:
						new_position = '.'
				else:
					if num_adjacent_active == 3:
						new_position = '#'
					else:
						new_position = '.'
				new_padded_space[z][x][y] = new_position
	return new_padded_space

def find_nth_step(parsed_input, n):
	curr_space = pad_flat_input(parsed_input, n)

	for step in range(n):
		curr_space = calculate_step(curr_space)

	curr_space_flattened = ''.join([''.join([''.join(row_list) for row_list in plane]) 
		for plane in curr_space])

	return curr_space_flattened.count('#')

def pad_flat_input_4d(cube_input, padding_num):
	num_rows = len(cube_input)
	num_cols = len(cube_input[0])

	padded_3d_space = pad_flat_input(cube_input, padding_num)

	final_4d_space = [[[['.'] * (2*padding_num+num_cols) 
		for r in range(2*padding_num+num_rows)] for z in range(2*padding_num+1)]
		for w in range(padding_num)] + \
		[padded_3d_space] + \
		[[[['.'] * (2*padding_num+num_cols) 
		for r in range(2*padding_num+num_rows)] for z in range(2*padding_num+1)]
		for w in range(padding_num)]

	return final_4d_space

def find_valid_neighbor_tuples_4d(curr_tup, dim_tup):
	w_coord, z_coord, x_coord, y_coord = curr_tup
	w_dim, z_dim, x_dim, y_dim = dim_tup

	diff_list = [-1,0,1]

	possible_neighbors = [(w_coord+w_diff, z_coord+z_diff, x_coord+x_diff, y_coord+y_diff)
		for w_diff in diff_list for z_diff in diff_list 
		for x_diff in diff_list for y_diff in diff_list]
	possible_neighbors.remove((w_coord, z_coord, x_coord, y_coord))

	valid_neighbors = [tup for tup in possible_neighbors if (0 <= tup[0] <= w_dim-1)
		and (0 <= tup[1] <= z_dim-1) and (0 <= tup[2] <= x_dim-1) 
		and (0 <= tup[3] <= y_dim-1)]

	return valid_neighbors

def calculate_step_4d(padded_space):
	num_w = len(padded_space)
	num_z = len(padded_space[0])
	num_x = len(padded_space[0][0])
	num_y = len(padded_space[0][0][0])

	new_padded_space = [[[['.']*num_y for x in range(num_x)] for z in range(num_z)]
		for w in range(num_w)]
	for w in range(num_w):
		for z in range(num_z):
			for x in range(num_x):
				for y in range(num_y):
					neighbor_tuples = find_valid_neighbor_tuples_4d((w, z, x, y), 
						(num_w, num_z, num_x, num_y))
					num_adjacent_active = len([tup for tup in neighbor_tuples
						if padded_space[tup[0]][tup[1]][tup[2]][tup[3]] == '#'])

					curr_position = padded_space[w][z][x][y]

					if curr_position == '#':
						if 2 <= num_adjacent_active <= 3:
							new_position = '#'
						else:
							new_position = '.'
					else:
						if num_adjacent_active == 3:
							new_position = '#'
						else:
							new_position = '.'
					new_padded_space[w][z][x][y] = new_position
	return new_padded_space

def find_nth_step_4d(parsed_input, n):
	curr_space = pad_flat_input_4d(parsed_input, n)

	for step in range(n):
		curr_space = calculate_step_4d(curr_space)

	curr_space_flattened = ''.join([''.join([''.join([''.join(row_list) 
		for row_list in plane]) for plane in space]) for space in curr_space])

	return curr_space_flattened.count('#')


if __name__ == '__main__':
	parsed_input = parse_input()

	sixth_step_space = find_nth_step(parsed_input, 6)
	print('The answer to the puzzle on Day 17 Part 1 is {}.'.format(sixth_step_space))

	sixth_step_space_4d = find_nth_step_4d(parsed_input, 6)
	print('The answer to the puzzle on Day 17 Part 2 is {}.'.format(sixth_step_space_4d))