def parse_boarding_data():
	with open('input.txt', 'r') as f:
		boarding_list = f.read().split('\n')[:-1]

	return boarding_list

def calculate_id(boarding_string):
	row_data = boarding_string[:-3]
	column_data = boarding_string[-3:]

	binary_row = row_data.replace('B', '1').replace('F', '0')
	binary_column = column_data.replace('R', '1').replace('L', '0')

	decimal_row = int(binary_row, 2)
	decimal_column = int(binary_column, 2)

	return decimal_row * 8 + decimal_column

def calculate_max_id(parsed_boarding):
	boarding_ids = [calculate_id(boarding_string) for boarding_string in parsed_boarding]

	return max(boarding_ids)

def find_missing_id(parse_boarding_data):
	boarding_ids = [calculate_id(boarding_string) for boarding_string in parsed_boarding]

	boarding_id_set = set(boarding_ids)

	for i in range(max(boarding_ids)):
		if i not in boarding_id_set and i-1 in boarding_id_set and i+1 in boarding_id_set:
			return i

	return None


if __name__ == '__main__':
	parsed_boarding = parse_boarding_data()
	max_id = calculate_max_id(parsed_boarding)
	print('The answer to the puzzle on Day 5 Part 1 is {}.'.format(max_id))

	missing_id = find_missing_id(parsed_boarding)
	print('The answer to the puzzle on Day 5 Part 2 is {}.'.format(missing_id))