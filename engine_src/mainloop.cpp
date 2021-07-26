#include <ctime>

#include "Openings.h"
#include "Search.h"
#include "options.h"
#include "nnue.h"

std::string nnue_path = "./engine_src/nnue";

void init_everything()
{
	init_table();
	load_openings();
	nnue_input = std::vector <int>(384);
	load_nnue(nnue_path);
	curr_state = state();
}

std::string read_fen() {
	std::string pos, turn, castle, ep, fiftymove, fullmove;
	std::cin >> pos >> turn >> castle >> ep >> fiftymove >> fullmove;
	return pos + " " + turn + " " + castle + " " + ep + " " + fiftymove + " " + fullmove;
}

int main()
{
	srand(time(NULL));
	set_default_options();
	std::string cmnd;
	while (cmnd != "exit" && cmnd != "quit")
	{
		init_everything();
		// std::cout << ">>>\n";
		std::cin >> cmnd;
		if (cmnd == "go")
		{
			std::string pos = read_fen();
			curr_state.load(pos);
			curr_state.print();
			std::cout << "STATIC EVAL: " << eval(curr_state, true, options["use_nnue"]) << std::endl;

			int move = -1, eval = MATED - 1;
			if (options["use_opening_book"]) {
				if (curr_state.to_move && curr_state.full_move > 2 && white_openings[curr_state.get_hash()].size()) {
					move = white_openings[curr_state.get_hash()][0];
				} 
				else if (!curr_state.to_move && curr_state.full_move > 2 && black_openings[curr_state.get_hash()].size()) {
					move = black_openings[curr_state.get_hash()][0];
				}
				else if (openings[curr_state.get_hash()].size()) {
					move = openings[curr_state.get_hash()][0];
				}
			}
			if (move == -1) {
				pii best_move = find_best_move();
				if ((curr_state.to_move && best_move.first <= -RESIGN) || (!curr_state.to_move && best_move.first >= RESIGN))
				{
					std::cout << "COMPUTER PLAYED RESIGN" << std::endl;
					continue;
				}
				move = best_move.second;
				eval = best_move.first;
			}
			std::cout << "COMPUTER PLAYED " << to_uci(move) << std::endl;
			if (eval >= MATED) {
				std::cout << "EVAL: " << (double)eval / 100 << std::endl;
			} else {
				std::cout << "BOOK MOVE\n";
			}
			curr_state.make_move(move);
			curr_state.print();
			std::cout << "GAME: " << curr_state.to_fen() << std::endl;
		} 
		else if (cmnd == "setoption") {
			std::string option_name;
			int value;
			std::cin >> option_name;
			if (option_name == "nnue_path") {
				std::cin >> nnue_path;
			} else {
				std::cin >> value;
				options[option_name] = value;
			}
		} 
		else if (cmnd == "debug") {
			std::string move;
			std::stack <int> moves;
			while (move != "stop") {
				std::cin >> move;
				if (move == "undo") {
					curr_state.unmake_move(moves.top());
					moves.pop();
				} else {
					int move_i = curr_state.parse_move(move);
					if (move_i == -1 || !curr_state.legal_check(move_i)) continue;
					curr_state.make_move(move_i);
					moves.push(move_i);
				}
				curr_state.print();
				std::cout << "EVAL: " << eval(curr_state, true) << std::endl;
			}
		}
	}
	return 0;
}
