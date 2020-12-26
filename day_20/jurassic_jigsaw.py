def parse_input():
	with open('input.txt', 'r') as f:
		input_lines = f.read().split('\n\n')[:-1]

	tile_list = [tile.split(':\n') for tile in input_lines]
	tile_list = [(tile[0], tile[1].split('\n')) for tile in tile_list]
	tile_dict = {tile_id: [list(tile_row) for tile_row in tile_val]
		for (tile_id, tile_val) in tile_list}
	return tile_dict

def calc_tile_boundaries_no_flips(tile_val):
	boundary_list = [('top', tile_val[0]), ('bottom', tile_val[-1][::-1]),
		('left', [tile_row[0] for tile_row in tile_val][::-1]),
		('right', [tile_row[-1] for tile_row in tile_val])]
	return boundary_list

def calc_tile_boundaries_with_flips(tile_val):
	boundary_list = calc_tile_boundaries_no_flips(tile_val)
	flipped_boundary_list = [(label + ' flipped', val[::-1]) 
		for (label, val) in boundary_list]
	return boundary_list + flipped_boundary_list

def find_two_tile_matches(tile1_val, tile2_val):
	tile1_boundary_list = calc_tile_boundaries_no_flips(tile1_val)
	tile2_boundary_list = calc_tile_boundaries_with_flips(tile2_val)

	match_list = []
	for orientation_1 in tile1_boundary_list:
		for orientation_2 in tile2_boundary_list:
			if orientation_1[1] == orientation_2[1]:
				match_list += [(orientation_1[0], orientation_2[0])]
	return match_list

def find_all_tile_matches_per_tile(curr_tile_id, curr_tile_val, parsed_input):
	total_match_list = []
	for loop_tile_id, loop_tile_val in parsed_input.items():
		if loop_tile_id != curr_tile_id:
			match_list = find_two_tile_matches(curr_tile_val, loop_tile_val)
			if len(match_list) > 0:
				total_match_list += [(loop_tile_id, match_list)]
	return total_match_list

def calculate_tile_matching_dict(parsed_input):
	matched_tile_dict = {}
	for tile_id, tile_val in parsed_input.items():
		curr_tile_matches = \
			find_all_tile_matches_per_tile(tile_id, tile_val, parsed_input)
		matched_tile_dict[tile_id] = curr_tile_matches
	return matched_tile_dict

def validate_num_tile_matches(parsed_input):
	tile_matching_dict = calculate_tile_matching_dict(parsed_input)
	tile_num_matches_dict = {}
	single_match_per_piece = True
	for tile_id, tile_matches in tile_matching_dict.items():
		for match in tile_matches:
			single_match_per_piece = single_match_per_piece and (len(match[1]) == 1)

		num_tile_matches = len(tile_matches)
		if num_tile_matches not in tile_num_matches_dict:
			tile_num_matches_dict[num_tile_matches] = 1
		else:
			tile_num_matches_dict[num_tile_matches] += 1
	return tile_num_matches_dict, single_match_per_piece

def calculate_corner_product(parsed_input):
	tile_matching_dict = calculate_tile_matching_dict(parsed_input)
	final_product = 1

	for tile_id, tile_matches in tile_matching_dict.items():
		if len(tile_matches) == 2:
			final_product *= int(tile_id[5:])

	return final_product

def remove_tile_boundaries(tile_array):
	tile_array_removed = [[[tile_row[1:-1] for tile_row in tile[1:-1]] 
		for tile in rows_of_tiles] for rows_of_tiles in tile_array]

	return tile_array_removed

def convert_arrays_to_combined_tiles(tile_array):
	tile_array_removed = remove_tile_boundaries(tile_array)

	array_with_joined_tile_row = [[[''.join(tile_row) for tile_row in tile] 
		for tile in rows_of_tiles] for rows_of_tiles in tile_array_removed]

	array_with_joined_rows_of_tiles = [[''.join([tile[i] for tile in rows_of_tiles]) 
		for i in range(len(rows_of_tiles[0][0]))] 
		for rows_of_tiles in array_with_joined_tile_row]

	final_array = [water_row for tile_row in array_with_joined_rows_of_tiles 
		for water_row in tile_row]

	return final_array

