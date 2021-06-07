#include <thread>
#include <map>

#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits, qsearch_hits;

Depth depth_qsearched;

int futility_margin(int depth, bool improving) {
	return (175 - 50 * improving) * depth;
}

pii find_best_move(double time_limit, Depth depth_limit) {
	// TODO: Make multi-threaded

	Depth curr_depth = ONE_PLY;
	pii result = std::make_pair(0.0, -1);

	while (true)
	{
		printf("Searching depth %d\n", curr_depth);

		nodes = 0; qsearch_nodes = 0;
		tb_hits = 0; qsearch_hits = 0;
		depth_qsearched = DEPTH_ZERO;

		int start_time = clock();

		std::vector <int> moves = curr_state.list_moves();

		if (moves.size() == 1) {
			// Break if there is only one legal move
			result.second = moves[0];
			break;
		}

		std::vector<pii> ordered_moves;

		for (int i : moves)
		{
			curr_state.make_move(i);

			if (!curr_state.king_attacked()) {
				Bitstring hash = curr_state.get_hash();
				if (tt_exists[hash % TABLE_SIZE] && tt_hashes[hash % TABLE_SIZE] == hash) {
					ordered_moves.push_back({tt_evals[hash % TABLE_SIZE], i});
				}
				else {
					ordered_moves.push_back({eval(curr_state), i});
				}
			}

			curr_state.unmake_move(i);
		}

		std::stable_sort(ordered_moves.begin(), ordered_moves.end());
		
		int best_move = -1;
		Value evaluation = -RESIGN;
		for (const pii& p : ordered_moves)
		{
			int move = p.second;
			// printf("Considering %s\n", curr_state.move_to_string(i).c_str());

			curr_state.make_move(move);
			Value x = -search(curr_depth, -VALUE_INFINITE, -evaluation);
			curr_state.unmake_move(move);

			if (x > evaluation) {
				evaluation = x;
				best_move = move;
			}

			// printf("x = %d\n", x);

			if (break_now) break;
		}

		int time_taken = clock() - start_time;

		double actual_eval = (double)evaluation / 100;
		std::cout << "Done searching, actual depth = " << curr_depth - depth_qsearched << std::endl;
		printf("Best move is %s, EVAL = %lf\n%lf seconds taken, %lld nodes searched, %lld nodes qsearched\nSpeed = %lf nodes per second. %lld TB hits, %lld Qsearch TB hits\n",
				curr_state.move_to_string(best_move).c_str(),
				actual_eval, (double)time_taken / CLOCKS_PER_SEC, nodes, qsearch_nodes, 
				((double)nodes + qsearch_nodes) * CLOCKS_PER_SEC / time_taken, tb_hits, qsearch_hits);
		
		result = std::make_pair(evaluation, best_move);

		if (abs(evaluation) >= MATE) {
			break;
		}
		
		if (break_now || (time_taken * curr_state.list_moves().size() > 4 * time_limit * CLOCKS_PER_SEC)) {
			printf("Breaking\n");
			break;
		}

		if (curr_depth >= depth_limit) {
			printf("Max depth reached\n");
			break;
		}

		curr_depth += ONE_PLY;
	}

	if (!curr_state.to_move) result.first *= -1;

	return result;
}