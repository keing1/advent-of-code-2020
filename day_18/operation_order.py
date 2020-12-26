import copy

def read_equations():
	with open('input.txt', 'r') as f:
		equation_list = f.read().split('\n')[:-1]
	return equation_list

def find_paren_close_index(eq_str, start_paren_index):
	active_open_parens = 1
	i = start_paren_index
	while active_open_parens > 0:
		i += 1
		try:
			char = eq_str[i]
		except KeyError:
			raise ValueError()

		if char == '(':
			active_open_parens += 1
		elif char == ')':
			active_open_parens -= 1

	return i

def parse_equation_w_paren_nesting(eq_str):
	parsed_eq = []
	i = 0
	start_digit = False
	curr_num_str = ''
	while i < len(eq_str):
		char = eq_str[i]
		if start_digit:
			if char.isdigit():
				curr_num_str += char
				i += 1
				continue
			else:
				parsed_eq += [int(curr_num_str)]
				start_digit = False
				curr_num_str = ''
		if char in {'+', '*'}:
			parsed_eq += [char]
			i += 1
		elif char == '(':
			paren_close_index = find_paren_close_index(eq_str, i)
			parsed_eq += [parse_equation_w_paren_nesting(eq_str[i+1:paren_close_index])]
			i += (paren_close_index - i + 1)
		elif char.isdigit():
			start_digit = True
			curr_num_str += char
			i += 1
		else:
			i += 1

	if curr_num_str != '':
		parsed_eq += [int(curr_num_str)]

	return parsed_eq

def include_addition_nesting(parsed_eq):
	new_parsed_eq = copy.deepcopy(parsed_eq)
	i = 0
	while i < len(new_parsed_eq):
		token = new_parsed_eq[i]
		if type(token) is list:
			new_parsed_eq[i] = include_addition_nesting(new_parsed_eq[i])
			i += 1
		elif token == '+':
			if len(new_parsed_eq) > 3:
				if type(new_parsed_eq[i+1]) is list:
					new_parsed_eq[i+1] = include_addition_nesting(new_parsed_eq[i+1])
				new_parsed_eq = new_parsed_eq[:i-1] + \
					[[new_parsed_eq[i-1], '+', new_parsed_eq[i+1]]] + \
					new_parsed_eq[i+2:]
			else:
				i += 1
		else:
			i += 1

	return new_parsed_eq

def execute_parsed_equation(parsed_eq):
	first_token = parsed_eq[0]
	if type(first_token) is list:
		curr_num = execute_parsed_equation(first_token)
	else:
		curr_num = first_token

	curr_op = None
	for curr_token in parsed_eq[1:]:
		if (type(curr_token) is not list) and (curr_token in {'*', '+'}):
			curr_op = curr_token
		else:
			if type(curr_token) is list:
				curr_token = execute_parsed_equation(curr_token)

			if curr_op == '*':
				curr_num *= curr_token
			elif curr_op == '+':
				curr_num += curr_token
			else:
				raise ValueError()
	return curr_num

def calc_equation(eq_str, addition_precedence):
	parsed_eq = parse_equation_w_paren_nesting(eq_str)
	if addition_precedence:
		parsed_eq = include_addition_nesting(parsed_eq)
	equation_result = execute_parsed_equation(parsed_eq)

	return equation_result

def calc_equation_sum(equation_list, addition_precedence):
	equation_sum = sum([calc_equation(equation, addition_precedence) 
		for equation in equation_list])
	return equation_sum

if __name__ == '__main__':
	equation_list = read_equations()

	equation_sum = calc_equation_sum(equation_list, False)
	print('The answer to the puzzle on Day 18 Part 1 is {}.'\
		.format(equation_sum))

	equation_sum_two = calc_equation_sum(equation_list, True)
	print('The answer to the puzzle on Day 18 Part 2 is {}.'\
		.format(equation_sum_two))
