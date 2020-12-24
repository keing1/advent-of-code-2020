import math
import numpy as np
import copy

def parse_line(line):
	dir_list = ['e', 'se', 'sw', 'w', 'nw', 'ne']

	direction_list = []
	curr_dir = ''
	for char in line:
		curr_dir += char
		if curr_dir in dir_list:
			direction_list += [curr_dir]
			curr_dir = ''

	return direction_list

def parse_input():
	with open('input.txt', 'r') as f:
		tile_list = f.read().split('\n')[:-1]

	tile_dir_lists = [parse_line(line) for line in tile_list]

	return tile_dir_lists

def calc_pos(tile_dir_list):
	curr_pos = (0,0)

	for dir in tile_dir_list:
		if dir == 'e':
			curr_pos = (curr_pos[0]+1, curr_pos[1])
		elif dir == 'se':
			curr_pos = (curr_pos[0]+1, curr_pos[1]-1)
		elif dir == 'sw':
			curr_pos = (curr_pos[0], curr_pos[1]-1)
		elif dir == 'w':
			curr_pos = (curr_pos[0]-1, curr_pos[1])
		elif dir == 'nw':
			curr_pos = (curr_pos[0]-1,curr_pos[1]+1)
		else:
			curr_pos = (curr_pos[0],curr_pos[1]+1)

	return curr_pos

def find_flipped_tiles(parsed_input):
	flip_set = set()

	for tile_dir_list in parsed_input:
		x_pos, y_pos = calc_pos(tile_dir_list)

		if (x_pos, y_pos) in flip_set:
			flip_set.remove((x_pos, y_pos))
		else:
			flip_set.add((x_pos, y_pos))

	return flip_set, len(flip_set)

def run_step(flip_set):
	flip_list = list(flip_set)
	max_x = max([tile[0] for tile in flip_list])
	max_y = max([tile[1] for tile in flip_list])
	min_x = min([tile[0] for tile in flip_list])
	min_y = min([tile[1] for tile in flip_list])

	flip_set_copy = copy.deepcopy(flip_set)

	for x_coord in range(min_x-1, max_x+2):
		for y_coord in range(min_y-1, max_y+2):
			if (x_coord, y_coord) in flip_set:
				curr_color = 'black'
			else:
				curr_color = 'white'

			adjacent_tiles = [(x_coord+1, y_coord), (x_coord-1, y_coord),
				(x_coord, y_coord+1), (x_coord, y_coord-1),
				(x_coord+1, y_coord-1), (x_coord-1, y_coord+1)]

			num_adjacent = 0
			for tile in adjacent_tiles:
				if tile in flip_set:
					num_adjacent += 1

			if curr_color == 'black':
				if num_adjacent == 0 or num_adjacent > 2:
					flip_set_copy.remove((x_coord, y_coord))
			else:
				if num_adjacent == 2:
					flip_set_copy.add((x_coord, y_coord))

	return flip_set_copy

def run_tiles(num_steps, parsed_input):
	flip_set, num_flipped = find_flipped_tiles(parsed_input)
	for step in range(num_steps):
		flip_set = run_step(flip_set)

	return len(flip_set)

if __name__ == '__main__':
	parsed_input = parse_input()

	flip_set, num_flipped = find_flipped_tiles(parsed_input)
	print('The answer to the puzzle on Day 24 Part 1 is {}.'\
		.format(num_flipped))

	num_flipped_part_two = run_tiles(100, parsed_input)
	print('The answer to the puzzle on Day 24 Part 2 is {}.'\
		.format(num_flipped_part_two))
