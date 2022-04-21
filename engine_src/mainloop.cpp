#include <chrono>
#include <ctime>

#include "Openings.h"
#include "Search.h"
#include "nnue.h"
#include "options.h"

std::string nnue_path = "./engine_src/nnue";

void init_everything() {
	init_table(options["table_size"]);
	load_openings();
	if (options["use_nnue"]) {
		load_nnue(nnue_path);
	}
	curr_state = state();
}

std::string read_fen() {
	std::string pos, turn, castle, ep, fiftymove, fullmove;
	std::cin >> pos >> turn >> castle >> ep >> fiftymove >> fullmove;
	return pos + " " + turn + " " + castle + " " + ep + " " + fiftymove + " " + fullmove;
}

unsigned long long curr_time() {
	return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
}

int main() {
	srand(time(NULL));
	set_default_options();
	std::string cmnd;
	while (cmnd != "exit" && cmnd != "quit") {
		init_everything();
		std::cin >> cmnd;
		if (cmnd == "go") {
			std::string pos = read_fen();
			curr_state.load(pos);
			curr_state.print();
			std::cout << "STATIC EVAL: " << eval(curr_state, true, options["use_nnue"]) << std::endl;

			int move = -1, eval = MATED - 1;
			if (options["use_opening_book"]) {
				if (curr_state.to_move && curr_state.full_move > 2 && white_openings[curr_state.get_hash()].size()) {
					move = white_openings[curr_state.get_hash()][0];
				} else if (!curr_state.to_move && curr_state.full_move > 2 && black_openings[curr_state.get_hash()].size()) {
					move = black_openings[curr_state.get_hash()][0];
				} else if (openings[curr_state.get_hash()].size()) {
					move = openings[curr_state.get_hash()][0];
				}
			}
			if (move == -1) {
				pii best_move = find_best_move();
				if ((curr_state.to_move && best_move.first <= -RESIGN) || (!curr_state.to_move && best_move.first >= RESIGN)) {
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
		} else if (cmnd == "setoption") {
			std::string option_name;
			int value;
			std::cin >> option_name;
			if (option_name == "nnue_path") {
				std::cin >> nnue_path;
			} else {
				std::cin >> value;
				options[option_name] = value;
			}
		} else if (cmnd == "options") {
			for (auto& p : options) {
				std::cout << p.first << ": " << p.second << std::endl;
			}
		} else if (cmnd == "stress") {
			int n;
			std::cin >> n;
			std::string pos = read_fen();
			curr_state.load(pos);
			curr_state.print();
			std::cout << "STATIC EVAL: " << eval(curr_state, true, options["use_nnue"]) << std::endl;
			std::cout << "\n----------------------------------------------------------------\nTesting eval()...\n";
			auto start_time = curr_time();
			for (int i = 0; i < n; i++) {
				eval(curr_state);
			}
			auto total_time = curr_time() - start_time;
			std::cout << "Total time for " << n << " calls: " << total_time << "ms" << std::endl;
			std::cout << "Average time: " << (double)total_time / n << "ms" << std::endl;
			std::cout << "\n----------------------------------------------------------------\nTesting is_check()...\n";
			start_time = curr_time();
			for (int i = 0; i < n; i++) {
				curr_state.is_check();
			}
			total_time = curr_time() - start_time;
			std::cout << "Total time for " << n << " calls: " << total_time << "ms" << std::endl;
			std::cout << "Average time: " << (double)total_time / n << "ms" << std::endl;
			std::cout << "\n----------------------------------------------------------------\nTesting list_moves()...\n";
			start_time = curr_time();
			for (int i = 0; i < n; i++) {
				curr_state.list_moves();
			}
			total_time = curr_time() - start_time;
			std::cout << "Total time for " << n << " calls: " << total_time << "ms" << std::endl;
			std::cout << "Average time: " << (double)total_time / n << "ms" << std::endl;
			std::cout << "\n----------------------------------------------------------------\n";
			if (options["use_nnue"]) {
				std::cout << "Testing eval() with nnue...\n";
				start_time = curr_time();
				for (int i = 0; i < n; i++) {
					eval(curr_state, false, true);
				}
				total_time = curr_time() - start_time;
				std::cout << "Total time for " << n << " calls: " << total_time << "ms" << std::endl;
				std::cout << "Average time: " << (double)total_time / n << "ms" << std::endl;
			}
			options["depth_limit"] = 4;
			options["mcts_max_depth"] = -1;
			std::cout << "Testing search...\n";
			start_time = curr_time();
			find_best_move();
			total_time = curr_time() - start_time;
			std::cout << "Total time: " << total_time << "ms\n----------------------------------------------------------------" << std::endl;
			set_default_options();
		} else if (cmnd == "test") {
			curr_state.load(start_fen);
			std::stack<int> moves;
			while (true) {
				curr_state.print();
				std::string move;
				std::cin >> move;
				if (move == "debug") {
					int row, col, color;
					std::cin >> row >> col >> color;
					std::cout << curr_state.see(row, col, color) << std::endl;
				} else if (move == "fen") {
					std::cout << curr_state.to_fen() << std::endl;
				} else if (move == "undo") {
					curr_state.unmake_move(moves.top());
					moves.pop();
				} else {
					moves.push(curr_state.parse_move(move));
					curr_state.make_move(curr_state.parse_move(move));
				}
			}
		} else if (cmnd == "self") {
            curr_state.load(start_fen);
			curr_state.print();
            while (true) {
                pii move = find_best_move();
                std::cout << (double)move.first / 100 << " " << to_uci(move.second) << std::endl;
                curr_state.make_move(move.second);
				std::cout << curr_state.to_fen() << std::endl;
                curr_state.print();
            }
        } else if (cmnd == "count") {
			std::string fen = read_fen();
			curr_state.load(fen);
			for (int i = 1; i < 10; i++) {
				auto start_time = curr_time();
				std::cout << "Depth: " << i << " " << count_positions(i) << std::endl;
				std::cout << "Total time: " << curr_time() - start_time << "ms\n----------------------------------------------------------------" << std::endl;
			}
		} else if (cmnd == "options") {
			for (auto [name, value] : options) {
				std::cout << name << ": " << value << std::endl;
			}
		}
	}
	return 0;
}
