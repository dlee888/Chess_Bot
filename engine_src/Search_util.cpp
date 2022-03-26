#include <algorithm>
#include <chrono>
#include <map>
#include <thread>

#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits, qsearch_hits;

Depth depth_qsearched, qs_depth_floor;

std::mt19937 rng(std::chrono::system_clock::now().time_since_epoch().count());

unsigned int mcts_prob;
int mcts_depth;
bool use_nnue;

pii search_result = {0.0, -1};
bool done_searching = false;

int futility_margin(int depth) { return 150 * depth; }

#if not defined __WIN32__ and not defined __WIN64__
void break_after(int time) {
	int time_left = time;
	const int dt = 100;
	while (time_left > 0) {
		std::this_thread::sleep_for(std::chrono::duration<int, std::milli>(std::min(dt, time_left)));
		if (done_searching) {
			return;
		}
		time_left -= dt;
	}
	break_now = true;
}
#endif

pii moves_loop() {
	Depth curr_depth = ONE_PLY;

	std::vector<int> moves = curr_state.list_moves();

	std::vector<pii> ordered_moves;

	for (int i : moves) {
		curr_state.make_move(i);

		if (!curr_state.king_attacked()) {
			Bitboard hash = curr_state.get_hash();
			int key = get_key(hash);
			if (tt_exists[key] && tt_hashes[key] == hash) {
				ordered_moves.push_back({tt_evals[key], i});
			} else {
				ordered_moves.push_back({eval(curr_state), i});
			}
		}

		curr_state.unmake_move(i);
	}

	if (ordered_moves.size() == 1) {
		// Break if there is only one legal move
		search_result.second = ordered_moves[0].second;
		done_searching = true;
		return search_result;
	}

	while (true) {
		if (options["debug"])
			printf("Searching depth %d\n", curr_depth);

		nodes = 0;
		qsearch_nodes = 0;
		tb_hits = 0;
		qsearch_hits = 0;
		depth_qsearched = DEPTH_ZERO;
		qs_depth_floor = std::max(Depth(-curr_depth + 2), (Depth)-5);

		int start_time = clock();

		std::stable_sort(ordered_moves.begin(), ordered_moves.end());

		int best_move = -1;
		Value evaluation = -RESIGN;
		for (pii& p : ordered_moves) {
			// printf("Considering %s\n", curr_state.move_to_string(p.second).c_str());
			curr_state.make_move(p.second);
			// curr_state.print();
			Value x = -search(curr_depth, -VALUE_INFINITE, -evaluation);
			// printf("x = %d\n", x);
			// curr_state.print();
			curr_state.unmake_move(p.second);

			p.first = -x;

			if (x > evaluation) {
				evaluation = x;
				best_move = p.second;
			}

			if (break_now)
				break;
		}
		if (break_now) {
			if (options["debug"])
				printf("Time is up\n");
			break;
		}

		int time_taken = clock() - start_time;

		if (options["debug"])
			std::cout << "Done searching, actual depth = " << curr_depth - depth_qsearched << std::endl
					  << "Best move is " << curr_state.move_to_string(best_move) << ", EVAL = " << (double)evaluation / 100 << std::endl
					  << (double)time_taken / CLOCKS_PER_SEC << " seconds taken" << std::endl
					  << nodes << " nodes searched, " << qsearch_nodes << " nodes qsearched "
					  << ((double)nodes + qsearch_nodes) * CLOCKS_PER_SEC / time_taken << " nodes per second." << std::endl
					  << tb_hits << " tt hits, " << qsearch_hits << " qsearch tt hits" << std::endl;

		search_result = std::make_pair(evaluation, best_move);

		if (abs(evaluation) >= MATE || curr_depth >= (int)options["depth_limit"]) {
			break;
		}

#if (defined __WIN32__) or (defined __WIN64__)
		if (break_now || (time_taken * curr_state.list_moves().size() > 5.5 * options["time_limit"] * CLOCKS_PER_SEC)) {
			printf("Breaking\n");
			break;
		}
#endif

		curr_depth += ONE_PLY;
	}

	if (curr_depth == ONE_PLY) {
		search_result = ordered_moves[0];
	}

	done_searching = true;
	return search_result;
}

pii find_best_move() {
	// TODO: Make search multi-threaded
	search_result = {0.0, -1};
	break_now = false;
	done_searching = false;
	mcts_prob = options["mcts_prob"];
	mcts_depth = options["mcts_max_depth"];
	use_nnue = options["use_nnue"];

#if not defined __WIN32__ and not defined __WIN64__
	auto timer = std::thread(break_after, options["time_limit"]);
	auto searcher = std::thread(moves_loop);

	timer.join();
	searcher.join();
#else
	moves_loop();
#endif

	if (!curr_state.to_move)
		search_result.first *= -1;

	return search_result;
}
