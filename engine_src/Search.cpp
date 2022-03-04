#include "Search.h"

bool break_now = false;

state curr_state;

Value search(Depth depth, Value alpha, Value beta) {
	nodes++;

	// printf("search(%d, %d, %d)\n", depth, alpha, beta);
	// curr_state.print();

	Bitstring curr_board_hash = curr_state.get_hash();
	Bitstring key = curr_board_hash % TABLE_SIZE;

	if (tt_exists[key] && tt_depths[key] >= depth && tt_hashes[key] == curr_board_hash) {
		// printf("tt hit, %d\n", tt_evals[key]);
		tb_hits++;
		return tt_evals[key];
	}

	if (curr_state.adjucation()) {
		// printf("adjucation\n");
		return DRAWN;
	}

	// if (curr_state.king_attacked()) {
	// 	// printf("king attacked\n");
	// 	return MATE;
	// }

	if (break_now || (depth <= mcts_depth && mcts_prob > rng())) {
		return eval(curr_state);
	}

	if (depth <= DEPTH_ZERO) {
		return qsearch(alpha, beta, depth);
	}

	Value curr_eval;
	if (tt_exists[key] && tt_hashes[key] == curr_board_hash) {
		// tt entry can be used as more accurate static eval
		curr_eval = tt_evals[key];
	} else {
		curr_eval = eval(curr_state);
	}

	// Futility pruning
	if (depth < 7 && (curr_eval - futility_margin(depth) >= beta)) {
		// printf("futility prune: %d\n", curr_eval);
		return curr_eval;
	}

	// Razor pruning and extended razor pruning
	if (depth <= 1) {
		if (curr_eval + RAZOR_MARGIN < alpha) {
			// printf("razor prune\n");
			return qsearch(alpha, beta, DEPTH_ZERO);
		}
	}

	// Null move pruning
	if (depth >= 3 && !curr_state.is_check()) {
		// curr_state.print();
		curr_state.make_move(0);
		Value x = -search(depth - Depth(3), -beta, -alpha);
		// printf("x = %d, beta = %d\n", x, beta);
		if (x >= beta - TEMPO) {
			curr_state.unmake_move(0);
			return beta;
		}
		curr_state.unmake_move(0);
	}

	std::vector<int> moves = curr_state.list_moves();
	std::vector<pii> ordered_moves;

	bool mate = true;
	for (int i : moves) {
		int see_val = curr_state.see((i >> 9) & 7, (i >> 6) & 7, curr_state.to_move);
		if (depth < 5 && see_val < 0) {
			continue;
		}
		curr_state.make_move(i);
		if (!curr_state.king_attacked()) {
			mate = false;
			Bitstring hash = curr_state.get_hash();
			if (tt_exists[hash % TABLE_SIZE] && tt_hashes[hash % TABLE_SIZE] == hash) {
				ordered_moves.push_back({tt_evals[hash % TABLE_SIZE], i});
			} else {
				ordered_moves.push_back({eval(curr_state) + see_val, i});
			}
		}
		curr_state.unmake_move(i);
	}

	if (mate) {
		if (curr_state.is_check()) {
			// printf("checkmate\n");
			return MATED;
		} else {
			// printf("stalemate\n");
			return DRAWN;
		}
	}

	std::stable_sort(ordered_moves.begin(), ordered_moves.end());

	Value value = -VALUE_INFINITE;
	for (const pii& p : ordered_moves) {
		int move = p.second;
		// printf("Considering %s\n", curr_state.move_to_string(move).c_str());

		curr_state.make_move(move);
		Value x = -search(depth - ONE_PLY, -beta, -alpha);
		curr_state.unmake_move(move);

		value = std::max(value, x);
		alpha = std::max(alpha, value);

		if (alpha >= beta) {
			// printf("alpha beta cutoff: %d\n", alpha);
			return alpha;
		}
	}

	replace_tt(key, depth, value, curr_board_hash, curr_state.full_move);

	// printf("done searching, returned %d\n", value);
	// curr_state.print();

	return value;
}

