#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED

#include <vector>
#include <algorithm>
#include <functional>

#include "State.h"
#include "Evaluate.h"
#include "Transpose.h"

#define DINF 9.99e100

int quiescent_prune;

long long nodes;
long long tb_hits, collisions;

bool greater(const pdi &a, const pdi &b)
{
	return a.first > b.first;
}
bool less(const pdi &a, const pdi &b)
{
	return a.first < b.first;
}

pdi find_best_move(int depth, double alpha, double beta, int priority = -1, bool speed = 0)
{
	nodes++;

	//printf("Searching with depth = %d, alpha = %lf, beta = %lf\n", depth, alpha, beta);
	//curr_state.print();
	//printf("hash = %lld\n", curr_state.board_hash);

	bool not_same = true;
	if (exists[curr_state.board_hash])
	{
		if (curr_state == positions[curr_state.board_hash])
		{
			tb_hits++;
			//printf("found in table\n");
			not_same = false;
			if (depth <= depths[curr_state.board_hash])
				return best_moves[curr_state.board_hash];
		}
		else
		{
			//printf("collision\n");
			collisions++;
		}
	}

	if (!curr_state.to_move)
	{
		if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true))
		{
			return pdi(-1000.0, -1);
		}
	}
	else
	{
		if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false))
		{
			return pdi(1000.0, -1);
		}
	}

	double curr_eval = eval(curr_state, speed);
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
		ordered_moves.push_back({eval(curr_state, speed), i});
		if (!curr_state.to_move)
		{
			if (!curr_state.attacking(whitekings[0].first, whitekings[0].second, true))
			{
				curr_state.unmake_move(i);
				mate = 0;
				break;
			}
		}
		else
		{
			if (!curr_state.attacking(blackkings[0].first, blackkings[0].second, false))
			{
				curr_state.unmake_move(i);
				mate = 0;
				break;
			}
		}
		curr_state.unmake_move(i);
	}
	if (mate == 3)
	{
		if (curr_state.to_move)
		{
			if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true))
				mate = 2;
			else
				mate = 1;
		}
		else
		{
			if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false))
				mate = 2;
			else
				mate = 1;
		}
	}

	if (mate == 1)
		return pdi(0, -1);
	else if (mate == 2)
	{
		if (curr_state.to_move)
			return pdi(-1000, -1);
		else
			return pdi(1000, -1);
	}

	// if (depth < quiescent_prune && curr_state.quiescent())
	// {
	// 	return pdi(curr_eval, -1);
	// }

	if (curr_state.to_move)
	{
		sort(ordered_moves.begin(), ordered_moves.end(), greater);

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
				if (not_same)
					positions[curr_state.board_hash] = curr_state;
				best_moves[curr_state.board_hash] = pdi(alpha, best_move);
				return pdi(alpha, best_move);
			}
		}
		for (int move : moves)
		{
			//int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			if(alpha > eval(curr_state, speed)+prune)
			{
				curr_state.unmake_move(move);
				continue;
			}
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
				break;
		}

		if (!(exists[curr_state.board_hash] && positions[curr_state.board_hash].full_move + depths[curr_state.board_hash] > curr_state.full_move + depth))
		{
			exists[curr_state.board_hash] = true;
			depths[curr_state.board_hash] = depth;
			if (not_same)
				positions[curr_state.board_hash] = curr_state;
			best_moves[curr_state.board_hash] = {alpha, best_move};
		}

		if (depth == 1 && alpha != 1000 && alpha != -1000)
			return pdi((9 * curr_eval + 11 * alpha) / 20, best_move);
		else
			return pdi(alpha, best_move);
	}
	else
	{
		sort(ordered_moves.begin(), ordered_moves.end(), less);
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
				if (not_same)
					best_moves[curr_state.board_hash] = pdi(beta, best_move);
				return pdi(beta, best_move);
			}
		}
		for (int move : moves)
		{
			//int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			if(beta > eval(curr_state, speed)+prune)
			{
				curr_state.unmake_move(move);
				continue;
			}
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
				break;
		}

		if (!(exists[curr_state.board_hash] && positions[curr_state.board_hash].full_move + depths[curr_state.board_hash] > curr_state.full_move + depth))
		{
			exists[curr_state.board_hash] = true;
			depths[curr_state.board_hash] = depth;
			if (not_same)
				positions[curr_state.board_hash] = curr_state;
			best_moves[curr_state.board_hash] = pdi(beta, best_move);
		}

		if (depth == 1 && beta != 1000 && beta != -1000)
			return pdi((9 * curr_eval + 11 * beta) / 20, best_move);
		return pdi(beta, best_move);
	}
}

#endif // !SEARCH_H_INCLUDED
