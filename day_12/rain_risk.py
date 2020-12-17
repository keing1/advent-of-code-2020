def parse_actions():
	with open('input.txt', 'r') as f:
		actions_list = f.read().split('\n')[:-1]

	parsed_actions = [(action[0], int(action[1:])) for 
		action in actions_list]

	return parsed_actions

def update_state_one(current_state, action):
	action_type = action[0]
	action_val = action[1]

	curr_dir = current_state[0]
	curr_pos = current_state[1]

	right_order_list = ['N', 'E', 'S', 'W']
	left_order_list = ['N', 'W', 'S', 'E']
	if action_type == 'N':
		return [curr_dir, [curr_pos[0], curr_pos[1]+action_val]]
	elif action_type == 'S':
		return [curr_dir, [curr_pos[0], curr_pos[1]-action_val]]
	elif action_type == 'E':
		return [curr_dir, [curr_pos[0]+action_val, curr_pos[1]]]
	elif action_type == 'W':
		return [curr_dir, [curr_pos[0]-action_val, curr_pos[1]]]
	elif action_type == 'L':
		left_list_ind = left_order_list.index(curr_dir)
		num_steps = action_val // 90
		left_list_ind_new = (left_list_ind + num_steps) % 4
		new_dir = left_order_list[left_list_ind_new]
		return [new_dir, curr_pos]
	elif action_type == 'R':
		right_list_ind = right_order_list.index(curr_dir)
		num_steps = action_val // 90
		right_list_ind_new = (right_list_ind + num_steps) % 4
		new_dir = right_order_list[right_list_ind_new]
		return [new_dir, curr_pos]
	else:
		if curr_dir == 'E':
			return [curr_dir, [curr_pos[0]+action_val, curr_pos[1]]]
		elif curr_dir == 'W':
			return [curr_dir, [curr_pos[0]-action_val, curr_pos[1]]]
		elif curr_dir == 'S':
			return [curr_dir, [curr_pos[0], curr_pos[1]-action_val]]
		else:
			return [curr_dir, [curr_pos[0], curr_pos[1]+action_val]]


def calculate_final_distance_one(parsed_actions):
	curr_state = ['E', [0, 0]]

	for action in parsed_actions:
		curr_state = update_state_one(curr_state, action)

	return abs(curr_state[1][0]) + abs(curr_state[1][1])

def update_state_two(current_state, action):
	action_type = action[0]
	action_val = action[1]

	curr_dir = current_state[0]
	curr_pos = current_state[1]
	rel_way_pos = current_state[2]
	
	if action_type == 'N':
		return [curr_dir, curr_pos, [rel_way_pos[0], rel_way_pos[1]+action_val]]
	elif action_type == 'S':
		return [curr_dir, curr_pos, [rel_way_pos[0], rel_way_pos[1]-action_val]]
	elif action_type == 'E':
		return [curr_dir, curr_pos, [rel_way_pos[0]+action_val, rel_way_pos[1]]]
	elif action_type == 'W':
		return [curr_dir, curr_pos, [rel_way_pos[0]-action_val, rel_way_pos[1]]]
	elif action_type == 'L':
		if action_val == 90:
			return [curr_dir, curr_pos, [-rel_way_pos[1], rel_way_pos[0]]]
		elif action_val == 180:
			return [curr_dir, curr_pos, [-rel_way_pos[0], -rel_way_pos[1]]]
		elif action_val == 270:
			return [curr_dir, curr_pos, [rel_way_pos[1], -rel_way_pos[0]]]
	elif action_type == 'R':
		if action_val == 90:
			return [curr_dir, curr_pos, [rel_way_pos[1], -rel_way_pos[0]]]
		elif action_val == 180:
			return [curr_dir, curr_pos, [-rel_way_pos[0], -rel_way_pos[1]]]
		elif action_val == 270:
			return [curr_dir, curr_pos, [-rel_way_pos[1], rel_way_pos[0]]]
	else:
		east_amount = rel_way_pos[0]*action_val
		north_amount = rel_way_pos[1]*action_val
		return [curr_dir, [curr_pos[0]+east_amount, curr_pos[1]+north_amount], rel_way_pos]

def calculate_final_distance_two(parsed_actions):
	curr_state = ['E', [0, 0], [10, 1]]

	for action in parsed_actions:
		curr_state = update_state_two(curr_state, action)

	return abs(curr_state[1][0]) + abs(curr_state[1][1])

if __name__ == '__main__':
	parsed_actions = parse_actions()
	final_dist = calculate_final_distance_one(parsed_actions)
	print('The answer to the puzzle on Day 12 Part 1 is {}.'.format(final_dist))

	final_dist_two = calculate_final_distance_two(parsed_actions)
	print('The answer to the puzzle on Day 12 Part 2 is {}.'.format(final_dist_two))