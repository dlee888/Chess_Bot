#include "State.h"

void state::make_move(int move) {
	if (move == -1) {
		// throw std::exception("Trying to make an illegal move");
		return;
	}

	int row_init = (move >> 3) & 7, row_final = (move >> 9) & 7, col_init = move & 7, col_final = (move >> 6) & 7;
	int piece = (move >> 12) & 7, piece_captured = (move >> 15) & 7;

	fifty_move.push(fifty_move.top() + 1);

	if (piece_captured != 0) {
		fifty_move.pop();
		fifty_move.push(0);
	}

	int color = to_move ? 1 : -1;

	wk_rights.push(wk_rights.top());
	wq_rights.push(wq_rights.top());
	bk_rights.push(bk_rights.top());
	bq_rights.push(bq_rights.top());

	en_passant_target.push(-1);

	if (!to_move)
		full_move++;

	if (((move >> 18) & 3) == 3) {
		if (to_move) {
			white_castled = true;
			if ((move >> 20) == 1) { // kingside castle
				replace_board(7, 6, WK);
				replace_board(7, 5, WR);
				replace_board(7, 7, 0);
				replace_board(7, 4, 0);
				wk_rights.pop();
				wk_rights.push(false);
				wq_rights.pop();
				wq_rights.push(false);
			} else {
				replace_board(7, 3, WR);
				replace_board(7, 2, WK);
				replace_board(7, 0, 0);
				replace_board(7, 4, 0);
				wk_rights.pop();
				wk_rights.push(false);
				wq_rights.pop();
				wq_rights.push(false);
			}
		} else {
			black_castled = true;
			if ((move >> 20) == 1) { // kingside castle
				replace_board(0, 6, BK);
				replace_board(0, 5, BR);
				replace_board(0, 7, 0);
				replace_board(0, 4, 0);
				bk_rights.pop();
				bk_rights.push(false);
				bq_rights.pop();
				bq_rights.push(false);
			} else {
				replace_board(0, 3, BR);
				replace_board(0, 2, BK);
				replace_board(0, 0, 0);
				replace_board(0, 4, 0);
				bk_rights.pop();
				bk_rights.push(false);
				bq_rights.pop();
				bq_rights.push(false);
			}
		}
	} else if (((move >> 18) & 3) == 2) {
		fifty_move.pop();
		fifty_move.push(0);
		int promote_to = (move >> 20) + 2;

		replace_board(row_final, col_final, promote_to * color);
		replace_board(row_init, col_init, 0);

		if (piece_captured == WR) {
			if (to_move) {
				if (row_final == 0 && col_final == 0) {
					bq_rights.pop();
					bq_rights.push(false);
				}
				if (row_final == 0 && col_final == 7) {
					bk_rights.pop();
					bk_rights.push(false);
				}
			} else {
				if (row_final == 7 && col_final == 0) {
					wq_rights.pop();
					wq_rights.push(false);
				}
				if (row_final == 7 && col_final == 7) {
					wk_rights.pop();
					wk_rights.push(false);
				}
			}
		}
	} else if (((move >> 18) & 3) == 1) {
		if (to_move) {
			replace_board(row_final, col_final, WP);
			replace_board(row_init, col_init, 0);
			replace_board(row_final + 1, col_final, 0);

			fifty_move.pop();
			fifty_move.push(0);
		} else {
			replace_board(row_final, col_final, BP);
			replace_board(row_init, col_init, 0);
			replace_board(row_final - 1, col_final, 0);

			fifty_move.pop();
			fifty_move.push(0);
		}
	} else {
		// making the move
		replace_board(row_init, col_init, 0);
		replace_board(row_final, col_final, piece * color);

		if (piece == WP) {
			fifty_move.pop();
			fifty_move.push(0);
			if (abs(row_init - row_final) == 2) {
				en_passant_target.pop();
				en_passant_target.push((((row_init + row_final) / 2) << 3) + col_init);
			}
		} else if (piece == WR) {
			if (to_move) {
				if (row_init == 7 && col_init == 0) {
					wq_rights.pop();
					wq_rights.push(false);
				}
				if (row_init == 7 && col_init == 7) {
					wk_rights.pop();
					wk_rights.push(false);
				}
			} else {
				if (row_init == 0 && col_init == 0) {
					bq_rights.pop();
					bq_rights.push(false);
				}
				if (row_init == 0 && col_init == 7) {
					bk_rights.pop();
					bk_rights.push(false);
				}
			}
		} else if (piece == WK) {
			if (to_move) {
				wk_rights.pop();
				wk_rights.push(false);
				wq_rights.pop();
				wq_rights.push(false);
			} else {
				bk_rights.pop();
				bk_rights.push(false);
				bq_rights.pop();
				bq_rights.push(false);
			}
		}

		if (piece_captured == WR) {
			if (to_move) {
				if (row_final == 0 && col_final == 0) {
					bq_rights.pop();
					bq_rights.push(false);
				}
				if (row_final == 0 && col_final == 7) {
					bk_rights.pop();
					bk_rights.push(false);
				}
			} else {
				if (row_final == 7 && col_final == 0) {
					wq_rights.pop();
					wq_rights.push(false);
				}
				if (row_final == 7 && col_final == 7) {
					wk_rights.pop();
					wk_rights.push(false);
				}
			}
		}
	}
	to_move = !to_move;
}
