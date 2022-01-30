#include "State.h"

std::vector<int> state::list_moves() {
	std::vector<int> res;
	if (to_move) {
		if (wk_rights.top() && !board[7][5] && !board[7][6] && attacking(7, 4, true) == 7 && attacking(7, 5, true) == 7 &&
			attacking(7, 6, true) == 7) {
			res.push_back(1835008);
		}
		if (wq_rights.top() && !board[7][2] && !board[7][3] && !board[7][1] && attacking(7, 4, true) == 7 && attacking(7, 3, true) == 7 &&
			attacking(7, 2, true) == 7) {
			res.push_back(2883584);
		}
		for (const pii& p : piecelists[WP + 6]) {
			if (board[p.first - 1][p.second] == 0) {
				if (p.first != 1) {
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second) << 6) + (WP << 12));
					if (p.first == 6 && board[4][p.second] == 0) {
						res.push_back(48 + p.second + ((32 + p.second) << 6) + (WP << 12));
					}
				} else {
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second) << 6) + (WP << 12) + 3670016);
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second) << 6) + (WP << 12) + 524288);
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second) << 6) + (WP << 12) + 1572864);
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second) << 6) + (WP << 12) + 2621440);
				}
			}
			if (!out_of_bounds(p.first - 1, p.second - 1)) {
				if (board[p.first - 1][p.second - 1] < 0) {
					if (p.first == 1) {
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second - 1]) << 15) + 3670016);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second - 1]) << 15) + 524288);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second - 1]) << 15) + 1572864);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second - 1]) << 15) + 2621440);
					} else {
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second - 1]) << 15));
					}
				} else if (((p.first - 1) << 3) + p.second - 1 == en_passant_target.top()) {
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second - 1) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[p.first - 1][p.second - 1]) << 15) + (1 << 18));
				}
			}
			if (!out_of_bounds(p.first - 1, p.second + 1)) {
				if (board[p.first - 1][p.second + 1] < 0) {
					if (p.first == 1) {
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second + 1]) << 15) + 3670016);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second + 1]) << 15) + 524288);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second + 1]) << 15) + 1572864);
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second + 1]) << 15) + 2621440);
					} else {
						res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first - 1][p.second + 1]) << 15));
					}
				} else if (((p.first - 1) << 3) + p.second + 1 == en_passant_target.top()) {
					res.push_back((p.first << 3) + p.second + ((((p.first - 1) << 3) + p.second + 1) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[p.first - 1][p.second + 1]) << 15) + (1 << 18));
				}
			}
		}
		for (const pii& p : piecelists[WN + 6]) {
			for (int i = 0; i < 8; i++) {
				int row_final = p.first + dr_knight[i], col_final = p.second + dc_knight[i];
				if (!out_of_bounds(row_final, col_final) && board[row_final][col_final] <= 0) {
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
				}
			}
		}
		for (const pii& p : piecelists[WB + 6]) {
			for (int j = 0; j < 4; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_bishop[j] * i, col_final = p.second + dc_bishop[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] > 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[WR + 6]) {
			for (int j = 0; j < 4; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_rook[j] * i, col_final = p.second + dc_rook[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] > 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[WQ + 6]) {
			for (int j = 0; j < 8; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_queen[j] * i, col_final = p.second + dc_queen[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] > 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[WK + 6]) {
			for (int i = 0; i < 8; i++) {
				int row_final = p.first + dr_king[i], col_final = p.second + dc_king[i];
				if (!out_of_bounds(row_final, col_final) && board[row_final][col_final] <= 0) {
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
				}
			}
		}
	} else {
		if (bk_rights.top() && !board[0][5] && !board[0][6] && attacking(0, 4, false) == 7 && attacking(0, 5, false) == 7 &&
			attacking(0, 6, false) == 7) {
			res.push_back(1835008);
		}
		if (bq_rights.top() && !board[0][2] && !board[0][3] && !board[0][1] && attacking(0, 4, false) == 7 && attacking(0, 3, false) == 7 &&
			attacking(0, 2, false) == 7) {
			res.push_back(2883584);
		}
		for (const pii& p : piecelists[BP + 6]) {
			if (board[p.first + 1][p.second] == 0) {
				if (p.first != 6) {
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second) << 6) + (WP << 12));
					if (p.first == 1) {
						if (board[3][p.second] == 0) {
							res.push_back(8 + p.second + ((24 + p.second) << 6) + (WP << 12));
						}
					}
				} else {
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second) << 6) + (WP << 12) + 3670016);
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second) << 6) + (WP << 12) + 2621440);
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second) << 6) + (WP << 12) + 1572864);
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second) << 6) + (WP << 12) + 524288);
				}
			}
			if (!out_of_bounds(p.first + 1, p.second - 1)) {
				if (board[p.first + 1][p.second - 1] > 0) {
					if (p.first == 6) {
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second - 1]) << 15) + 3670016);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second - 1]) << 15) + 524288);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second - 1]) << 15) + 1572864);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second - 1]) << 15) + 2621440);
					} else {
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second - 1]) << 15));
					}
				} else if (((p.first + 1) << 3) + p.second - 1 == en_passant_target.top()) {
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second - 1) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[p.first + 1][p.second - 1]) << 15) + (1 << 18));
				}
			}
			if (!out_of_bounds(p.first + 1, p.second + 1)) {
				if (board[p.first + 1][p.second + 1] > 0) {
					if (p.first == 6) {
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second + 1]) << 15) + 524288);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second + 1]) << 15) + 1572864);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second + 1]) << 15) + 2621440);
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second + 1]) << 15) + 3670016);
					} else {
						res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) +
									  (abs(board[p.first][p.second]) << 12) + (abs(board[p.first + 1][p.second + 1]) << 15));
					}
				} else if (((p.first + 1) << 3) + p.second + 1 == en_passant_target.top()) {
					res.push_back((p.first << 3) + p.second + ((((p.first + 1) << 3) + p.second + 1) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[p.first + 1][p.second + 1]) << 15) + (1 << 18));
				}
			}
		}
		for (const pii& p : piecelists[BN + 6]) {
			for (int i = 0; i < 8; i++) {
				int row_final = p.first + dr_knight[i], col_final = p.second + dc_knight[i];
				if (!out_of_bounds(row_final, col_final)) {
					if (board[row_final][col_final] >= 0) {
						res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
									  (abs(board[row_final][col_final]) << 15));
					}
				}
			}
		}
		for (const pii& p : piecelists[BB + 6]) {
			for (int j = 0; j < 4; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_bishop[j] * i, col_final = p.second + dc_bishop[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] < 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[BR + 6]) {
			for (int j = 0; j < 4; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_rook[j] * i, col_final = p.second + dc_rook[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] < 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[BQ + 6]) {
			for (int j = 0; j < 8; j++) {
				for (int i = 1; i < 8; i++) {
					int row_final = p.first + dr_queen[j] * i, col_final = p.second + dc_queen[j] * i;
					if (out_of_bounds(row_final, col_final) || board[row_final][col_final] < 0) {
						break;
					}
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
					if (board[row_final][col_final] != 0) {
						break;
					}
				}
			}
		}
		for (const pii& p : piecelists[BK + 6]) {
			for (int i = 0; i < 8; i++) {
				int row_final = p.first + dr_king[i], col_final = p.second + dc_king[i];
				if (!out_of_bounds(row_final, col_final) && board[row_final][col_final] >= 0) {
					res.push_back((p.first << 3) + p.second + (((row_final << 3) + col_final) << 6) + (abs(board[p.first][p.second]) << 12) +
								  (abs(board[row_final][col_final]) << 15));
				}
			}
		}
	}
	return res;
}