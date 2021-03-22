#include <thread>
#include <map>

#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits, qsearch_hits;

int orig_eval;

int prune = 500;

int RESIGN = 1000;

int priority;

namespace {
	int danger[7] = {0, 5, 15, 15, 25, 40, 70};
}

std::map <int, int> eval_cache;

bool move_comparator(const int &a, const int &b)
{
	int good_a = 0, good_b = 0;
	
	if (a == priority) {
		good_a = INF;
	} else {
		good_a = eval_cache[a];
	}
	
	if (b == priority) {
		good_b = INF;
	} else {
		good_b = eval_cache[b];
	}

	return good_a > good_b;
}

pdi find_best_move(int depth) {
	// TODO: Make multi-threaded
	if (break_now) {
		return {0, -69};
	}

	nodes = 0; qsearch_nodes = 0;
	tb_hits = 0; qsearch_hits = 0;
	orig_eval = eval(curr_state);

	int best_move = -1, eval = -RESIGN;

	std::vector <int> moves = curr_state.list_moves();

	sort(moves.begin(), moves.end(), move_comparator);

	for (int i : moves) {
		// printf("Considering %s\n", curr_state.move_to_string(i).c_str());

		curr_state.make_move(i);
		int x = -search(depth - 1, -INF, -eval);
		curr_state.unmake_move(i);

		if (x > eval) {
			eval = x;
			best_move = i;
		}

		// printf("x = %d\n", x);

		if (break_now) break;
	}

	if (!curr_state.to_move) eval *= -1;

	return {eval, best_move};
}