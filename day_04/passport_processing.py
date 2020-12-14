def parse_passport_data():
	with open('input.txt', 'r') as f:
		passport_list = f.read().split("\n\n")

	# split passports on newline and space characters to create sublists of 
	# key-value pairs
	parsed_passport_list = [passport.replace('\n', ' ').split(' ') 
		for passport in passport_list]

	# Remove trailing space caused by newline at end of last line
	parsed_passport_list[-1] = parsed_passport_list[-1][:-1]

	return parsed_passport_list

def is_passport_valid_part_one(passport):
	necessary_passport_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 
		'ecl', 'pid'}

	val_fields = set()

	for field in passport:
		if field[:3] in necessary_passport_fields:
			val_fields.add(field[:3])

	return len(val_fields) == 7

def is_passport_valid_part_two(passport):
	necessary_passport_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 
		'ecl', 'pid'}

	val_fields = set()

	for field in passport:
		[field_key, field_val] = field.split(':')
		if field_key == 'byr':
			try:
				val_int = int(field_val)
				if 1920 <= val_int <= 2002:
					val_fields.add(field_key)
			except ValueError:
				pass
		elif field_key == 'iyr':
			try:
				val_int = int(field_val)
				if 2010 <= val_int <= 2020:
					val_fields.add(field_key)
			except ValueError:
				pass
		elif field_key == 'eyr':
			try:
				val_int = int(field_val)
				if 2020 <= val_int <= 2030:
					val_fields.add(field_key)
			except ValueError:
				pass
		elif field_key == 'hgt':
			try:
				if (field_val[-2:] == 'cm') and (150 <= int(field_val[:-2]) <= 193):
					val_fields.add(field_key)
				elif (field_val[-2:] == 'in') and (59 <= int(field_val[:-2]) <= 76):
					val_fields.add(field_key)
			except ValueError:
				pass
		elif field_key == 'hcl':
			if field_val[0] == '#' and len(field_val) == 7 and \
				all(c in '0123456789abcdef' for c in field_val[1:]):
				val_fields.add(field_key)
		elif field_key == 'ecl':
			if field_val in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
				val_fields.add(field_key)
		elif field_key == 'pid':
			if len(field_val) == 9 and field_val.isnumeric():
				val_fields.add(field_key)


	return len(val_fields) == 7

def find_num_valid_passports(parsed_passport_list, part_one=True):
	if part_one:
		valid_passport_list = [is_passport_valid_part_one(passport) 
			for passport in parsed_passport_list]
	else:
		valid_passport_list = [is_passport_valid_part_two(passport) 
			for passport in parsed_passport_list]

	return valid_passport_list.count(True)


if __name__ == '__main__':
	parsed_passport_list = parse_passport_data()
	num_valid_passports_one = find_num_valid_passports(parsed_passport_list, True)
	print('The answer to the puzzle on Day 4 Part 1 is {}.'.format(num_valid_passports_one))

	num_valid_passports_two = find_num_valid_passports(parsed_passport_list, False)
	print('The answer to the puzzle on Day 4 Part 2 is {}.'.format(num_valid_passports_two))