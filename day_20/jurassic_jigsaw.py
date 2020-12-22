def parse_input():
	with open('input.txt', 'r') as f:
		input_lines = f.read().split('\n\n')[:-1]

	tile_list = [tile.split(':\n') for tile in input_lines]
	tile_list = [(tile[0], tile[1].split('\n')) for tile in tile_list]
	tile_list = [(tile_id, [list(tile_row) for tile_row in tile_val])
		for (tile_id, tile_val) in tile_list]

	return tile_list

def calc_tile_boundaries_no_flips(tile_val):
	boundary_list = []
	boundary_list += [('top', tile_val[0])]
	boundary_list += [('bottom', tile_val[-1])]
	boundary_list += [('left',[tile_row[0] for tile_row in tile_val])]
	boundary_list += [('right', [tile_row[-1] for tile_row in tile_val])]

	return boundary_list

def calc_tile_boundaries_with_flips(tile_val):
	boundary_list = calc_tile_boundaries_no_flips(tile_val)
	flipped_boundary_list = [(label + ' flipped', val[::-1]) 
		for (label, val) in boundary_list]

	total_boundary_list = boundary_list + flipped_boundary_list

	return total_boundary_list

def find_two_tile_matches(tile1, tile2):
	tile1_boundary_list = calc_tile_boundaries_no_flips(tile1[1])
	tile2_boundary_list = calc_tile_boundaries_with_flips(tile2[1])

	match_list = []

	for orientation_1 in tile1_boundary_list:
		for orientation_2 in tile2_boundary_list:
			if orientation_1[1] == orientation_2[1]:
				match_list += [(orientation_1[0], orientation_2[0])]

	return match_list


def find_all_tile_matches_per_tile(curr_tile, parsed_input):
	curr_tile_id = curr_tile[0]
	curr_tile_val = curr_tile[1]

	total_match_list = []

	for loop_tile in parsed_input:
		if loop_tile[0] != curr_tile_id:
			match_list = find_two_tile_matches(curr_tile, loop_tile)
			if len(match_list) > 0:
				total_match_list += [((curr_tile_id, loop_tile[0]), match_list)]
	return total_match_list

def validate_num_tile_matches(parsed_input):
	tile_num_matches_dict = {}
	for tile in parsed_input:
		tile_matches = find_all_tile_matches_per_tile(tile, parsed_input)
		num_tile_matches = len(tile_matches)
		if num_tile_matches not in tile_num_matches_dict:
			tile_num_matches_dict[num_tile_matches] = 1
		else:
			tile_num_matches_dict[num_tile_matches] += 1
	return tile_num_matches_dict

def calc_num_monsters_curr_orientation(image):
	sea_monster_str = ['                  # ', 
					   '#    ##    ##    ###', 
					   ' #  #  #  #  #  #   ']

	num_cols_monster = len(sea_monster_str[0])
	num_rows_monster = len(sea_monster_str)

	num_cols_image = len(image[0])
	num_rows_image = len(image)

	monster_count = 0
	for i in range(num_rows_image-num_rows_monster+1):
		for j in range(num_cols_image-num_cols_monster+1):
			potential_monster = [image_row[j:j+num_cols_monster]
				for image_row in image[i:i+num_rows_monster]]
			if potential_monster == sea_monster_str:
				monster_count += 1

	return monster_count

def calc_num_monsters(image):
	image_curr_orientation = image

	num_monsters = calc_num_monsters_curr_orientation(image)
	if num_monsters > 0:
		return num_monsters
	
	upside_down_image = image[::-1]
	num_monsters = calc_num_monsters_curr_orientation(upside_down_image)
	if num_monsters > 0:
		return num_monsters

	flipped_left_right_image = [image_row[::-1] for image_row in image]
	num_monsters = calc_num_monsters_curr_orientation(flipped_left_right_image)
	if num_monsters > 0:
		return num_monsters

	upside_down_flipped_image = [image_row[::-1] for image_row in upside_down_image]
	num_monsters = calc_num_monsters_curr_orientation(flipped_left_right_image)
	if num_monsters > 0:
		return num_monsters

	rotate_right_image = [[image_row[i] for image_row in image] 
		for i in range(len(image[0]))]
	num_monsters = calc_num_monsters_curr_orientation(rotate_right_image)
	if num_monsters > 0:
		return num_monsters

	rotate_left_image = [[image_row[i] for image_row in image] 
		for i in range(len(image[0])-1, -1, -1)]
	num_monsters = calc_num_monsters_curr_orientation(rotate_left_image)
	if num_monsters > 0:
		return num_monsters

	flipped_rotate_right_image = [image_row[::-1] 
		for image_row in flipped_rotate_right_image]
	num_monsters = calc_num_monsters_curr_orientation(flipped_rotate_right_image)
	if num_monsters > 0:
		return num_monsters

	flipped_rotate_left_image = [image_row[::-1]
		for image_row in flipped_rotate_left_image]
	num_monsters = calc_num_monsters_curr_orientation(flipped_rotate_left_image)
	if num_monsters > 0:
		return num_monsters

	return None

def find_image_roughness(image):
	num_monsters = calc_num_monsters(image)

	total_pounds = sum([image_row.count('#') for image_row in image])

	# 15 is number of number signs in sea monster
	return total_pounds - 15 * num_monsters

def output_num_matches(parsed_input):
	for tile in parsed_input:
		print(find_all_tile_matches_per_tile(tile, parsed_input))
		print(len(find_all_tile_matches_per_tile(tile, parsed_input)))
	return

parsed_input = parse_input()
print(validate_num_tile_matches(parsed_input))
