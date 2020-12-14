import string

def parse_customs():
	with open('input.txt', 'r') as f:
		parsed_custom_data = f.read().split('\n\n')
	
	parsed_custom_data = [group_str.split('\n') 
		for group_str in parsed_custom_data]

	parsed_custom_data[-1] = parsed_custom_data[-1][:-1]

	return parsed_custom_data


def calculate_any_by_group(group_list):
	char_set = set()

	group_str = ''.join(group_list)

	for char in group_str:
		char_set.add(char)

	return len(char_set)

def calculate_any_sum(parsed_custom_data):
	group_any_list = [calculate_any_by_group(group_list) 
		for group_list in parsed_custom_data]

	return sum(group_any_list)

def calculate_every_by_group(group_list):
	all_letters = string.ascii_lowercase

	# For each letter, checking if that letter is in every string in group_list
	num_letters_every = [all(map(lambda person_str: letter in person_str, group_list)) 
		for letter in all_letters]

	return num_letters_every.count(True)

def calculate_every_sum(parsed_custom_data):
	group_every_list = [calculate_every_by_group(group_list) 
		for group_list in parsed_custom_data]

	return sum(group_every_list)


if __name__ == '__main__':
	parsed_custom_data = parse_customs()

	total_unique_sum = calculate_any_sum(parsed_custom_data)

	print('The answer to the puzzle on Day 6 Part 1 is {}.'.format(total_unique_sum))

	total_every_sum = calculate_every_sum(parsed_custom_data)

	print('The answer to the puzzle on Day 6 Part 2 is {}.'.format(total_every_sum))