import math

input_one = [1,6,7,2,4,8,3,5,9]

class Node:
	def __init__(self, val, next=None):
		self.val = val
		self.next = next

def convert_list_to_looped_ll(input_list):
	ll_dict = {}
	init_num = input_list[0]

	init_node = Node(init_num)
	curr_node = init_node
	ll_dict[init_num] = init_node
	max_num = init_num
	for num in input_list[1:]:
		new_node = Node(num)
		ll_dict[num] = new_node
		max_num = max(num, max_num)
		
		curr_node.next = new_node
		curr_node = new_node
	curr_node.next = init_node

	return init_node, ll_dict, max_num

def print_ll(init_node):
	node_list = [init_node.val]

	curr_node = init_node.next
	while curr_node is not init_node:
		node_list += [curr_node.val]
		curr_node = curr_node.next
	print(node_list)
	return

def generate_part_one_input_ll():
	return convert_list_to_looped_ll(input_one)

def generate_part_two_input_ll():
	max_one = max(input_one)
	input_two = input_one + list(range(max_one+1,1000001))

	return convert_list_to_looped_ll(input_two)

def game_step(curr_node, ll_dict, max_num):
	move_node_1 = curr_node.next
	move_node_2 = move_node_1.next
	move_node_3 = move_node_2.next
	move_node_val_list = [move_node_1.val, move_node_2.val, move_node_3.val]

	next_node = move_node_3.next

	curr_val = curr_node.val

	destination_val = curr_val-1
	if destination_val == 0:
		destination_val += max_num

	while destination_val in move_node_val_list:
		destination_val -= 1
		if destination_val == 0:
			destination_val += max_num

	destination_node = ll_dict[destination_val]
	after_destination_node = destination_node.next

	destination_node.next = move_node_1
	move_node_3.next = after_destination_node
	
	curr_node.next = next_node

	return next_node, ll_dict, max_num

def find_node_one(curr_node):
	while curr_node.val != 1:
		curr_node = curr_node.next

	return curr_node

def find_final_ordering(num_steps, curr_node, ll_dict, max_num):
	for step in range(num_steps):
		curr_node, ll_dict, max_num = game_step(curr_node, ll_dict, max_num)

	one_node = find_node_one(curr_node)

	loop_node = one_node.next
	final_cup_str = ''
	while loop_node is not one_node:
		final_cup_str += str(loop_node.val)
		loop_node = loop_node.next

	return final_cup_str

def find_star_cup_product(num_steps, curr_node, ll_dict, max_num):
	for step in range(num_steps):
		curr_node, ll_dict, max_num = game_step(curr_node, ll_dict, max_num)

	one_node = find_node_one(curr_node)

	val_one = one_node.next.val
	val_two = one_node.next.next.val

	return val_one * val_two

if __name__ == '__main__':
	part_one_first_cup, part_one_ll_dict, part_one_max = generate_part_one_input_ll()

	final_ordering = find_final_ordering(100, part_one_first_cup, part_one_ll_dict,
		part_one_max)
	print('The answer to the puzzle on Day 23 Part 1 is {}.'\
		.format(final_ordering))

	part_two_first_cup, part_two_ll_dict, part_two_max = generate_part_two_input_ll()

	final_star_product = find_star_cup_product(10000000, part_two_first_cup,
		part_two_ll_dict, part_two_max)
	print('The answer to the puzzle on Day 23 Part 2 is {}.'\
		.format(final_star_product))
