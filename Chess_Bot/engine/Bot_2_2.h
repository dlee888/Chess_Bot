#ifndef BOT_H_INCLUDED
#define BOT_H_INCLUDED

#include <fstream>
#include <ctime>
#include <vector>

#include "Openings.h"
#include "Search.h"

int RESIGN = 1000;

void play()
{
	std::vector<int> game;
	//std::map<state, int> draw;
	bool computer_is_white = false, is_draw = false;
	int num_move = 0;
	double time_limit;
	std::string move;
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
			//draw[curr_state]++;
			//if(draw[curr_state] >= 3) is_draw = true;
			game.push_back(move_i);
			num_move++;
			for (int i = 0; i < openings.size(); i++)
			{
				if (openings[i].moves[num_move - 1] != move_i)
				{
					openings.erase(openings.begin() + i);
					i--;
				}
			}
		}
	}
	else if (move == "yes2")
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
			int move_i = std::stoi(move);
			curr_state.make_move(move_i);
			//draw[curr_state]++;
			//if(draw[curr_state] >= 3) is_draw = true;
			game.push_back(move_i);
			num_move++;
			for (int i = 0; i < openings.size(); i++)
			{
				if (openings[i].moves[num_move - 1] != move_i)
				{
					openings.erase(openings.begin() + i);
					i--;
				}
			}
		}
	}
	std::cout << "How much time (max) do you want the program to take (seconds)?\n";
	std::cin >> time_limit;
	std::cout << "Do you want the computer to play black or white?\n";
	std::cin >> move;
	if (move == "white")
		computer_is_white = true;

	int move_i = -1;

	curr_state.print();

	std::string error_msg = "";

	while (true)
	{
		if (move == "resign" || move == "quit")
			break;
		if (curr_state.mate())
			break;
		if (curr_state.adjucation() || is_draw)
			break;

		if (curr_state.to_move == computer_is_white)
		{
			int opening_size = openings.size();
			if (computer_is_white)
				opening_size += white_openings.size();
			else 
				opening_size += black_openings.size();
			if (opening_size)
			{
				if (opening_size > openings.size())
				{
					if (computer_is_white)
					{
						std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(white_openings[0].moves[num_move]) << std::endl
						  << "OPENING: " << white_openings[0].name << std::endl;
						move_i = white_openings[0].moves[num_move];
					}
					else
					{
						std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(black_openings[0].moves[num_move]) << std::endl
						  << "OPENING: " << black_openings[0].name << std::endl;
						move_i = black_openings[0].moves[num_move];
					}
				}
				else
				{
					std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(openings[0].moves[num_move]) << std::endl
						  << "OPENING: " << openings[0].name << std::endl;
					move_i = openings[0].moves[num_move];
				}
				curr_state.make_move(move_i);
				game.push_back(move_i);
			}
			else
			{
				int time_taken = 0, curr_depth = 1;
				pdi best_move = std::make_pair(0.0, -1);
				while ((double)time_taken / CLOCKS_PER_SEC * curr_state.list_moves().size() < 4 * time_limit)
				{
					printf("Searching depth %d\n", curr_depth);

					nodes = 0; qsearch_nodes = 0;
					tb_hits = 0;
					orig_eval = eval(curr_state);

					int start_time = clock();
					if (computer_is_white) best_move = search(curr_depth, -RESIGN, INF, best_move.second);
					else best_move = search(curr_depth, -INF, RESIGN, best_move.second);
					time_taken = clock() - start_time;

					double actual_eval = (double)best_move.first / 100;
					printf("Best move is %s, EVAL = %lf\n%lf seconds taken, %lld nodes searched, %lld nodes qsearched\nSpeed = %lf nodes per second. %lld TB hits\n",
						   curr_state.move_to_string(best_move.second).c_str(),
						   actual_eval, (double)time_taken / CLOCKS_PER_SEC, nodes, qsearch_nodes, ((double)nodes + qsearch_nodes) * CLOCKS_PER_SEC / time_taken, tb_hits);
					if (abs(best_move.first) >= 100000)
						break;
					curr_depth++;
				}
				move_i = best_move.second;
				if (move_i == -2) {
					error_msg = "COMPUTER RESIGNED";
					break;
				}
				if (move_i == -1)
				{
					error_msg = "ILLEGAL MOVE PLAYED";
					break;
				}
				if ((computer_is_white && best_move.first < -RESIGN) || (!computer_is_white && best_move.first > RESIGN))
				{
					error_msg = "COMPUTER RESIGNED";
					break;
				}
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(move_i) << std::endl
						  << "EVAL: " << (double)best_move.first / 100 << std::endl;
				curr_state.make_move(move_i);
				game.push_back(move_i);
			}
		}
		else
		{
			printf("Where do you move?\n");
			std::cin >> move;
			if (move == "resign" || move == "quit")
				break;
			move_i = curr_state.parse_move(move);
			if (move_i == -1 || !curr_state.legal_check(move_i))
			{
				error_msg = "ILLEGAL MOVE PLAYED";
				break;
			}
			curr_state.make_move(move_i);
			game.push_back(move_i);
		}

		num_move++;
		curr_state.print();
		std::cout << "HERUISTIC EVAL: " << (double)eval(curr_state) / 100 << std::endl;
		for (int i = 0; i < openings.size(); i++)
		{
			if (openings[i].moves[num_move - 1] != move_i || openings[i].moves[num_move] == -1)
			{
				openings.erase(openings.begin() + i);
				i--;
			}
		}
		if (computer_is_white)
		{
			for (int i = 0; i < white_openings.size(); i++)
			{
				if (white_openings[i].moves[num_move - 1] != move_i || white_openings[i].moves[num_move] == -1)
				{
					white_openings.erase(white_openings.begin() + i);
					i--;
				}
			}
		}
		else
		{
			for (int i = 0; i < black_openings.size(); i++)
			{
				if (black_openings[i].moves[num_move - 1] != move_i || black_openings[i].moves[num_move] == -1)
				{
					black_openings.erase(black_openings.begin() + i);
					i--;
				}
			}
		}
		
		scramble_openings();
	}
	if (error_msg.size() != 0)
		std::cout << error_msg << std::endl;
	else if (move == "resign")
	{
		if (computer_is_white)
			printf("WHITE WON\n");
		else
			printf("BLACK WON\n");
	}
	else
	{
		int m = curr_state.mate();
		if (m == 1 || curr_state.adjucation() || is_draw)
			printf("DRAW\n");
		else
		{
			if (m == 2)
			{
				if (curr_state.to_move)
					printf("BLACK WON\n");
				else
					printf("WHITE WON\n");
			}
			else
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
