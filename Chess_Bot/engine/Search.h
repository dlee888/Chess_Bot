#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED
#include <vector>
#include <algorithm>
#include <functional>
#include <cassert>

#include "State.h"
#include "Evaluate.h"
#include "Transpose.h"

#define INF 1000000007

int quiescent_prune;

long long nodes;
long long tb_hits, collisions;

int orig_eval;

int prune = 500;

bool greater(const pdi &a, const pdi &b)
{
	return a.first > b.first;
}
bool less(const pdi &a, const pdi &b)
{
	return a.first < b.first;
}

pdi find_best_move(int depth, int alpha, int beta, int priority = -1)
{
	nodes++;

	//printf("Searching with depth = %d, alpha = %lf, beta = %lf\n", depth, alpha, beta);
	//curr_state.print();
	//printf("hash = %lld\n", curr_board_hash);

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= depth) {
		tb_hits++;
		return best_moves[curr_board_hash];
	}

	if (!curr_state.to_move)
	{
		if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true) != 7)
		{
			return pdi(-100000, -1);
		}
	}
	else
	{
		if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false) != 7)
		{
			return pdi(100000, -1);
		}
	}

	int curr_eval = eval(curr_state);
	if (depth <= 0)
	{
		return pdi(curr_eval, -1);
	}

	std::vector<int> moves = curr_state.list_moves();
	std::vector<pdi> ordered_moves;

	int mate = 3;
	for (int i : moves)
	{
		curr_state.make_move(i);
		ordered_moves.push_back({eval(curr_state), i});
		if (mate == 3) {
			if (!curr_state.to_move)
			{
				if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true) == 7)
				{
					mate = 0;
				}
			}
			else
			{
				if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false) == 7)
				{
					mate = 0;
				}
			}
		}
		curr_state.unmake_move(i);
	}
	if (mate == 3)
	{
		if (curr_state.to_move)
		{
			if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true) != 7)
				mate = 2;
			else
				mate = 1;
		}
		else
		{
			if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false) != 7)
				mate = 2;
			else
				mate = 1;
		}
	}

	if (mate == 1)
		return pdi(0, -1);
	else if (mate == 2)
	{
		if (curr_state.to_move) {
			return pdi(-100000, -1);
		}
		else {
			return pdi(100000, -1);
		}
	}
	
	if (curr_state.to_move)
	{
		if (curr_eval < orig_eval - prune && depth <= 3) {
			return pdi(curr_eval, -1);
		}

		sort(ordered_moves.begin(), ordered_moves.end(), greater);

		int best_move = -2;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			auto x = find_best_move(depth - 1, alpha, beta, -1);
			curr_state.unmake_move(priority);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			if (alpha < x.first)
			{
				alpha = x.first;
				best_move = priority;
			}
			if (alpha >= beta)
			{
				exists[curr_board_hash] = true;
				depths[curr_board_hash] = depth;
				best_moves[curr_board_hash] = pdi(alpha, best_move);
				return pdi(alpha, best_move);
			}
		}
		for (pdi& p : ordered_moves)
		{
			int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = find_best_move(depth - 1, alpha, beta, -1);
			curr_state.unmake_move(move);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			if (alpha < x.first)
			{
				alpha = x.first;
				best_move = move;
			}
			if (alpha >= beta)
				break;
		}

		exists[curr_board_hash] = true;
		depths[curr_board_hash] = depth;
		best_moves[curr_board_hash] = {alpha, best_move};

		if (depth == 1 && alpha != 100000 && alpha != -100000)
			return pdi((curr_eval + alpha) / 2, best_move);
		else
			return pdi(alpha, best_move);
	}
	else
	{
		if (curr_eval > orig_eval + prune && depth <= 3) {
			return pdi(curr_eval, -1);
		}

		sort(ordered_moves.begin(), ordered_moves.end(), less);

		int best_move = -2;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			auto x = find_best_move(depth - 1, alpha, beta, -1);
			curr_state.unmake_move(priority);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			if (beta > x.first)
			{
				beta = x.first;
				best_move = priority;
			}
			if (alpha >= beta)
			{
				exists[curr_board_hash] = true;
				depths[curr_board_hash] = depth;
				best_moves[curr_board_hash] = pdi(beta, best_move);
				return pdi(beta, best_move);
			}
		}
		for (pdi& p : ordered_moves)
		{
			int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = find_best_move(depth - 1, alpha, beta, -1);
			curr_state.unmake_move(move);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			if (beta > x.first)
			{
				beta = x.first;
				best_move = move;
			}
			if (alpha >= beta)
				break;
	}

		exists[curr_board_hash] = true;
		depths[curr_board_hash] = depth;
		best_moves[curr_board_hash] = pdi(beta, best_move);

		if (depth == 1 && beta != 100000 && beta != -100000)
			return pdi((curr_eval + beta) / 2, best_move);
		return pdi(beta, best_move);
	}
}

#endif // !SEARCH_H_INCLUDED
