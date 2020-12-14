def parse_geology():
	with open('input.txt', 'r') as f:
		geology_matrix = f.read().splitlines()

	return geology_matrix

def calculate_num_trees(num_right, num_down, geology_matrix):
	matrix_width = len(geology_matrix[0])

	x_pos = 0
	y_pos = 0
	trees_count = 0

	while y_pos < len(geology_matrix):
		if geology_matrix[y_pos][x_pos] == "#":
			trees_count += 1
		x_pos += num_right
		x_pos = x_pos % matrix_width
		
		y_pos += num_down

	return trees_count 

if __name__ == "__main__":
	parsed_board = parse_geology()
	tree_count_3_1 = calculate_num_trees(3, 1, parsed_board)
	print('The answer to day 3 part 1 is {}.'.format(tree_count_3_1))

	tree_count_1_1 = calculate_num_trees(1, 1, parsed_board)
	tree_count_5_1 = calculate_num_trees(5, 1, parsed_board)
	tree_count_7_1 = calculate_num_trees(7, 1, parsed_board)
	tree_count_1_2 = calculate_num_trees(1, 2, parsed_board)

	tree_product = tree_count_3_1 * tree_count_1_1 * tree_count_5_1 * \
		tree_count_7_1 * tree_count_1_2
	print('The answer to day 3 part 2 is {}.'.format(tree_product))