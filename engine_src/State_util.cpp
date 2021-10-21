#include "State.h"
#include "psqt.h"

#pragma GCC target("avx2")
#pragma GCC optimize("Ofast")
#pragma GCC optimization("unroll-loops")

void state::replace_board(int row, int col, int piece) {
	int orig_piece = board[row][col];
	board_hash ^= rand_bitstrings[(row << 3) + col][orig_piece + 6];
	cnts[orig_piece + 6]--;
	if (orig_piece != 0) {
		for (int i = 0; i < (int)piecelists[orig_piece + 6].size(); i++) {
			if (piecelists[orig_piece + 6][i].first == row && piecelists[orig_piece + 6][i].second == col) {
				piecelists[orig_piece + 6].erase(piecelists[orig_piece + 6].begin() + i);
				break;
			}
		}
	}
	curr_psqt -= get_psqt(orig_piece, row, col);
	if (board[row][col] == WP) {
		if (white_pawn_counts[col] >= 2)
			doubled_white -= white_pawn_counts[col];
		white_pawn_counts[col]--;
		if (white_pawn_counts[col] >= 2)
			doubled_white += white_pawn_counts[col];
	} else if (board[row][col] == BP) {
		if (black_pawn_counts[col] >= 2)
			doubled_black -= black_pawn_counts[col];
		black_pawn_counts[col]--;
		if (black_pawn_counts[col] >= 2)
			doubled_black += black_pawn_counts[col];
	}
	if (orig_piece != 0) {
		nnue_input[((abs(orig_piece) - 1) << 6) + (row << 3) + col] = 0;
	}

	board_hash ^= rand_bitstrings[(row << 3) + col][piece + 6];
	board[row][col] = piece;
	cnts[piece + 6]++;
	if (piece != 0) {
		piecelists[piece + 6].push_back({row, col});
	}
	curr_psqt += get_psqt(piece, row, col);
	if (board[row][col] == WP) {
		if (white_pawn_counts[col] >= 2)
			doubled_white -= white_pawn_counts[col];
		white_pawn_counts[col]++;
		if (white_pawn_counts[col] >= 2)
			doubled_white += white_pawn_counts[col];
	} else if (board[row][col] == BP) {
		if (black_pawn_counts[col] >= 2)
			doubled_black -= black_pawn_counts[col];
		black_pawn_counts[col]++;
		if (black_pawn_counts[col] >= 2)
			doubled_black += black_pawn_counts[col];
	}
	if (piece != 0) {
		nnue_input[((abs(piece) - 1) << 6) + (row << 3) + col] = (piece < 0 ? -1 : 1);
	}
}

bool state::adjucation() {
	if (fifty_move.top() >= 50)
		return true;
	if (cnts[WP + 6] == 0 && cnts[BP + 6] == 0) {
		if (3 * cnts[WB + 6] + 3 * cnts[WN + 6] + 5 * cnts[WR + 6] + 7 * cnts[WQ + 6] < 5) {
			if (3 * cnts[BB + 6] + 3 * cnts[BN + 6] + 5 * cnts[BR + 6] + 7 * cnts[BQ + 6] < 5) {
				return true;
			}
		}
		if (cnts[WB + 6] == 0 && cnts[BB + 6] == 0 && cnts[WR + 6] == 0 && cnts[BR + 6] == 0 && cnts[WQ + 6] == 0 && cnts[BQ + 6] == 0) {
			return true;
		}
	}
	return false;
}

// returns 2 if checkmate, 1 if stalemate, and 0 otherwise
int state::mate() {
	for (int i : list_moves()) {
		make_move(i);
		if (!king_attacked()) {
			unmake_move(i);
			return 0;
		}
		unmake_move(i);
	}
	if (is_check())
		return 2;
	else
		return 1;
}

// lowest piece of the opposite color that is attacking a square
int state::attacking(int row, int col, bool color) {
	if (color) {
		if (!out_of_bounds(row - 1, col - 1)) {
			if (board[row - 1][col - 1] == BP)
				return 1;
		}
		if (!out_of_bounds(row - 1, col + 1)) {
			if (board[row - 1][col + 1] == BP)
				return 1;
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == BN)
				return 2;
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == BB)
					return 3;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == BR)
					return 4;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == BQ)
					return 5;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == BK)
				return 6;
		}
	} else {
		if (!out_of_bounds(row + 1, col - 1)) {
			if (board[row + 1][col - 1] == WP)
				return 1;
		}
		if (!out_of_bounds(row + 1, col + 1)) {
			if (board[row + 1][col + 1] == WP)
				return 1;
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == WN)
				return 2;
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == WB)
					return 3;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == WR)
					return 4;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == WQ)
					return 5;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == WK)
				return 6;
		}
	}
	return 7;
}
