#ifndef ENGINE_H_INCLUDED
#define ENGINE_H_INCLUDED

#include <ctime>

#include "Openings.h"
#include "Search.h"

void analyse_game(int depth)
{
	std::vector<int> game;
	std::string move;
	int num_move = 0;
	state temp = state();

	printf("Please enter the game: ");
	while (!(move == "*"))
	{
		if (num_move % 2 == 0)
			std::cin >> move;
		if (move == "*")
			break;
		std::cin >> move;
		if (move == "*")
			break;
		int move_i = temp.parse_move(move);
		temp.make_move(move_i);
		game.push_back(move_i);
		num_move++;
	}

	init_eval_info();
	std::vector<pdi> best_moves;
	for (int i : game)
	{
		best_moves.push_back(find_best_move(depth));
		curr_state.make_move(i);
	}
	best_moves.push_back(find_best_move(depth));

	init_eval_info();
	temp = state();

	for (int i = 0; i < game.size(); i++)
	{
		temp.print();
		printf("EVAL = %lf\n", (double)best_moves[i].first / 100);
		printf("%s was played\n", temp.move_to_string(game[i]).c_str());
		double eval_diff = ((double)best_moves[i + 1].first - best_moves[i].first) / 100;
		if (!temp.to_move)
			eval_diff *= -1;
		if (eval_diff > 0.01)
		{
			printf("Brilliant move!\n");
		}
		else if (eval_diff > -0.01)
		{
			if (game[i] == best_moves[i].second)
			{
				printf("Best move!\n");
			}
			else
			{
				printf("Excellent move!\n");
			}
		}
		else if (eval_diff > -0.15)
		{
			printf("Inaccuracy\n");
		}
		else if (eval_diff > -0.4)
		{
			printf("Mistake\n");
		}
		else
		{
			printf("Blunder\n");
		}
		printf("Best move was %s, EVAL = %lf\n", temp.move_to_string(best_moves[i].second).c_str(), (double)best_moves[i].first / 100);
		temp.make_move(game[i]);

		printf("Type \'next\' to continue. ");
		std::cin >> move;
		while (move != "next")
			std::cin >> move;
	}
}

void get_best_move()
{
	std::string move;
	int num_move = 0;
	printf("Please enter the game: ");
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
	double tlim;
	std::cout << "How much time do you want the program to take? ";
	std::cin >> tlim;

	int time_taken = 0, curr_depth = 1;
	pdi best_move = std::make_pair(0.0, -1);
	while ((double)time_taken / CLOCKS_PER_SEC * curr_state.list_moves().size() < 2 * tlim)
	{
		printf("Searching depth %d\n", curr_depth);
		int start_time = clock();
		best_move = find_best_move(curr_depth);
		time_taken = clock() - start_time;
		printf("Best move is %s, EVAL = %lf\n%lf seconds taken, %lld nodes searched\nSpeed = %lf nodes per second\n",
			   curr_state.move_to_string(best_move.second).c_str(),
			   (double)best_move.first / 100, (double)time_taken / CLOCKS_PER_SEC, nodes, (double)nodes * CLOCKS_PER_SEC / time_taken);
		if (abs(best_move.first - 1000.0) < 1)
			break;
		if (abs(best_move.first + 1000.0) < 1)
			break;
		nodes = 0;
		curr_depth++;
	}

	std::cout << "Best move is " << curr_state.move_to_string(best_move.second) << ", EVAL = " << (double)best_move.first / 100 << std::endl;
}
void get_best_move2()
{
	std::string move;
	int num_move = 0;
	printf("Please enter the game: ");
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
	int depth;
	std::cout << "What depth do you want? ";
	std::cin >> depth;

	auto best_move = find_best_move(depth);
	std::cout << "Best move is " << curr_state.move_to_string(best_move.second) << ", EVAL = " << (double)best_move.first / 100 << std::endl;
}
#endif // !ENGINE_H_INCLUDED
