#include "Search.h"

bool break_now = false;

state curr_state;

Value search(Depth depth, Value alpha, Value beta)
{
	nodes++;

	// printf("search(%d, %d, %d)\n", depth, alpha, beta);
	// curr_state.print();

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= depth)
	{
		// printf("tt hit, %d\n", best_eval[curr_board_hash]);
		tb_hits++;
		return best_eval[curr_board_hash];
	}

	if (curr_state.adjucation()) {
		// printf("adjucation\n");
		return DRAWN;
	}

	if (depth <= DEPTH_ZERO) {
		return qsearch(alpha, beta);
	}

	if (curr_state.king_attacked()) {
		// printf("king attacked\n");
		return MATE;
	}

	if (break_now) {
		return eval(curr_state);
	}

	std::vector<int> moves = curr_state.list_moves();
	eval_cache.clear();

	bool mate = true;
	for (int i : moves)
	{
		curr_state.make_move(i);

		int hash = curr_state.get_hash() % TABLE_SIZE;
		if (exists[hash]) {
			eval_cache[i] = -best_eval[hash];
		}
		else {
			eval_cache[i] = -eval(curr_state);
		}

		if (mate && !curr_state.king_attacked())
		{
			mate = false;
		}

		curr_state.unmake_move(i);
	}
	if (mate)
	{
		if (curr_state.is_check()) {
			// printf("checkmate\n");
			return MATED;
		}
		else {
			// printf("stalemate\n");
			return DRAWN;
		}
	}

	Value curr_eval;
	if (exists[curr_board_hash]) {
		// tt entry can be used as more accurate static eval
		curr_eval = best_eval[curr_board_hash];
	} else {
		curr_eval = eval(curr_state);
	}

	// Futility pruning
	// TODO: implement improving
	if (depth < 7 && curr_eval < orig_eval - futility_margin(depth, false))
	{
		// printf("futility prune: %d\n", curr_eval);
		return curr_eval;
	}

	// Razor pruning and extended razor pruning
	if (depth < 1) {
		if (curr_eval + RAZOR_MARGIN < alpha) {
			// printf("razor prune\n");
			return qsearch(alpha, beta);
		}
	} 
	
	std::sort(moves.begin(), moves.end(), move_comparator);

	for (int move : moves)
	{
		// printf("Considering %s\n", curr_state.move_to_string(move).c_str());

		curr_state.make_move(move);

		Value x = -search(depth - ONE_PLY, -beta, -alpha);
		curr_state.unmake_move(move);

		alpha = std::max(alpha, x);

		if (alpha >= beta) {
			// printf("alpha beta cutoff: %d\n", alpha);
			return alpha;
		}
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = depth;
	best_eval[curr_board_hash] = alpha;

	// printf("done searching, returned %d\n", alpha);
	// curr_state.print();

	return alpha;
}

// Only searches captures and queen promotions to avoid horizon effect
Value qsearch(Value alpha, Value beta)
{
	qsearch_nodes++;
	
	// printf("qsearch(%d, %d)\n", alpha, beta);
	// curr_state.print();

	unsigned long long curr_board_hash = curr_state.get_hash() % TABLE_SIZE;

	if (exists[curr_board_hash] && depths[curr_board_hash] >= DEPTH_QS_NO_CHECKS)
	{
		// printf("tt hit: %d\n", best_eval[curr_board_hash]);
		qsearch_hits++;
		return best_eval[curr_board_hash];
	}

	if (curr_state.adjucation()) {
		// printf("adjucation\n");
		return DRAWN;
	}

	if (curr_state.king_attacked()){
		// printf("king attacked\n");
		return MATE;
	}

	std::vector<int> ordered_moves;

	eval_cache.clear();

	bool mate = true;
	for (int i : curr_state.list_moves())
	{
		curr_state.make_move(i);
		if (mate && !curr_state.king_attacked())
		{
			mate = false;
		}

		if ((((i >> 15) & 7) != 0) || ((((i >> 18) & 3) == 2) && (((i >> 20) & 3) == 3)))
		{
			ordered_moves.push_back(i);
			
			int hash = curr_state.get_hash() % TABLE_SIZE;
			if (exists[hash]) {
				// printf("using tt for eval of move %s\n", curr_state.move_to_string(i).c_str());
				eval_cache[i] = -best_eval[hash];
			}
			else {
				eval_cache[i] = -eval(curr_state);
			}
		}

		curr_state.unmake_move(i);
	}
	if (mate)
	{
		if (curr_state.is_check()) {
			// printf("checkmate\n");
			return MATED;
		}
		else {
			// printf("stalemate\n");
			return DRAWN;
		}
	}
	
	Value curr_eval;
	if (exists[curr_board_hash]) {
		// tt entry can be used as more accurate static eval
		curr_eval = best_eval[curr_board_hash];
	} else {
		curr_eval = eval(curr_state);
	}

	if (break_now || ordered_moves.size() == 0)
	{
		// printf("no moves: %d\n", curr_eval);
		return curr_eval;
	}

	if (curr_eval >= beta)
	{ // Standing pat
		// printf("stand-pat: %d\n", curr_eval);
		return curr_eval;
	}

	// printf("static eval = %d\n", curr_eval);

	alpha = std::max(alpha, curr_eval);

	std::sort(ordered_moves.begin(), ordered_moves.end(), move_comparator);

	for (int move : ordered_moves)
	{
		// printf("Considering %s\n", curr_state.move_to_string(move).c_str());

		curr_state.make_move(move);
		Value x = -qsearch(-beta, -alpha);
		curr_state.unmake_move(move);

		alpha = std::max(alpha, x);

		if (alpha >= beta) {
			// printf("alpha beta cutoff: %d\n", alpha);
			return alpha;
		}
	}

	exists[curr_board_hash] = true;
	depths[curr_board_hash] = DEPTH_QS_NO_CHECKS;
	best_eval[curr_board_hash] = alpha;
	
	// printf("done qsearching, returned %d\n", alpha);
	// curr_state.print();

	return alpha;
}