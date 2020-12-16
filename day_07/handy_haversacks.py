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
	edge_graph = {}

	for bag_line in parsed_bag_data:
		surrounding_bag = bag_line[0]
		inside_bags = bag_line[1]
		for bag_tuple in inside_bags:
			bag_name = bag_tuple[1]
			if bag_tuple[1] in edge_graph:
				edge_graph[bag_tuple[1]] += [surrounding_bag]
			else:
				edge_graph[bag_tuple[1]] = [surrounding_bag]

	return edge_graph

def find_reachable_bags(edge_graph, starting_bag_name):
	reached_nodes = set()
	current_nodes = edge_graph[starting_bag_name]

	while len(current_nodes) > 0:
		active_node = current_nodes.pop()
		if active_node not in reached_nodes:
			if active_node in edge_graph:
				current_nodes += edge_graph[active_node]
			reached_nodes.add(active_node)

	return reached_nodes

def find_enclosing_bags(parsed_bag_data, starting_bag_name):
	edge_graph = create_edge_graph(parsed_bag_data)

	reachable_bag_types = find_reachable_bags(edge_graph, starting_bag_name)

	return len(reachable_bag_types)

def create_reverse_edge_graph(parsed_bag_data):
	edge_graph = {}

	for bag_line in parsed_bag_data:
		surrounding_bag = bag_line[0]
		inside_bags = bag_line[1]
		edge_graph[surrounding_bag] = inside_bags

	return edge_graph

def find_num_inside_bags(parsed_bag_data, starting_bag_name):
	edge_graph = create_reverse_edge_graph(parsed_bag_data)

	current_bag_count = 0
	current_bag_list = edge_graph[starting_bag_name]

	while len(current_bag_list) > 0:
		active_bag = current_bag_list.pop()
		active_bag_count = active_bag[0]
		active_bag_name = active_bag[1]

		current_bag_count += active_bag_count

		inside_bag_list = edge_graph[active_bag_name]

		updated_inside_bag_list = list(map(lambda tup: (tup[0]*active_bag_count, tup[1]),
											inside_bag_list))

		current_bag_list += updated_inside_bag_list

	return current_bag_count


if __name__ == '__main__':
	parsed_bag_data = parse_bag_file()

	num_enclosing_bags = find_enclosing_bags(parsed_bag_data, 'shiny gold')
	print('The answer to the puzzle on Day 7 Part 1 is {}.'.format(num_enclosing_bags))

	total_inside_bags = find_num_inside_bags(parsed_bag_data, 'shiny gold')
	print('The answer to the puzzle on Day 7 Part 2 is {}.'.format(total_inside_bags))


