from collections import deque
import copy

def parse_decks():
	with open('input.txt', 'r') as f:
		input_lines = f.read().split('\n')[:-1]

	break_point = input_lines.index('')

	player_1_deck = input_lines[1:break_point]
	player_1_deck = [int(num) for num in player_1_deck]
	player_1_deck = deque(player_1_deck)

	player_2_deck = input_lines[break_point+2:]
	player_2_deck = [int(num) for num in player_2_deck]
	player_2_deck = deque(player_2_deck)

	final_decks = {'Player 1': player_1_deck, 'Player 2': player_2_deck}

	return final_decks

def run_game_step(deck_dictionary):
	player_1_deck = deck_dictionary['Player 1']
	player_2_deck = deck_dictionary['Player 2']

	player_1_card = player_1_deck.popleft()
	player_2_card = player_2_deck.popleft()

	if player_1_card > player_2_card:
		player_1_deck.append(player_1_card)
		player_1_deck.append(player_2_card)
	else:
		player_2_deck.append(player_2_card)
		player_2_deck.append(player_1_card)
	return

def run_game(initial_decks):
	current_decks = initial_decks

	player_1_deck = current_decks['Player 1']
	player_2_deck = current_decks['Player 2']

	while len(player_1_deck) > 0 and len(player_2_deck) > 0:
		run_game_step(current_decks)

	if len(player_1_deck) == 0:
		winner = 'Player 2'
	else:
		winner = 'Player 1'

	return current_decks, winner

def calculate_deck_score(winner_deck):
	deck_score = 0
	winner_deck_len = len(winner_deck)

	for i, num in enumerate(winner_deck):
		deck_score += (winner_deck_len-i)*num
	return deck_score

def calculate_final_score(parsed_decks):
	deck_copy = copy.deepcopy(parsed_decks)

	current_decks, winner = run_game(deck_copy)
	deck_score = calculate_deck_score(list(current_decks[winner]))
	return deck_score

def run_game_step_recursive(deck_dictionary):
	player_1_deck = deck_dictionary['Player 1']
	player_2_deck = deck_dictionary['Player 2']

	player_1_card = player_1_deck.popleft()
	player_2_card = player_2_deck.popleft()

	player_1_length = len(player_1_deck)
	player_2_length = len(player_2_deck)

	if (player_1_length >= player_1_card) and (player_2_length >= player_2_card):
		new_player_1_deck = deque(list(player_1_deck)[:player_1_card])
		new_player_2_deck = deque(list(player_2_deck)[:player_2_card])

		recursive_dict = {'Player 1': new_player_1_deck, 'Player 2': new_player_2_deck}

		updated_deck, winner = run_game_recursive(recursive_dict)
		if winner == 'Player 1':
			player_1_deck.append(player_1_card)
			player_1_deck.append(player_2_card)
		else:
			player_2_deck.append(player_2_card)
			player_2_deck.append(player_1_card)
	else:
		if player_1_card > player_2_card:
			player_1_deck.append(player_1_card)
			player_1_deck.append(player_2_card)
		else:
			player_2_deck.append(player_2_card)
			player_2_deck.append(player_1_card)

def run_game_recursive(initial_decks):
	current_decks = initial_decks

	player_1_deck = current_decks['Player 1']
	player_2_deck = current_decks['Player 2']

	visited_states = set()

	while len(player_1_deck) > 0 and len(player_2_deck) > 0:
		run_game_step_recursive(current_decks)
		current_decks_tuple = (tuple(current_decks['Player 1']),
			tuple(current_decks['Player 2']))
		if current_decks_tuple in visited_states:
			return current_decks, 'Player 1'
		else:
			visited_states.add(current_decks_tuple)

	if len(player_1_deck) == 0:
		winner = 'Player 2'
	else:
		winner = 'Player 1'

	return current_decks, winner

def calculate_final_score_recursive(parsed_decks):
	deck_copy = copy.deepcopy(parsed_decks)

	current_decks, winner = run_game_recursive(deck_copy)
	deck_score = calculate_deck_score(list(current_decks[winner]))
	return deck_score

if __name__ == '__main__':
	parsed_decks = parse_decks()
	final_score = calculate_final_score(parsed_decks)
	print('The answer to the puzzle on Day 22 Part 1 is {}.'\
		.format(final_score))

	final_score_recursive = calculate_final_score_recursive(parsed_decks)
	print('The answer to the puzzle on Day 22 Part 2 is {}.'\
		.format(final_score_recursive))
