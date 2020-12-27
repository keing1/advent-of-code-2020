def parse_seating():
	with open('input.txt', 'r') as f:
		seating_arr = f.read().split('\n')[:-1]

	seating_arr = [list(row) for row in seating_arr]

	return seating_arr

def find_num_visible(seating_arr, row, col, use_update_one):
	adj_dir_tuples = [(1,0), (0,1), (-1,0), (0,-1), 
			(1,1), (1,-1), (-1,1), (-1,-1)]
	if use_update_one:
		adj_tuples = [(row+row_diff, col+col_diff) 
			for (row_diff, col_diff) in adj_dir_tuples]
		adj_tuples = [(i_val,j_val) for (i_val,j_val) in adj_tuples 
			if 0 <= i_val < len(seating_arr) and 0 <= j_val < len(seating_arr[0])]
		adj_seats = [seating_arr[i_val][j_val] for (i_val,j_val) in adj_tuples]
		num_adj = adj_seats.count('#')
		return num_adj
	else:
		num_vis = 0
		for (row_diff, col_diff) in adj_dir_tuples:
			row_val = row + row_diff
			col_val = col + col_diff
			while 0 <= row_val < len(seating_arr) and \
				0 <= col_val < len(seating_arr[0]):
				seat_type = seating_arr[row_val][col_val]
				if seat_type == '#':
					num_vis += 1
					break
				elif seat_type == 'L':
					break
				row_val += row_diff
				col_val += col_diff

		return num_vis

def find_update_char(seat_type, num_vis, use_update_one):
	if use_update_one:
		if seat_type == '#':
			if num_vis >= 4:
				update_char = 'L'
			else:
				update_char = '#'
		else:
			if num_vis == 0:
				update_char = '#'
			else:
				update_char = 'L'
	else:
		if seat_type == '#':
			if num_vis >= 5:
				update_char = 'L'
			else:
				update_char = '#'
		else:
			if num_vis == 0:
				update_char = '#'
			else:
				update_char = 'L'
	return update_char

def update_seating(seating_arr, use_update_one):
	new_seating = [[None for j in range(len(seating_arr[0]))] for i in range(len(seating_arr))]
	for i in range(len(seating_arr)):
		for j in range(len(seating_arr[0])):
			seat_type = seating_arr[i][j]
			if seat_type != '.':
				num_vis = find_num_visible(seating_arr, i, j, use_update_one)
				new_seating[i][j] = find_update_char(seat_type, num_vis, use_update_one)
			else:
				new_seating[i][j] = '.'
	return new_seating

def find_final_occupied(seating_arr, use_update_one):
	curr_seating = seating_arr
	
	while True:
		new_seating = update_seating(curr_seating, use_update_one)
		if new_seating == curr_seating:
			break
		curr_seating = new_seating

	total_occupied = sum(row.count('#') for row in new_seating)
	return total_occupied

if __name__ == '__main__':
	seating_arr = parse_seating()
	total_occupied = find_final_occupied(seating_arr, True)
	print('The answer to the puzzle on Day 11 Part 1 is {}.'.format(total_occupied))

	total_occupied_two = find_final_occupied(seating_arr, False)
	print('The answer to the puzzle on Day 11 Part 2 is {}.'.format(total_occupied_two))