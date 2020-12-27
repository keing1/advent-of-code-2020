def parse_input():
	with open('input.txt', 'r') as f:
		input_lines = f.read().split('\n')[:-1]

	input_nums = [int(num_str) for num_str in input_lines]

	return input_nums

def find_discrete_log(base, mod, result):
	power = 1

	curr_num = base
	while curr_num != result:
		curr_num *= base
		curr_num = curr_num % mod
		power += 1

	return power

def calc_power(base, power, mod):
	curr_num = 1
	for i in range(power):
		curr_num *= base
		curr_num = curr_num % mod

	return curr_num

def calc_encryption(parsed_input, base, mod):
	card_power = find_discrete_log(base, mod, parsed_input[0])
	door_power = find_discrete_log(base, mod, parsed_input[1])

	final_output = calc_power(parsed_input[0], door_power, mod)
	return final_output

if __name__ == '__main__':
	parsed_input = parse_input()

	encryption_key = calc_encryption(parsed_input, 7, 20201227)
	print('The answer to the puzzle on Day 25 Part 1 is {}.'\
		.format(encryption_key))
