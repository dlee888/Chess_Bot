#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED

#include <vector>
#include <algorithm>

#include "State.h"
#include "Evaluate.h"
#include "Transpose.h"

#define DINF 9.99e100

int quiescent_prune;

long long nodes;
long long tb_hits, collisions;

pdi find_best_move(int depth, double alpha, double beta, int priority = -1)
{
	nodes++;

	if (exists[curr_state.board_hash] && depth <= depths[curr_state.board_hash])
	{
		if (curr_state == positions[curr_state.board_hash])
		{
			tb_hits++;
			return best_moves[curr_state.board_hash];
		}
		else
		{
			collisions++;
		}
	}

	if (!curr_state.to_move)
	{
		if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true) != 7)
		{
			return pdi(-1000.0, -1);
		}
	}
	else
	{
		if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false) != 7)
		{
			return pdi(1000.0, -1);
		}
	}

	int m = curr_state.mate();
	if (m == 1)
	{
		return pdi(0, -1);
	}
	else if (m == 2)
	{
		if (curr_state.to_move)
		{
			return pdi(-1000, -1);
		}
		else
		{
			return pdi(1000, -1);
		}
	}

	double curr_eval = eval(curr_state);
	if (depth <= 0)
	{
		return pdi(curr_eval, -1);
	}

	if (depth < quiescent_prune && curr_state.quiescent())
	{
		return pdi(curr_eval, -1);
	}

	if (curr_state.to_move)
	{
		int best_move = -1;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state));
			auto x = find_best_move(depth - 1, alpha, beta);
			curr_state.unmake_move(priority);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state));
			if (alpha < x.first)
			{
				alpha = x.first;
				best_move = priority;
			}
			if (alpha >= beta)
			{
				exists[curr_state.board_hash] = true;
				depths[curr_state.board_hash] = depth;
				positions[curr_state.board_hash] = curr_state;
				best_moves[curr_state.board_hash] = pdi(alpha, best_move);
				return pdi(alpha, best_move);
			}
		}
		for (int move : curr_state.list_moves())
		{
			if (move == priority)
				continue;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state));
			auto x = find_best_move(depth - 1, alpha, beta);
			curr_state.unmake_move(move);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state));
			if (alpha < x.first)
			{
				alpha = x.first;
				best_move = move;
			}
			if (alpha >= beta)
			{
				break;
			}
		}
		exists[curr_state.board_hash] = true;
		depths[curr_state.board_hash] = depth;
		positions[curr_state.board_hash] = curr_state;
		best_moves[curr_state.board_hash] = pdi(alpha, best_move);
		if (depth == 1 && alpha != 1000 && alpha != -1000)
		{
			return pdi((9 * curr_eval + 11 * alpha) / 20, best_move);
		}
		else
		{
			return pdi(alpha, best_move);
		}
	}
	else
	{
		int best_move = -1;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state));
			auto x = find_best_move(depth - 1, alpha, beta);
			curr_state.unmake_move(priority);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state));
			if (beta > x.first)
			{
				beta = x.first;
				best_move = priority;
			}
			if (alpha >= beta)
			{
				exists[curr_state.board_hash] = true;
				depths[curr_state.board_hash] = depth;
				positions[curr_state.board_hash] = curr_state;
				best_moves[curr_state.board_hash] = pdi(beta, best_move);
				return pdi(beta, best_move);
			}
		}
		for (int move : curr_state.list_moves())
		{
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state));
			auto x = find_best_move(depth - 1, alpha, beta);
			curr_state.unmake_move(move);
			//curr_state.print();
			//printf("Unmade move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state));
			if (beta > x.first)
			{
				beta = x.first;
				best_move = move;
			}
			if (alpha >= beta)
			{
				break;
			}
		}
		exists[curr_state.board_hash] = true;
		depths[curr_state.board_hash] = depth;
		positions[curr_state.board_hash] = curr_state;
		best_moves[curr_state.board_hash] = pdi(beta, best_move);
		if (depth == 1 && beta != 1000 && beta != -1000)
		{
			return pdi((9 * curr_eval + 11 * beta) / 20, best_move);
		}
		return pdi(beta, best_move);
	}
}

#endif // !SEARCH_H_INCLUDED