def calc_orientation_swap(orig_dir, final_dir):
	orig_split = orig_dir.split(' ')
	final_split = final_dir.split(' ')

	flipped_orig = (len(orig_split) == 2)
	flipped_final = (len(final_split) == 2)

	orientation_list = ['top', 'right', 'bottom', 'left']

	orig_orientation_index = orientation_list.index(orig_split[0])
	final_orientation_index = orientation_list.index(final_split[0])

	num_rotations = (final_orientation_index - orig_orientation_index) % 4
	
	if not (flipped_orig ^ flipped_final):
		flip_val = 'none'
	else:
		if final_split[0] in {'right', 'left'}:
			flip_val = 'vertical'
		else:
			flip_val = 'horizontal'

	return num_rotations, flip_val

def calc_new_orientation_dir(orig_dir, num_rotations, flip_val):
	orientation_list = ['top', 'right', 'bottom', 'left']

	orig_split = orig_dir.split(' ')

	orig_index = orientation_list.index(orig_split[0])
	new_index = (orig_index + num_rotations) % 4
	new_dir = orientation_list[new_index]

	vertical_flip_map = {'top': 'bottom flipped', 'bottom': 'top flipped',
		'right': 'right flipped', 'left': 'left flipped'}
	horizontal_flip_map = {'top': 'top flipped', 'bottom': 'bottom flipped',
		'right': 'left flipped', 'left': 'right flipped'}

	if flip_val == 'vertical':
		new_dir = vertical_flip_map[new_dir]
		if len(orig_split) == 2:
			new_dir = new_dir.split(' ')[0]
	elif flip_val == 'horizontal':
		new_dir = horizontal_flip_map[new_dir]
		if len(orig_split) == 2:
			new_dir = new_dir.split(' ')[0]
	else:
		if len(orig_split) == 2:
			new_dir += ' flipped'

	return new_dir

def reorient_tile(tile, num_rotations, flip_val):
	new_tile = tile
	for i in range(num_rotations):
		new_tile = [[tile_row[i] for tile_row in new_tile][::-1] 
			for i in range(len(new_tile[0]))]

	if flip_val == 'vertical':
		new_tile = new_tile[::-1]
	elif flip_val == 'horizontal':
		new_tile = [tile_row[::-1] for tile_row in new_tile]
	return new_tile

def combine_tiles_together(tile_matching_dict, parsed_input):
	for tile_id, tile_matches in tile_matching_dict.items():
		if len(tile_matches) == 2:
			init_tile_id = tile_id
			init_tile_matches = tile_matches
			break
	init_tile_val = parsed_input[init_tile_id]

	adjacent_dir_set = {init_tile_matches[0][1][0][0],init_tile_matches[1][1][0][0]}

	if adjacent_dir_set == {'right', 'top'}:
		curr_pos = (0, 11)
	elif adjacent_dir_set == {'top', 'left'}:
		curr_pos = (11, 11)
	elif adjacent_dir_set == {'left', 'bottom'}:
		curr_pos = (11, 0)
	elif adjacent_dir_set == {'bottom', 'right'}:
		curr_pos = (0, 0)
	else:
		raise InvalidArgumentError()

	opposite_dir_dict = {'top': 'bottom flipped', 'bottom': 'top flipped',
		'right': 'left flipped', 'left': 'right flipped'}

	visited_set = {init_tile_id}
	curr_tile_stack = [(init_tile_id, init_tile_matches, curr_pos)]
	tile_array = [[None]*12 for i in range(12)]
	tile_array[curr_pos[1]][curr_pos[0]] = init_tile_val

	while len(curr_tile_stack) > 0:
		curr_tile = curr_tile_stack.pop()
		curr_tile_id = curr_tile[0]
		curr_tile_matches = curr_tile[1]
		curr_pos = curr_tile[2]
		for adj_tile in curr_tile_matches:
			adj_tile_id = adj_tile[0]
			adj_tile_dirs = adj_tile[1][0]
			adj_tile_val = parsed_input[adj_tile_id]
			if adj_tile_id not in visited_set:
				new_adj_tile_dir = opposite_dir_dict[adj_tile_dirs[0]]
				adj_tile_matches = tile_matching_dict[adj_tile_id]

				num_rotations, flip_val = \
					calc_orientation_swap(adj_tile_dirs[1], new_adj_tile_dir) 
				reoriented_adj_tile = \
					reorient_tile(adj_tile_val, num_rotations, flip_val)
				
				new_adj_tile_matches = []
				for match in adj_tile_matches:
					matched_id = match[0]
					matched_dirs = match[1]

					curr_match_dir = matched_dirs[0][0]
					other_match_dir = matched_dirs[0][1]
					new_curr_match_dir = calc_new_orientation_dir(matched_dirs[0][0],
																num_rotations, flip_val)
					new_other_match_dir = other_match_dir
					if new_curr_match_dir[-7:] == 'flipped':
						if new_other_match_dir[-7:] == 'flipped':
							new_other_match_dir = new_other_match_dir.split(' ')[0]
						else:
							new_other_match_dir += ' flipped'
						new_curr_match_dir = new_curr_match_dir.split(' ')[0]

					new_adj_tile_matches += \
						[(matched_id, [(new_curr_match_dir, new_other_match_dir)])]

				if adj_tile_dirs[0] == 'top':
					new_pos = (curr_pos[0], curr_pos[1]-1)
				elif adj_tile_dirs[0] == 'bottom':
					new_pos = (curr_pos[0], curr_pos[1]+1)
				elif adj_tile_dirs[0] == 'right':
					new_pos = (curr_pos[0]+1, curr_pos[1])
				elif adj_tile_dirs[0] == 'left':
					new_pos = (curr_pos[0]-1, curr_pos[1])
				else:
					raise InvalidArgumentError()

				tile_array[new_pos[1]][new_pos[0]] = reoriented_adj_tile
				visited_set.add(adj_tile_id)
				curr_tile_stack += [(adj_tile_id, new_adj_tile_matches, new_pos)]
	
	final_combined_tiles = convert_arrays_to_combined_tiles(tile_array)
	return final_combined_tiles

