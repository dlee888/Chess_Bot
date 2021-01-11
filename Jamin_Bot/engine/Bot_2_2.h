#ifndef BOT_H_INCLUDED
#define BOT_H_INCLUDED

#include <fstream>
#include <ctime>
#include <vector>

#include "Openings.h"
#include "Search.h"

void play() {
	std::vector <int> game;
	
	bool computer_is_white = false;
	int num_move = 0;
	double time_limit;
	std::string move;
	std::cout << "Do you want to load a game in progress?\n";
	std::cin >> move;
	if (move == "yes") {
		std::cout << "Please enter the game:\n";
		//loading by typing in moves, such as 1. e4 e5 2. d4 ...
		while (!(move == "*")) {
			if (num_move % 2 == 0) std::cin >> move;
			if (move == "*") break;
			std::cin >> move;
			if (move == "*") break;
			int move_i = curr_state.parse_move(move);
			curr_state.make_move(move_i);
			game.push_back(move_i);
			num_move++;
			for (int i = 0; i < openings.size(); i++) {
				if (openings[i].moves[num_move - 1] != move_i) {
					openings.erase(openings.begin() + i);
					i--;
				}
			}
		}
	}
	else if (move == "yes2") {
		std::cout << "Please enter the game:\n";
		//loading by typing in moves, such as 1. e4 e5 2. d4 ...
		while (!(move == "*")) {
			if (num_move % 2 == 0) std::cin >> move;
			if (move == "*") break;
			std::cin >> move;
			if (move == "*") break;
			int move_i = std::stoi(move);
			curr_state.make_move(move_i);
			game.push_back(move_i);
			num_move++;
			for (int i = 0; i < openings.size(); i++) {
				if (openings[i].moves[num_move - 1] != move_i) {
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
	if (move == "white") computer_is_white = true;

	if (time_limit < 40) {
		quiescent_prune = -1;
	}
	else if (time_limit < 70) {
		quiescent_prune = 3;
	}
	else if (time_limit < 135) {
		quiescent_prune = 4;
	}
	else if (time_limit < 600) {
		quiescent_prune = 5;
	}
	else {
		quiescent_prune = 6;
	}

	int move_i = -1;

	curr_state.print();
	//std::cout << eval(curr_state) << std::endl;
	
	std::string error_msg = "";
	
	while (true) {
		if (move == "resign" || move == "quit") break;
		if (curr_state.mate()) break;
		if (curr_state.adjucation()) break;

		if (curr_state.to_move == computer_is_white) {
			if (openings.size()) {
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(openings[0].moves[num_move]) << std::endl
					<< "OPENING: " << openings[0].name << std::endl;
				move_i = openings[0].moves[num_move];
				curr_state.make_move(move_i);
				game.push_back(move_i);
			}
			else {
				int time_taken = 0, curr_depth = 1;
				pdi best_move = std::make_pair(0.0, -1);
				while ((double)time_taken / CLOCKS_PER_SEC * curr_state.list_moves().size() < 3 * time_limit) {
					printf("Searching depth %d\n", curr_depth);
					int start_time = clock();
					best_move = find_best_move(curr_depth, -DINF, DINF, best_move.second);
					time_taken = clock() - start_time;
					printf("Best move is %s, EVAL = %lf\n%lf seconds taken, %lld nodes searched\nSpeed = %lf nodes per second\n",
						curr_state.move_to_string(best_move.second).c_str(),
						best_move.first, (double)time_taken / CLOCKS_PER_SEC, nodes, (double)nodes * CLOCKS_PER_SEC / time_taken);
					if (abs(best_move.first) > 300) break;
					nodes = 0;
					curr_depth++;
				}
				std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(best_move.second) << std::endl << "EVAL: " << best_move.first << std::endl;
				move_i = best_move.second;
				curr_state.make_move(best_move.second);
				game.push_back(move_i);
			}
		}
		else {
			printf("Where do you move?\n");
			std::cin >> move;
			if (move == "resign" || move == "quit") break;
			move_i = curr_state.parse_move(move);
			if (move_i == -1) {
				error_msg = "ILLEGAL MOVE PLAYED";
				break;
			}
			curr_state.make_move(move_i);
			game.push_back(move_i);
		}

		num_move++;
		curr_state.print();
		std::cout << "HERUISTIC EVAL: " << eval(curr_state) << std::endl;
		for (int i = 0; i < openings.size(); i++) {
			if (openings[i].moves[num_move - 1] != move_i || openings[i].moves[num_move] == -1) {
				openings.erase(openings.begin() + i);
				i--;
			}
		}
		scramble_openings();
	}
	if (error_msg.size() != 0) {
		std::cout << error_msg << std::endl;
	}
	else if (move == "resign") {
		if (computer_is_white) {
			printf("WHITE WON\n");
		}
		else {
			printf("BLACK WON\n");
		}
	}
	else {
		int m = curr_state.mate();
		if (m == 1 || curr_state.adjucation()) {
			printf("DRAW\n");
		}
		else {
			if (m == 2) {
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
	}
	for (int i : game) {
		std::cout << i << " ";
	}
	std::cout << std::endl;
}
#endif // !BOT_H_INCLUDED
