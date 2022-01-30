#include "State.h"
#include "psqt.h"

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
// Square of the lowest piece attacking the square
int state::attacker(int row, int col, bool color) {
	if (color) {
		if (!out_of_bounds(row - 1, col - 1)) {
			if (board[row - 1][col - 1] == BP)
				return make_square(row - 1, col - 1);
		}
		if (!out_of_bounds(row - 1, col + 1)) {
			if (board[row - 1][col + 1] == BP)
				return make_square(row - 1, col + 1);
		}
		for (int i = 0; i < 8; i++) {
			if (!out_of_bounds(row + dr_knight[i], col + dc_knight[i]) && board[row + dr_knight[i]][col + dc_knight[i]] == BN) {
				return make_square(row + dr_knight[i], col + dc_knight[i]);
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == BB)
					return make_square(row + dr_bishop[j] * i, col + dc_bishop[j] * i);
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == BR)
					return make_square(row + dr_rook[j] * i, col + dc_rook[j] * i);
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == BQ)
					return make_square(row + dr_queen[j] * i, col + dc_queen[j] * i);
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == BK)
				return make_square(row + dr_king[i], col + dc_king[i]);
		}
	} else {
		if (!out_of_bounds(row + 1, col - 1)) {
			if (board[row + 1][col - 1] == WP)
				return make_square(row + 1, col - 1);
		}
		if (!out_of_bounds(row + 1, col + 1)) {
			if (board[row + 1][col + 1] == WP)
				return make_square(row + 1, col + 1);
		}
		for (int i = 0; i < 8; i++) {
			if (!out_of_bounds(row + dr_knight[i], col + dc_knight[i]) && board[row + dr_knight[i]][col + dc_knight[i]] == WN) {
				return make_square(row + dr_knight[i], col + dc_knight[i]);
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == WB)
					return make_square(row + dr_bishop[j] * i, col + dc_bishop[j] * i);
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == WR)
					return make_square(row + dr_rook[j] * i, col + dc_rook[j] * i);
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++) {
			for (int i = 1; i < 8; i++) {
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == WQ)
					return make_square(row + dr_queen[j] * i, col + dc_queen[j] * i);
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++) {
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == WK)
				return make_square(row + dr_king[i], col + dc_king[i]);
		}
	}
	return -1;
}

// Static exchange evaluation function
int state::see(int row, int col, bool color) {
	if (color && board[row][col] > 0) {
		return 0;
	}
	if (!color && board[row][col] < 0) {
		return 0;
	}
	std::vector<int> white_attacking, black_attacking;
	if (!out_of_bounds(row - 1, col - 1)) {
		if (board[row - 1][col - 1] == BP)
			black_attacking.push_back(1);
	}
	if (!out_of_bounds(row - 1, col + 1)) {
		if (board[row - 1][col + 1] == BP)
			black_attacking.push_back(1);
	}
	for (int i = 0; i < 8; i++) {
		if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
			continue;
		if (board[row + dr_knight[i]][col + dc_knight[i]] == BN)
			black_attacking.push_back(2);
	}
	for (int j = 0; j < 4; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
				break;
			if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == BB)
				black_attacking.push_back(3);
			if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
				break;
		}
	}
	for (int j = 0; j < 4; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
				break;
			if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == BR)
				black_attacking.push_back(4);
			if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
				break;
		}
	}
	for (int j = 0; j < 8; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
				break;
			if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == BQ)
				black_attacking.push_back(5);
			if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
				break;
		}
	}
	for (int i = 0; i < 8; i++) {
		if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
			continue;
		if (board[row + dr_king[i]][col + dc_king[i]] == BK)
			black_attacking.push_back(6);
	}
	if (!out_of_bounds(row + 1, col - 1)) {
		if (board[row + 1][col - 1] == WP)
			white_attacking.push_back(1);
	}
	if (!out_of_bounds(row + 1, col + 1)) {
		if (board[row + 1][col + 1] == WP)
			white_attacking.push_back(1);
	}
	for (int i = 0; i < 8; i++) {
		if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
			continue;
		if (board[row + dr_knight[i]][col + dc_knight[i]] == WN)
			white_attacking.push_back(2);
	}
	for (int j = 0; j < 4; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
				break;
			if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == WB)
				white_attacking.push_back(3);
			if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
				break;
		}
	}
	for (int j = 0; j < 4; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
				break;
			if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == WR)
				white_attacking.push_back(4);
			if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
				break;
		}
	}
	for (int j = 0; j < 8; j++) {
		for (int i = 1; i < 8; i++) {
			if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
				break;
			if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == WQ)
				white_attacking.push_back(5);
			if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
				break;
		}
	}
	for (int i = 0; i < 8; i++) {
		if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
			continue;
		if (board[row + dr_king[i]][col + dc_king[i]] == WK)
			white_attacking.push_back(6);
	}
	// std::cout << "white_attacking:\n";
	// for (int i : white_attacking) {
	// 	std::cout << i << " ";
	// }
	// std::cout << std::endl;
	// std::cout << "black_attacking:\n";
	// for (int i : black_attacking) {
	// 	std::cout << i << " ";
	// }
	// std::cout << std::endl;
	if (color) {
		if (white_attacking.size() == 0) {
			return 0;
		}
		int res = 0;
		if (board[row][col] < 0) {
			res += piece_vals[-board[row][col]];
		}
		for (int i = 0; i < std::min((int)white_attacking.size() - 1, (int)black_attacking.size()); i++) {
			res -= piece_vals[white_attacking[i]];
			if (res > 0) {
				return res;
			}
			res += piece_vals[black_attacking[i]];
		}
		if (black_attacking.size() >= white_attacking.size()) {
			res -= piece_vals[white_attacking[white_attacking.size() - 1]];
		}
		return res;
	} else {
		if (black_attacking.size() == 0) {
			return 0;
		}
		int res = 0;
		if (board[row][col] > 0) {
			res += piece_vals[board[row][col]];
		}
		for (int i = 0; i < std::min((int)white_attacking.size(), (int)black_attacking.size() - 1); i++) {
			res -= piece_vals[black_attacking[i]];
			if (res > 0) {
				return res;
			}
			res += piece_vals[white_attacking[i]];
		}
		if (black_attacking.size() <= white_attacking.size()) {
			res -= piece_vals[black_attacking[black_attacking.size() - 1]];
		}
		return res;
	}
}

// SLOW
// int state::see(int row, int col, bool color) {
// 	if ((color && board[row][col] > 0) || (!color && board[row][col] < 0)) {
// 		return 0;
// 	}
// 	int attack_square = attacker(row, col, !color);
// 	if (attack_square == -1) {
// 		return 0;
// 	}
// 	int res = piece_vals[abs(board[row][col])];
// 	int move = attack_square + (row << 9) + (col << 6) + (abs(board[attack_square >> 3][attack_square & 7]) << 12) + (abs(board[row][col]) << 15);
// 	bool orig_to_move = to_move;
// 	to_move = color;
// 	make_move(move);
// 	res -= see(row, col, !color);
// 	to_move = !color;
// 	unmake_move(move);
// 	to_move = orig_to_move;
// 	return std::max(0, res);
// }
