#include "Search.h"

bool break_now = false;

state curr_state;

int search(int depth, int alpha, int beta)
{
	nodes++;

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= depth)
	{
		tb_hits++;
		return best_eval[curr_board_hash];
	}

	if (curr_state.adjucation())
		return DRAWN;

	if (depth <= 0)
		return qsearch(alpha, beta);

	if (curr_state.king_attacked()) {
		return MATE;
	}

	if (break_now) {
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
		if (curr_state.is_check()) {
			return MATED;
		}
		else {
			return DRAWN;
		}
	}

	int curr_eval = eval(curr_state);

	// Futility pruning
	if (curr_eval < orig_eval - prune && depth <= 3)
	{
		return curr_eval;
	}

	// Razor pruning and extended razor pruning
	if (depth == 1) {
		if (curr_eval + RAZOR_MARGIN < beta) {
			return std::max(curr_eval + RAZOR_MARGIN, qsearch(alpha, beta));
		}
	} else if (depth <= 3) {
		if (curr_eval + EXTENDED_RAZOR_MARGIN < beta) {
			return std::max(curr_eval + EXTENDED_RAZOR_MARGIN, qsearch(alpha, beta));
		}
	}
	
	std::sort(moves.begin(), moves.end(), move_comparator);

	for (int move : moves)
	{
		curr_state.make_move(move);

		// More razor pruning
		if (depth <= 2 && eval(curr_state) + RAZOR_MARGIN < alpha) {
			curr_state.unmake_move(move);
			break;
		}

		int x = -search(depth - 1, -beta, -alpha);
		curr_state.unmake_move(move);

		alpha = std::max(alpha, x);

		if (alpha >= beta) {
			return alpha;
		}
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = depth;
	best_eval[curr_board_hash] = alpha;

	return alpha;
}

// Only searches captures and queen promotions to avoid horizon effect
int qsearch(int alpha, int beta)
{
	qsearch_nodes++;
	
	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= 0)
	{
		qsearch_hits++;
		return best_eval[curr_board_hash];
	}

	if (curr_state.adjucation()) {
		return DRAWN;
	}

	if (curr_state.king_attacked()){
		return MATE;
	}

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
			return MATED;
		}
		else {
			return DRAWN;
		}
	}

	int curr_eval = eval(curr_state);

	if (break_now || ordered_moves.size() == 0)
	{
		return curr_eval;
	}

	if (curr_eval >= beta)
	{ // Standing pat
		return curr_eval;
	}

	alpha = std::max(alpha, curr_eval);

	std::sort(ordered_moves.begin(), ordered_moves.end(), move_comparator);

	for (int move : ordered_moves)
	{
		curr_state.make_move(move);
		int x = -qsearch(-beta, -alpha);
		curr_state.unmake_move(move);

		alpha = std::max(alpha, x);

		if (alpha >= beta) {
			return alpha;
		}
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = 0;
	best_eval[curr_board_hash] = alpha;
	
	return alpha;
}