def process_expense_list():
	# Read in expense txt file
	with open('input.txt', 'r') as f:
		expense_list = f.readlines()
    
    # Remove new lines and change to ints
	return [int(expense[:-1]) for expense in expense_list]


# Calculate expense numbers for part 1
def calculate_expense_two_sum(exp_list, total):
	expense_set = set()

	for expense in exp_list:
		if total - expense in expense_set:
			return (expense, total - expense)
		expense_set.add(expense)
	return None

def calculate_expense_three_sum(exp_list, total):
	sorted_exp = sorted(exp_list)

	for i, v in enumerate(sorted_exp):
		two_sum = total - v
		two_sum_output = calculate_expense_two_sum(sorted_exp[i+1:], two_sum)
		if two_sum_output is not None:
			return (v, two_sum_output[0], two_sum_output[1])
	return None



if __name__ == '__main__':
	cleaned_expense_list = process_expense_list()

	part_1_numbers = calculate_expense_two_sum(cleaned_expense_list, 2020)
	part_1_outputs = part_1_numbers[0] * part_1_numbers[1]
	print('The answer to the puzzle on Day 1 Part 1 is {}.'.format(part_1_outputs))

	part_2_numbers = calculate_expense_three_sum(cleaned_expense_list, 2020)
	part_2_outputs = part_2_numbers[0] * part_2_numbers[1] * part_2_numbers[2]
	print('The answer to the puzzle on Day 1 Part 2 is {}.'.format(part_2_outputs))