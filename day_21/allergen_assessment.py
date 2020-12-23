import copy

def parse_ingredient_line(line):
	allergen_start = line.find('(')
	ingredient_names = set(line[:allergen_start-1].split(' '))
	allergen_names = set(line[allergen_start+10:-1].split(', '))

	return (ingredient_names, allergen_names)

def parse_ingredient_input():
	with open('input.txt', 'r') as f:
		ingredients_list = f.read().split('\n')[:-1]

	parsed_ingredients = [parse_ingredient_line(ingredient_line) 
		for ingredient_line in ingredients_list]

	return parsed_ingredients

def find_safe_and_dangerous_ingredients(parsed_ingredients):
	ingredient_count_mapping = {}

	allergen_ingredient_mapping = {}

	# Part 1
	for ingredient_line in parsed_ingredients:
		ingredient_names = ingredient_line[0]
		allergen_names = ingredient_line[1]
		for a_name in allergen_names:
			if a_name in allergen_ingredient_mapping:
				allergen_ingredient_mapping[a_name] = \
					allergen_ingredient_mapping[a_name].intersection(ingredient_names)
			else:
				allergen_ingredient_mapping[a_name] = ingredient_names

		for i_name in ingredient_names:
			if i_name in ingredient_count_mapping:
				ingredient_count_mapping[i_name] += 1
			else:
				ingredient_count_mapping[i_name] = 1


	potential_allergy_ingredients = set()
	for allergen, i_set in allergen_ingredient_mapping.items():
		potential_allergy_ingredients = potential_allergy_ingredients.union(i_set)

	safe_ingredient_appearance_count = 0
	for ingredient, i_count in ingredient_count_mapping.items():
		if ingredient not in potential_allergy_ingredients:
			safe_ingredient_appearance_count += i_count
		else:
			print('dangerous')
			print(ingredient)

	# Part 2
	allergen_ingredient_mapping_2 = copy.deepcopy(allergen_ingredient_mapping)

	final_allergen_ingredient_mapping = []

	while len(allergen_ingredient_mapping) > 0:
		allergen_value = None
		i_value = None
		for allergen, i_set in allergen_ingredient_mapping_2.items(): 
			if len(i_set) == 1:
				i_value = list(i_set)[0]
				allergen_value = allergen

		if allergen_value:
			for allergen, i_set in allergen_ingredient_mapping_2.items():
				i_set.discard(i_value)
			del allergen_ingredient_mapping[allergen_value]
			final_allergen_ingredient_mapping += [(allergen_value, i_value)]
		else:
			# Assuming this algorithm is sufficient, will raise error if not
			raise InvalidArgumentError

	sorted_final_mapping = sorted(final_allergen_ingredient_mapping, key=lambda x: x[0])
	final_ingredients = [item[1] for item in sorted_final_mapping]
	combined_ingredients = ','.join(final_ingredients)

	return safe_ingredient_appearance_count, combined_ingredients


if __name__ == '__main__':
	parsed_ingredients = parse_ingredient_input()
	ingredient_appearance_count, combined_ingredients = \
		find_safe_and_dangerous_ingredients(parsed_ingredients)

	print('The answer to the puzzle on Day 21 Part 1 is {}.'\
		.format(ingredient_appearance_count))

	print('The answer to the puzzle on Day 21 Part 2 is {}.'\
		.format(combined_ingredients))
