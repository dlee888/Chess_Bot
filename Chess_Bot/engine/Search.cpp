#include "Search.h"

pdi search(int depth, int alpha, int beta, int priority)
{
	nodes++;

	//printf("Searching with depth = %d, alpha = %lf, beta = %lf\n", depth, alpha, beta);
	//curr_state.print();
	//printf("hash = %lld\n", curr_board_hash);

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= depth)
	{
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
		return qsearch(alpha, beta);
	}

	std::vector<int> moves = curr_state.list_moves();
	std::vector<pdi> ordered_moves;

	int mate = 3;
	for (int i : moves)
	{
		curr_state.make_move(i);
		ordered_moves.push_back({eval(curr_state), i});
		if (mate == 3)
		{
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
		if (curr_state.to_move)
		{
			return pdi(-100000, -1);
		}
		else
		{
			return pdi(100000, -1);
		}
	}

	if (curr_state.to_move)
	{
		if (curr_eval < orig_eval - prune && depth <= 3)
		{
			return pdi(curr_eval, -1);
		}

		sort(ordered_moves.begin(), ordered_moves.end(), greater);

		int best_move = -2;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			auto x = search(depth - 1, alpha, beta, -1);
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
		for (pdi &p : ordered_moves)
		{
			int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = search(depth - 1, alpha, beta, -1);
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

		return pdi(alpha, best_move);
	}
	else
	{
		if (curr_eval > orig_eval + prune && depth <= 3)
		{
			return pdi(curr_eval, -1);
		}

		sort(ordered_moves.begin(), ordered_moves.end(), less);

		int best_move = -2;
		if (priority != -1)
		{
			curr_state.make_move(priority);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(priority).c_str(), eval(curr_state, speed));
			auto x = search(depth - 1, alpha, beta, -1);
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
		for (pdi &p : ordered_moves)
		{
			int move = p.second;
			if (move == priority)
				continue;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = search(depth - 1, alpha, beta, -1);
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

		return pdi(beta, best_move);
	}
}

pdi qsearch(int alpha, int beta)
{
	qsearch_nodes++;

    unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash])
	{
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

	std::vector<int> moves = curr_state.list_moves();
	std::vector<pdi> ordered_moves;

	int mate = 3;
	for (int i : moves)
	{
		curr_state.make_move(i);
		if (mate == 3)
		{
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
		if ((((i >> 15) & 7) == 0) && ((i >> 18) != 1) && ((i >> 18) != 2))
			continue;
		ordered_moves.push_back({eval(curr_state), i});
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
		if (curr_state.to_move)
		{
			return pdi(-100000, -1);
		}
		else
		{
			return pdi(100000, -1);
		}
	}

	if (ordered_moves.size() == 0)
	{
		return pdi(curr_eval, -3);
	}

	if (curr_state.to_move)
	{
        if (curr_eval >= beta) {
            return pdi(curr_eval, -3);
        }

		sort(ordered_moves.begin(), ordered_moves.end(), greater);

		int best_move = -3;
		for (pdi &p : ordered_moves)
		{
			int move = p.second;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = qsearch(alpha, beta);
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
		return pdi(alpha, best_move);
	}
	else
	{
        if (curr_eval <= alpha) {
            return pdi(curr_eval, -3);
        }

		sort(ordered_moves.begin(), ordered_moves.end(), less);

		int best_move = -3;
		for (pdi &p : ordered_moves)
		{
			int move = p.second;
			curr_state.make_move(move);
			//curr_state.print();
			//printf("Made move %s. Eval = %lf\n", curr_state.move_to_string(move).c_str(), eval(curr_state, speed));
			auto x = qsearch(alpha, beta);
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
		return pdi(beta, best_move);
	}
}