import copy

def parse_rule_line(rule_line):
	[rule_num, match] = rule_line.split(': ')
	if '\"' in match:
		return rule_num, match[1]
	match_list = match.split(' | ')
	match_tuple_list = [match.split(' ') for match in match_list]
	return rule_num, match_tuple_list

def parse_input():
	with open('input.txt', 'r') as f:
		data_split = f.read().split('\n\n')
	rule_list = data_split[0].split('\n')
	rule_dict = {}
	for rule in rule_list:
		rule_num, match = parse_rule_line(rule)
		rule_dict[rule_num] = match

	string_list = data_split[1].split('\n')[:-1]

	return rule_dict, string_list

def combined_rule_list(rule_to_string_dict, match_list):
	set_list = [rule_to_string_dict[match] for match in match_list]
	
	if len(set_list) == 1:
		return set_list[0]
	elif len(set_list) == 2:
		combined_set_list = {rule_start + rule_end for rule_start in set_list[0]
			for rule_end in set_list[1]}
		return combined_set_list
	else:
		raise ValueError()

def create_rule_to_string_dict(rule_dict):
	new_rule_dict = copy.deepcopy(rule_dict)
	rule_to_string_dict = {}
	while '0' not in rule_to_string_dict:
		rule_dict_drop_list = []
		for i, v in new_rule_dict.items():
			if type(v) is str:
				rule_dict_drop_list += [i]
				rule_to_string_dict[i] = {v}
			elif type(v) is list:
				flattened_rule_references = [num for sublist in v for num in sublist]
				if all(num in rule_to_string_dict for num in flattened_rule_references):
					rule_dict_drop_list += [i]
					set_concat = combined_rule_list(rule_to_string_dict, v[0])
					rule_to_string_dict[i] = set_concat
					if len(v) == 2:
						set_concat_2 = combined_rule_list(rule_to_string_dict, v[1])
						rule_to_string_dict[i] = \
							rule_to_string_dict[i].union(set_concat_2)
		for rule in rule_dict_drop_list:
			del new_rule_dict[rule]
	return rule_to_string_dict

def calc_num_matching_rules(rule_dict, string_list):
	rule_to_string_dict = create_rule_to_string_dict(rule_dict)
	match_zero_strings = rule_to_string_dict['0']
	num_matching = [sample_str in match_zero_strings 
		for sample_str in string_list].count(True)

	return num_matching

def calc_num_matching_updated_rules(rule_dict, string_list):
	rule_to_string_dict = create_rule_to_string_dict(rule_dict)
	rule_set_42 = rule_to_string_dict['42']
	rule_set_31 = rule_to_string_dict['31']
	total_match_count = 0
	for curr_str in string_list:
		# all strings matching 42 or 31 have length 8
		if len(curr_str) % 8 == 0:
			eight_multiple = len(curr_str) // 8
			for num_42s in range(eight_multiple//2+1,eight_multiple):
				num_31s = eight_multiple - num_42s	
				is_match = True
				for i in range(num_42s):
					if curr_str[8*i:8*(i+1)] not in rule_set_42:
						is_match = False
						break
				for i in range(num_31s):
					if i == 0:
						if curr_str[-8*(i+1):] not in rule_set_31:
							is_match = False
							break
					else:
						if curr_str[-8*(i+1):-8*i] not in rule_set_31:
							is_match = False
							break
				if is_match:
					total_match_count += 1
					break

	return total_match_count

if __name__ == '__main__':
	rule_dict, string_list = parse_input()

	num_matching_rules = calc_num_matching_rules(rule_dict, string_list)
	print('The answer to the puzzle on Day 19 Part 1 is {}.'\
		.format(num_matching_rules))

	num_matching_updated_rules = calc_num_matching_updated_rules(rule_dict, string_list)
	print('The answer to the puzzle on Day 19 Part 2 is {}.'\
		.format(num_matching_updated_rules))
