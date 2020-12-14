# Given a line from the password input, output a tuple (a, b, c, d),
# where a is the minimum number of times the character can appear,
# b is the maximum number of times, c is the character we are 
# checking for, and d is the password we are looking at
def parse_password_line(pw_line):
	line_parts = pw_line.split(' ')
	count_list = line_parts[0].split('-')
	char_to_check = line_parts[1][0]
	password = line_parts[2][:-1]

	return (int(count_list[0]), int(count_list[1]), char_to_check, password)


def read_and_parse_password_list():
	# Read in expense txt file
	with open('input.txt', 'r') as f:
		password_line_list = f.readlines()
    
    # Parse each individual line of the password list
	return [parse_password_line(password_line) for password_line in password_line_list]

def find_valid_password_count_one(parsed_lines):
	# For each parsed line, check if the number of times the character appears is between the 
	# minimum amount and the maximum amount
	valid_pass_list = [parsed_line[0] <= parsed_line[3].count(parsed_line[2]) <= parsed_line[1] 
		for parsed_line in parsed_lines]

	return valid_pass_list.count(True)

def find_valid_password_count_two(parsed_lines):
	# For each parsed line, check if the character appears in either the minimum
	# position or the maximum position
	valid_pass_list = [(parsed_line[3][parsed_line[0]-1]==parsed_line[2]) ^ 
		(parsed_line[3][parsed_line[1]-1]==parsed_line[2])
		for parsed_line in parsed_lines]
	return valid_pass_list.count(True)

if __name__ == '__main__':
	parsed_lines = read_and_parse_password_list()
	valid_count_part_one = find_valid_password_count_one(parsed_lines)
	print('The answer to the puzzle on Day 2 Part 1 is {}.'.format(valid_count_part_one))
	valid_count_part_two = find_valid_password_count_two(parsed_lines)
	print('The answer to the puzzle on Day 2 Part 2 is {}.'.format(valid_count_part_two))