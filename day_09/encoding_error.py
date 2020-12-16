def parse_numbers():
	with open('input.txt', 'r') as f:
		numbers_list = f.read().split('\n')[:-1]

	numbers_list = [int(num) for num in numbers_list]
	return numbers_list

# more efficient method would store intermediate sums
def find_invalid_number(parsed_numbers):
	for i, v in enumerate(parsed_numbers):
		if i > 24:
			valid_number = False
			for j in range(1, 26):
				for k in range(j+1, 26):
					if parsed_numbers[i-j] + parsed_numbers[i-k] == v:
						valid_number = True
			if not valid_number:
				break
	return v

# more efficient method would store intermediate sums
def find_adding_numbers(parsed_numbers, invalid_number):
	for i in range(len(parsed_numbers)):
		for j in range(i+1, len(parsed_numbers)):
			if sum(parsed_numbers[i:j+1]) == invalid_number:
				return parsed_numbers[i:j+1]


def find_encryption_weakness(parsed_numbers, invalid_number):
	adding_numbers = find_adding_numbers(parsed_numbers, invalid_number)
	return max(adding_numbers) + min(adding_numbers)


if __name__ == '__main__':
	parsed_numbers = parse_numbers()
	invalid_number = find_invalid_number(parsed_numbers)
	print('The answer to the puzzle on Day 9 Part 1 is {}.'.format(invalid_number))
	
	encryption_weakness = find_encryption_weakness(parsed_numbers, invalid_number)
	print('The answer to the puzzle on Day 9 Part 2 is {}.'.format(encryption_weakness))
