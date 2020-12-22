from functools import reduce

def parse_rule_line(rule_line):
	rule_line_split_one = rule_line.split(': ')
	rule_key = rule_line_split_one[0]
	rule_line_split_two = rule_line_split_one[1].split(' or ')
	
	range_one_str = rule_line_split_two[0]
	range_two_str = rule_line_split_two[1]

	range_one_list = range_one_str.split('-')
	range_one_list = [int(num) for num in range_one_list]

	range_two_list = range_two_str.split('-')
	range_two_list = [int(num) for num in range_two_list]

	return [rule_key, range_one_list, range_two_list]

def parse_ticket_inputs():
	with open('input.txt', 'r') as f:
		rules_list = []

		init_rules = True
		new_line = f.readline()
		while new_line != '\n':
			rules_list += [parse_rule_line(new_line)]
			new_line = f.readline()

		f.readline()
		my_ticket_list = f.readline()[:-1].split(',')
		my_ticket_list = [int(num) for num in my_ticket_list]

		f.readline()
		f.readline()

		nearby_ticket_str_list = f.read().split('\n')[:-1]
		nearby_ticket_lists = [my_str.split(',') for my_str in nearby_ticket_str_list]
		nearby_ticket_int_lists = [[int(a) for a in b] for b in nearby_ticket_lists]

	return rules_list, my_ticket_list, nearby_ticket_int_lists

def make_valid_num_set(rules_list):
	valid_num_set = set()
	for rule in rules_list:
		range_one = rule[1]
		range_two = rule[2]
		for num in range(range_one[0], range_one[1]+1):
			valid_num_set.add(num)
		for num in range(range_two[0], range_two[1]+1):
			valid_num_set.add(num)
	return valid_num_set

def calc_total_invalid_sum(rules_list, nearby_ticket_lists):
	valid_num_set = make_valid_num_set(rules_list)

	agg_sum = 0

	for ticket in nearby_ticket_lists:
		agg_sum += sum([num for num in ticket if num not in valid_num_set])
		
	return agg_sum

def remove_invalid_tickets(rules_list, nearby_ticket_lists):
	valid_num_set = make_valid_num_set(rules_list)

	valid_ticket_list = []

	for ticket in nearby_ticket_lists:
		if len([num for num in ticket if num not in valid_num_set]) == 0:
			valid_ticket_list += [ticket]

	return valid_ticket_list

def determine_valid_rules_for_pos(rules_list, valid_ticket_list):
	transposed_ticket_list = [[ticket[num] for ticket in valid_ticket_list] 
		for num in range(len(valid_ticket_list[0]))]

	valid_rule_set_list = []
	for pos_list in transposed_ticket_list:
		valid_rule_set = set()
		for i, rule in enumerate(rules_list):
			range_1 = rule[1]
			range_2 = rule[2]
			valid_rule = True
			for num in pos_list:
				if (range_1[0] <= num <= range_1[1]) or  (range_2[0] <= num <= range_2[1]):
					continue
				else:
					valid_rule = False
			if valid_rule:
				valid_rule_set.add(i)
		valid_rule_set_list += [valid_rule_set]
	return valid_rule_set_list

def find_rules_with_departure(rules_list):
	departure_set = set()
	for i, rule in enumerate(rules_list):
		if 'departure' in rule[0]:
			departure_set.add(i)
	return departure_set


def calc_ticket_product(rules_list, my_ticket_list, nearby_ticket_lists):
	valid_ticket_list = remove_invalid_tickets(rules_list, nearby_ticket_lists)

	valid_rule_set_list = determine_valid_rules_for_pos(rules_list, valid_ticket_list)

	unpicked_set = set(range(len(rules_list)))
	final_rule_dict = {}

	while len(unpicked_set) > 0:
		rule_val = None
		for i, valid_rule_set in enumerate(valid_rule_set_list):
			# There is an argument that this works as long as there is a unique
			# solution to the problem
			if len(valid_rule_set) == 1:
				rule_val = list(valid_rule_set)[0]
				final_rule_dict[rule_val] = i
				unpicked_set.remove(rule_val)
				break

		for valid_rule_set in valid_rule_set_list:
			if rule_val in valid_rule_set:
				valid_rule_set.remove(rule_val)

	rules_with_departure = find_rules_with_departure(rules_list)
	cols_with_departure = [final_rule_dict[rule] for rule in rules_with_departure]
	my_ticket_nums = [my_ticket_list[col] for col in cols_with_departure]


	return reduce(lambda x, y: x*y, my_ticket_nums, 1)

if __name__ == '__main__':
	rules_list, my_ticket_list, nearby_ticket_lists = parse_ticket_inputs()

	total_invalid_sum = calc_total_invalid_sum(rules_list, nearby_ticket_lists)
	print('The answer to the puzzle on Day 16 Part 1 is {}.'.format(total_invalid_sum))

	ticket_product = calc_ticket_product(rules_list, my_ticket_list, nearby_ticket_lists)
	print('The answer to the puzzle on Day 16 Part 2 is {}.'.format(ticket_product))