#include "State.h"

void state::unmake_move(int move) {
	if (move == -1) {
		// throw std::exception("Trying to make an illegal move");
		return;
	}

	to_move = !to_move;

	int row_init = (move >> 3) & 7, row_final = (move >> 9) & 7, col_init = move & 7, col_final = (move >> 6) & 7;
	int piece = (move >> 12) & 7, piece_captured = (move >> 15) & 7;

	int color = to_move ? 1 : -1;

	fifty_move.pop();

	wk_rights.pop();
	wq_rights.pop();
	bk_rights.pop();
	bq_rights.pop();

	en_passant_target.pop();

	if (!to_move) {
		full_move--;
	}

	if (move == 0) {
		return;
	}

	if (((move >> 18) & 3) == 3) {
		if (to_move) {
			white_castled = false;
			if ((move >> 20) == 1) { // kingside castle
				replace_board(7, 6, 0);
				replace_board(7, 5, 0);
				replace_board(7, 7, WR);
				replace_board(7, 4, WK);
			} else {
				replace_board(7, 3, 0);
				replace_board(7, 2, 0);
				replace_board(7, 0, WR);
				replace_board(7, 4, WK);
			}
		} else {
			black_castled = true;
			if ((move >> 20) == 1) { // kingside castle
				replace_board(0, 6, 0);
				replace_board(0, 5, 0);
				replace_board(0, 7, BR);
				replace_board(0, 4, BK);
			} else {
				replace_board(0, 3, 0);
				replace_board(0, 2, 0);
				replace_board(0, 0, BR);
				replace_board(0, 4, BK);
			}
		}
	} else if (((move >> 18) & 3) == 2) {
		replace_board(row_final, col_final, piece_captured * color * -1);
		replace_board(row_init, col_init, WP * color);
	} else if (((move >> 18) & 3) == 1) {
		if (to_move) {
			replace_board(row_final, col_final, 0);
			replace_board(row_init, col_init, WP);
			replace_board(row_final + 1, col_final, BP);
		} else {
			replace_board(row_final, col_final, 0);
			replace_board(row_init, col_init, BP);
			replace_board(row_final - 1, col_final, WP);
		}
	} else {
		replace_board(row_init, col_init, piece * color);
		replace_board(row_final, col_final, piece_captured * color * -1);
	}
}