// Only searches captures and queen promotions to avoid horizon effect
Value qsearch(Value alpha, Value beta, Depth depth) {
	qsearch_nodes++;

	depth_qsearched = std::min(depth_qsearched, depth);

	// printf("qsearch(%d, %d)\n", alpha, beta);
	// curr_state.print();

	Bitstring curr_board_hash = curr_state.get_hash();
	Bitstring key = curr_board_hash % TABLE_SIZE;

	if (tt_exists[key] && tt_depths[key] >= DEPTH_QS_NO_CHECKS && tt_hashes[key] == curr_board_hash) {
		// printf("tt hit: %d\n", tt_evals[key]);
		qsearch_hits++;
		return tt_evals[key];
	}

	if (curr_state.adjucation()) {
		// printf("adjucation\n");
		return DRAWN;
	}

	// if (curr_state.king_attacked()){
	// 	// printf("king attacked\n");
	// 	return MATE;
	// }

	Value curr_eval;
	if (tt_exists[key] && tt_hashes[key] == curr_board_hash) {
		// tt entry can be used as more accurate static eval
		curr_eval = tt_evals[key];
	} else {
		curr_eval = eval(curr_state, false, use_nnue);
	}

	if (depth < qs_depth_floor) {
		return curr_eval;
	}
	// if (mcts_prob > rng()) {
	// 	return curr_eval;
	// }

	// Futility pruning
	if (depth - qs_depth_floor < 5 && (curr_eval - futility_margin(depth - qs_depth_floor) >= beta)) {
		// printf("futility prune: %d\n", curr_eval);
		return curr_eval;
	}

	std::vector<pii> ordered_moves;

	bool mate = true;
	for (int i : curr_state.list_moves()) {
		if (curr_state.see((i >> 9) & 7, (i >> 6) & 7, curr_state.to_move) < 0) {
			continue;
		}
		curr_state.make_move(i);
		if (!curr_state.king_attacked()) {
			mate = false;
			if ((((i >> 15) & 7) != 0) || ((((i >> 18) & 3) == 2) && (((i >> 20) & 3) == 3))) {
				Bitstring hash = curr_state.get_hash();
				if (tt_exists[hash % TABLE_SIZE] && tt_hashes[hash % TABLE_SIZE] == hash) {
					// printf("using tt for eval of move %s\n", curr_state.move_to_string(i).c_str());
					ordered_moves.push_back({tt_evals[hash % TABLE_SIZE], i});
				} else {
					ordered_moves.push_back({eval(curr_state), i});
				}
			}
		}
		curr_state.unmake_move(i);
	}
	if (mate) {
		if (curr_state.is_check()) {
			// printf("checkmate\n");
			return MATED;
		} else {
			// printf("stalemate\n");
			return DRAWN;
		}
	}

	if (break_now || ordered_moves.size() == 0) {
		// printf("no moves: %d\n", curr_eval);
		return curr_eval;
	}

	if (curr_eval >= beta) { // Standing pat
		// printf("stand-pat: %d\n", curr_eval);
		return curr_eval;
	}

	// printf("static eval = %d\n", curr_eval);

	Value value = curr_eval;
	alpha = std::max(alpha, value);

	std::stable_sort(ordered_moves.begin(), ordered_moves.end());

	for (const pii& p : ordered_moves) {
		int move = p.second;
		// printf("Considering %s\n", curr_state.move_to_string(move).c_str());

		curr_state.make_move(move);
		Value x = -qsearch(-beta, -alpha, depth - ONE_PLY);
		curr_state.unmake_move(move);

		value = std::max(value, x);
		alpha = std::max(alpha, value);

		if (alpha >= beta) {
			// printf("alpha beta cutoff: %d\n", alpha);
			return alpha;
		}
	}

	replace_tt(key, depth - qs_depth_floor - Depth(10), value, curr_board_hash, curr_state.full_move);

	// printf("done qsearching, returned %d\n", value);
	// curr_state.print();

	return value;
}
