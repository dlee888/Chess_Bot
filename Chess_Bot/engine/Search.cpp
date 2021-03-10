#include "Search.h"

bool break_now = false;

state curr_state;

int search(int depth, int alpha, int beta)
{
	nodes++;

	// printf("Searching depth = %d, alpha = %d, beta = %d\n", depth, alpha, beta);
	// curr_state.print();

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	// printf("Board hash = %lld\n", curr_board_hash);

	if (exists[curr_board_hash] && depths[curr_board_hash] >= depth)
	{
		tb_hits++;
		// printf("TT hit\n");
		return best_eval[curr_board_hash];
	}

	if (depth <= 0)
		return qsearch(alpha, beta);

	if (curr_state.king_attacked()) {
		// printf("King attacked\n");
		return MATE;
	}

	if (break_now) {
		// printf("Breaking now\n");
		return eval(curr_state);
	}

	std::vector<int> moves = curr_state.list_moves();

	bool mate = true;
	for (int i : moves)
	{
		curr_state.make_move(i);
		if (mate && !curr_state.king_attacked())
		{
			mate = false;
		}
		curr_state.unmake_move(i);
	}
	if (mate)
	{
		if (curr_state.is_check())
			return MATED;
		else
			return DRAWN;
	}

	int curr_eval = eval(curr_state);

	if (curr_eval < orig_eval - prune && depth <= 3)
	{
		return curr_eval;
	}

	sort(moves.begin(), moves.end(), move_comparator);

	for (int move : moves)
	{
		curr_state.make_move(move);
		int x = -search(depth - 1, -beta, -alpha);
		curr_state.unmake_move(move);

		if (abs(x) >= 70184952) {
			break_now = true;
			curr_state.print();
			printf("Bug after %s\n", curr_state.move_to_string(move).c_str());
		}

		alpha = std::max(alpha, x);

		if (alpha >= beta)
			break;
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = depth;
	best_eval[curr_board_hash] = alpha;

	if (abs(alpha) >= 70184952) {
		break_now = true;
		curr_state.print();
		printf("Search bug found\n");
	}

	return alpha;
}

// Only searches captures and queen promotions to avoid horizon effect
int qsearch(int alpha, int beta)
{
	qsearch_nodes++;

	// printf("Qsearching alpha = %d, beta = %d\n", alpha, beta);
	// curr_state.print();
	
	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash])
	{
		// printf("Found in tt\n");
		qsearch_hits++;
		return best_eval[curr_board_hash];
	}

	if (curr_state.king_attacked())
		return MATE;

	std::vector<int> ordered_moves;

	bool mate = true;
	for (int i : curr_state.list_moves())
	{
		curr_state.make_move(i);
		if (mate && !curr_state.king_attacked())
		{
			mate = false;
		}
		curr_state.unmake_move(i);

		if ((((i >> 15) & 7) != 0) || ((((i >> 18) & 3) == 2) && (((i >> 20) & 3) == 3)))
		{
			ordered_moves.push_back(i);
		}
	}
	if (mate)
	{
		if (curr_state.is_check()) {
			// printf("Checkmate\n");
			return MATED;
		}
		else {
			// printf("Stalemate\n");
			return DRAWN;
		}
	}

	int curr_eval = eval(curr_state);

	if (break_now || ordered_moves.size() == 0)
	{
		// printf("Returned static eval = %d\n", curr_eval);
		return curr_eval;
	}

	if (curr_eval >= beta)
	{ // Standing pat
		return curr_eval;
	}

	alpha = std::max(alpha, curr_eval);

	sort(ordered_moves.begin(), ordered_moves.end(), move_comparator);

	int best_move = -3;
	for (int move : ordered_moves)
	{
		curr_state.make_move(move);
		int x = -qsearch(-beta, -alpha);
		curr_state.unmake_move(move);

		if (abs(x) >= 70184968) {
			break_now = true;
			curr_state.print();
			printf("Qsearch bug after %s\n", curr_state.move_to_string(move).c_str());
		}

		alpha = std::max(alpha, x);

		if (alpha >= beta)
			break;
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = 0;
	best_eval[curr_board_hash] = alpha;
	return alpha;
}