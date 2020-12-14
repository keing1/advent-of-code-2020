def parse_bag_type(bag_type):
	first_space = bag_type.find(' ')
	bag_count = int(bag_type[:first_space])
	bag_kind = bag_type[first_space+1:]
	return (bag_count, bag_kind)

def parse_bag_line(bag_line):
	split_sides = bag_line.split(' contain ')
	surrounding_bag = split_sides[0][:-5]
	if split_sides[1][:2] == 'no':
		return (surrounding_bag, [])
	else:
		split_inside_bags = split_sides[1].split(', ')
		processed_inside_bags = [bag_type.replace('.', '').replace(' bags', '')\
			.replace(' bag', '') for bag_type in split_inside_bags]

		parsed_inside_bags = [parse_bag_type(bag_type) 
			for bag_type in processed_inside_bags]
		return (surrounding_bag, parsed_inside_bags)

def parse_bag_file():
	with open('input.txt', 'r') as f:
		bag_lines = f.read().split('\n')[:-1]

	parsed_bag_lines = [parse_bag_line(line) for line in bag_lines]

	return parsed_bag_lines

def create_edge_graph(parsed_bag_data):
	pass

def find_reachable_bags(edge_graph, starting_bag_name):
	pass

def find_enclosing_bags(parsed_bag_data, starting_bag_name):
	edge_graph = create_edge_graph(parsed_bag_data)

	reachable_bag_types = find_reachable_bags(edge_graph, starting_bag_name)

	return len(reachable_bag_types)

if __name__ == '__main__':
	parsed_bag_data = parse_bag_file()

	num_enclosing_bags = find_enclosing_bags(parsed_bag_data, 'shiny gold')
	print('The answer to the puzzle on Day 7 Part 1 is {}.'.format(num_enclosing_bags))