def calc_num_monsters_curr_orientation(image):
	sea_monster_str = ['                  # ', 
					   '#    ##    ##    ###', 
					   ' #  #  #  #  #  #   ']
	sea_monster_indices = [(row,col) for row in range(len(sea_monster_str)) 
		for col in range(len(sea_monster_str[0])) if sea_monster_str[row][col] == '#']

	num_cols_monster = len(sea_monster_str[0])
	num_rows_monster = len(sea_monster_str)

	num_cols_image = len(image[0])
	num_rows_image = len(image)

	monster_count = 0
	for i in range(num_rows_image-num_rows_monster+1):
		for j in range(num_cols_image-num_cols_monster+1):
			potential_monster = [image_row[j:j+num_cols_monster]
				for image_row in image[i:i+num_rows_monster]]
			is_monster = True
			for (row, col) in sea_monster_indices:
				if potential_monster[row][col] != '#':
					is_monster = False
					break
			if is_monster:
				monster_count += 1

	return monster_count

def calc_num_monsters(image):
	possible_orientations = (reorient_tile(image, num_rotations, flipped_val)
		for num_rotations in range(4) for flipped_val in ['none', 'vertical'])

	for oriented_tile in possible_orientations:
		num_monsters = calc_num_monsters_curr_orientation(oriented_tile)
		if num_monsters > 0:
			return num_monsters
	return 0

def find_image_roughness(image):
	num_monsters = calc_num_monsters(image)
	total_pounds = sum([image_row.count('#') for image_row in image])
	# 15 is number of number of pound signs in sea monster
	return total_pounds - 15 * num_monsters

def calculate_tile_puzzle_roughness(parsed_input):
	tile_matching_dict = calculate_tile_matching_dict(parsed_input)
	consolidated_tiles = combine_tiles_together(tile_matching_dict, parsed_input)
	num_pounds = find_image_roughness(consolidated_tiles)

	return num_pounds

if __name__ == '__main__':
	parsed_input = parse_input()
	# The below makes clear that there is only one possible way to connect pieces and namely
	# a naive algorithm of just finding two pieces that match and building iteratively
	# will work if there exists a solution. It also shows that such a solution must be
	# of size 12 x 12.
	num_matches_dict, pairs_of_pieces_bool = validate_num_tile_matches(parsed_input)
	for i, v in num_matches_dict.items():
		print('The number of tiles with {} matches is {}.'.format(i, v))

	if pairs_of_pieces_bool:
		print('Every pair of tiles matches in at most one way.')

	corner_product = calculate_corner_product(parsed_input)
	print('The answer to the puzzle on Day 20 Part 1 is {}.'\
		.format(corner_product))

	final_roughness = calculate_tile_puzzle_roughness(parsed_input)
	print('The answer to the puzzle on Day 20 Part 2 is {}.'\
		.format(final_roughness))
