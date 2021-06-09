#include <ctime>

#include "Openings.h"
#include "options.h"
#include "Search.h"

void init_everything()
{
	init_table();
	load_openings();
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
	while (cmnd != "exit")
	{
		init_everything();
		// std::cout << ">>>\n";
		std::cin >> cmnd;
		if (cmnd == "go")
		{
			std::string pos = read_fen();
			curr_state.load(pos);
			curr_state.print();
			std::cout << eval(curr_state, true) << std::endl;
			if (options["use_opening_book"]) {
				if (curr_state.to_move && curr_state.full_move > 2 && white_openings[curr_state.get_hash()].size()) {
					int move_i = white_openings[curr_state.get_hash()][0];
					std::cout << "COUPUTER PLAYED " << curr_state.move_to_string(move_i) << std::endl;
					curr_state.make_move(move_i);
					curr_state.print();
					std::cout << "GAME: " << curr_state.to_fen() << std::endl;
					continue;
				} 
				else if (!curr_state.to_move && curr_state.full_move > 2 && black_openings[curr_state.get_hash()].size()) {
					int move_i = black_openings[curr_state.get_hash()][0];
					std::cout << "COUPUTER PLAYED " << curr_state.move_to_string(move_i) << std::endl;
					curr_state.make_move(move_i);
					curr_state.print();
					std::cout << "GAME: " << curr_state.to_fen() << std::endl;
					continue;
				}
				else if (openings[curr_state.get_hash()].size()) {
					int move_i = openings[curr_state.get_hash()][0];
					std::cout << "COUPUTER PLAYED " << curr_state.move_to_string(move_i) << std::endl;
					curr_state.make_move(move_i);
					curr_state.print();
					std::cout << "GAME: " << curr_state.to_fen() << std::endl;
					continue;
				}
			}
			pii best_move = find_best_move(options["time_limit"], (Depth)options["depth_limit"]);
			if ((curr_state.to_move && best_move.first <= -RESIGN) || (!curr_state.to_move && best_move.first >= RESIGN))
			{
				std::cout << "COMPUTER PLAYED RESIGN" << std::endl;
				continue;
			}
			std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(best_move.second) << std::endl
				<< "EVAL: " << (double)best_move.first / 100 << std::endl;
			curr_state.make_move(best_move.second);
			curr_state.print();
			std::cout << "GAME: " << curr_state.to_fen() << std::endl;
		} 
		else if (cmnd == "setoption") {
			std::string option_name;
			int value;
			std::cin >> option_name >> value;
			options[option_name] = value;
		} 
		else if (cmnd == "debug") {
			int i;
			std::cin >> i;
			while (i != -1) {
				curr_state.make_move(i);
				std::cin >> i;
			}
			std::cout << curr_state.to_fen() << std::endl;
		}
		else if (cmnd == "quit")
		{
			break;
		}
		else
		{
			// std::cout << "COMMAND NOT RECOGNIZED\n";
		}
	}
	return 0;
}
