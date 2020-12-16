def parse_adapters():
	with open('input.txt', 'r') as f:
		adapter_list = f.read().split('\n')[:-1]

	adapter_list = [int(adapter) for adapter in adapter_list]

	return adapter_list

def find_difference_product(parsed_adapters):
	sorted_adapters = sorted(parsed_adapters)

	init_adapter_list = [0] + sorted_adapters
	final_adapter_list = sorted_adapters + [sorted_adapters[-1] + 3]
	adapter_diff = [y-x for (x,y) in zip(init_adapter_list,
										final_adapter_list)]

	num_1_diff = adapter_diff.count(1)
	num_3_diff = adapter_diff.count(3)

	return num_1_diff * num_3_diff

def find_num_distinct_arrangements(parsed_adapters):
	num_arrangements_dictionary = {0: 1}

	sorted_adapters = sorted(parsed_adapters)

	adapter_output_list = sorted_adapters + [sorted_adapters[-1] + 3]

	for adapter in adapter_output_list:
		num_one_less = 0
		num_two_less = 0
		num_three_less = 0
		if adapter-1 in num_arrangements_dictionary:
			num_one_less = num_arrangements_dictionary[adapter-1]
		if adapter-2 in num_arrangements_dictionary:
			num_two_less = num_arrangements_dictionary[adapter-2]
		if adapter-3 in num_arrangements_dictionary:
			num_three_less = num_arrangements_dictionary[adapter-3]

		num_arrangements_dictionary[adapter] = num_one_less + num_two_less + \
			num_three_less

	return num_arrangements_dictionary[adapter_output_list[-1]]

if __name__ == '__main__':
	parsed_adapters = parse_adapters()

	diff_product = find_difference_product(parsed_adapters)
	print('The answer to the puzzle on Day 10 Part 1 is {}.'.format(diff_product))

	num_arrangements = find_num_distinct_arrangements(parsed_adapters)
	print('The answer to the puzzle on Day 10 Part 2 is {}.'.format(num_arrangements))