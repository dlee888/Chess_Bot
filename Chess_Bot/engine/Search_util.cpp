#include <thread>
#include <map>

#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits, qsearch_hits;

int orig_eval;

int futility_margin(int depth, bool improving) {
	return (175 - 50 * improving) * depth;
}

int priority;

namespace {
	int danger[7] = {0, 5, 15, 15, 25, 40, 70};
}

std::map <int, int> eval_cache;

bool move_comparator(const int &a, const int &b)
{
	int good_a = 0, good_b = 0;
	
	if (a == priority) {
		good_a = VALUE_INFINITE;
	} else {
		good_a = eval_cache[a];
	}
	
	if (b == priority) {
		good_b = VALUE_INFINITE;
	} else {
		good_b = eval_cache[b];
	}

	return good_a > good_b;
}

pii find_best_move(Depth depth) {
	// TODO: Make multi-threaded
	if (break_now) {
		return {0, -69};
	}

	nodes = 0; qsearch_nodes = 0;
	tb_hits = 0; qsearch_hits = 0;
	orig_eval = eval(curr_state);

	int best_move = -1;
	Value evaluation = -RESIGN;

	std::vector <int> moves = curr_state.list_moves();
	eval_cache.clear();

	for (int i : moves) {
		curr_state.make_move(i);

		int hash = curr_state.get_hash() % TABLE_SIZE;
		if (exists[hash]) {
			eval_cache[i] = -best_eval[hash];
		} else {
			eval_cache[i] = -eval(curr_state);
		}

		curr_state.unmake_move(i);
	}

	sort(moves.begin(), moves.end(), move_comparator);

	for (int i : moves) {
		// printf("Considering %s, %d\n", curr_state.move_to_string(i).c_str(), eval_cache[i]);

		curr_state.make_move(i);
		Value x = -search(depth - ONE_PLY, -VALUE_INFINITE, -evaluation);
		curr_state.unmake_move(i);

		if (x > evaluation) {
			evaluation = x;
			best_move = i;
		}

		// printf("x = %d\n", x);

		if (break_now) break;
	}

	if (!curr_state.to_move) evaluation *= -1;

	return {evaluation, best_move};
}