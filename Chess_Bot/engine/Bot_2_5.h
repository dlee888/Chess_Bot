#ifndef BOT_H_INCLUDED
#define BOT_H_INCLUDED
#include <map>
#include <ctime>
#include <vector>

#include "Openings.h"
#include "Search.h"

void play()
{
	std::vector<int> game;
	bool computer_is_white = false;
	int num_move = 0;
	double time_limit;

	std::map <Bitstring, int> repetition_cnt;
	bool is_draw = false;

	std::string move;
	
	std::cout << "Do you want the computer to play black or white?\n";
	std::cin >> move;
	if (move == "white") {
		computer_is_white = true;
	}

	std::cout << "Do you want to load a game in progress?\n";
	std::cin >> move;
	if (move == "yes")
	{
		std::cout << "Please enter the game:\n";
		//loading by typing in moves, such as 1. e4 e5 2. d4 ...
		while (!(move == "*"))
		{
			if (num_move % 2 == 0)
				std::cin >> move;
			if (move == "*")
				break;
			std::cin >> move;
			if (move == "*")
				break;
			int move_i = curr_state.parse_move(move);
			curr_state.make_move(move_i);
			repetition_cnt[curr_state.get_hash()]++;
			if(repetition_cnt[curr_state.get_hash()] >= 3) is_draw = true;
			game.push_back(move_i);
			num_move++;
			
			remove_openings(num_move, move_i, computer_is_white);
		}
	}
	else if (move == "yes2")
	{
		std::cout << "Please enter the game:\n";
		int move_i;
		while (true)
		{
			std::cin >> move_i;
			if (move_i == -1) {
				break;
			}

			curr_state.make_move(move_i);
			repetition_cnt[curr_state.get_hash()]++;
			if(repetition_cnt[curr_state.get_hash()] >= 3) is_draw = true;
			game.push_back(move_i);
			num_move++;
			remove_openings(num_move, move_i, computer_is_white);
		}
	}
	std::cout << "How much time (max) do you want the program to take (seconds)?\n";
	std::cin >> time_limit;

	int move_i = -1;

	curr_state.print();

	std::string error_msg = "";

	while (true)
	{
		if (move == "resign" || move == "quit") {
			break;
		}
		if (curr_state.mate() || curr_state.adjucation() || is_draw) {
			break;
		}

		if (curr_state.to_move == computer_is_white)
		{
			if (computer_is_white && white_openings.size() > 0) {
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(white_openings[0].moves[num_move]) << std::endl
					<< "OPENING: " << white_openings[0].name << std::endl;
				move_i = white_openings[0].moves[num_move];
			}
			else if (!computer_is_white && black_openings.size() > 0) {
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(black_openings[0].moves[num_move]) << std::endl
					<< "OPENING: " << black_openings[0].name << std::endl;
				move_i = black_openings[0].moves[num_move];
			}
			else if (openings.size() > 0) {
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(openings[0].moves[num_move]) << std::endl
						<< "OPENING: " << openings[0].name << std::endl;
				move_i = openings[0].moves[num_move];
			}
			else
			{
				pii best_move = find_best_move(time_limit);
				move_i = best_move.second;

				if ((computer_is_white && best_move.first <= -RESIGN) || (!computer_is_white && best_move.first >= RESIGN))
				{
					error_msg = "COMPUTER RESIGNED";
					break;
				}
				if (move_i == -1)
				{
					error_msg = "ILLEGAL MOVE PLAYED";
					break;
				}

				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(move_i) << std::endl
						  << "EVAL: " << (double)best_move.first / 100 << std::endl;
			}
		}
		else
		{
			printf("Where do you move?\n");
			std::cin >> move;
			if (move == "resign" || move == "quit") break;
			
			move_i = curr_state.parse_move(move);
			if (move_i == -1 || !curr_state.legal_check(move_i))
			{
				error_msg = "ILLEGAL MOVE PLAYED";
				break;
			}
		}
		curr_state.make_move(move_i);
		game.push_back(move_i);

		num_move++;
		curr_state.print();
		std::cout << "HERUISTIC EVAL: " << (double)eval(curr_state, true) / 100 * (curr_state.to_move ? 1 : -1) << std::endl;
		
		remove_openings(num_move, move_i, computer_is_white);
		scramble_openings();
	}

	if (error_msg.size() != 0) {
		std::cout << error_msg << std::endl;
	}
	else if (move == "resign")
	{
		if (computer_is_white) {
			printf("WHITE WON\n");
		}
		else {
			printf("BLACK WON\n");
		}
	}
	else
	{
		int m = curr_state.mate();
		if (m == 1 || curr_state.adjucation() || is_draw) {
			printf("DRAW\n");
		}
		else if (m == 2)
		{
			if (curr_state.to_move) {
				printf("BLACK WON\n");
			}
			else {
				printf("WHITE WON\n");
			}
		}
		else {
			printf("GAME STILL IN PROGRESS\n");
		}
	}
    printf("GAME: ");
	for (int i : game)
	{
		std::cout << i << " ";
	}
	std::cout << std::endl;
}
#endif // !BOT_H_INCLUDED
