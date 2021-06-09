#include "State.h"

// DEPRECATED (kind of)
void state::replace_board(int row, int col, int piece)
{
	board_hash ^= rand_bitstrings[(row << 3) + col][board[row][col] + 6];
	board_hash ^= rand_bitstrings[(row << 3) + col][piece + 6];
	board[row][col] = piece;
}
void state::_replace_board(int row, int col, int piece)
{
	board_hash ^= rand_bitstrings[(row << 3) + col][board[row][col] + 6];
	cnts[board[row][col] + 6]--;
	if (board[row][col] == WP)
	{
		whitepawn_row_sum -= 7 - row;
		if (white_pawn_counts[col] >= 2)
			doubled_white -= white_pawn_counts[col];
		white_pawn_counts[col]--;
		if (white_pawn_counts[col] >= 2)
			doubled_white += white_pawn_counts[col];
		white_center -= pawn_center[row][col];
		for (int i = 0; i < whitepawns.size(); i++)
		{
			if (whitepawns[i].first == row && whitepawns[i].second == col)
			{
				whitepawns.erase(whitepawns.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BP)
	{
		blackpawn_row_sum -= row;
		if (black_pawn_counts[col] >= 2)
			doubled_black -= black_pawn_counts[col];
		black_pawn_counts[col]--;
		if (black_pawn_counts[col] >= 2)
			doubled_black += black_pawn_counts[col];
		black_center -= pawn_center[7 - row][col];
		for (int i = 0; i < blackpawns.size(); i++)
		{
			if (blackpawns[i].first == row && blackpawns[i].second == col)
			{
				blackpawns.erase(blackpawns.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == WN)
	{
		white_devel -= knight_devel[row][col];
		white_center -= knight_center[row][col];
		for (int i = 0; i < whiteknights.size(); i++)
		{
			if (whiteknights[i].first == row && whiteknights[i].second == col)
			{
				whiteknights.erase(whiteknights.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BN)
	{
		black_devel -= knight_devel[7 - row][col];
		black_center -= knight_center[7 - row][col];
		for (int i = 0; i < blackknights.size(); i++)
		{
			if (blackknights[i].first == row && blackknights[i].second == col)
			{
				blackknights.erase(blackknights.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == WB)
	{
		white_devel -= bishop_devel[row][col];
		for (int i = 0; i < whitebishops.size(); i++)
		{
			if (whitebishops[i].first == row && whitebishops[i].second == col)
			{
				whitebishops.erase(whitebishops.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BB)
	{
		black_devel -= bishop_devel[7 - row][col];
		for (int i = 0; i < blackbishops.size(); i++)
		{
			if (blackbishops[i].first == row && blackbishops[i].second == col)
			{
				blackbishops.erase(blackbishops.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == WR)
	{
		for (int i = 0; i < whiterooks.size(); i++)
		{
			if (whiterooks[i].first == row && whiterooks[i].second == col)
			{
				whiterooks.erase(whiterooks.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BR)
	{
		for (int i = 0; i < blackrooks.size(); i++)
		{
			if (blackrooks[i].first == row && blackrooks[i].second == col)
			{
				blackrooks.erase(blackrooks.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == WQ)
	{
		for (int i = 0; i < whitequeens.size(); i++)
		{
			if (whitequeens[i].first == row && whitequeens[i].second == col)
			{
				whitequeens.erase(whitequeens.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BQ)
	{
		for (int i = 0; i < blackqueens.size(); i++)
		{
			if (blackqueens[i].first == row && blackqueens[i].second == col)
			{
				blackqueens.erase(blackqueens.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == WK)
	{
		for (int i = 0; i < whitekings.size(); i++)
		{
			if (whitekings[i].first == row && whitekings[i].second == col)
			{
				whitekings.erase(whitekings.begin() + i);
				break;
			}
		}
	}
	else if (board[row][col] == BK)
	{
		for (int i = 0; i < blackkings.size(); i++)
		{
			if (blackkings[i].first == row && blackkings[i].second == col)
			{
				blackkings.erase(blackkings.begin() + i);
				break;
			}
		}
	}
	board_hash ^= rand_bitstrings[(row << 3) + col][piece + 6];
	board[row][col] = piece;
	cnts[piece + 6]++;
	if (board[row][col] == WP)
	{
		whitepawn_row_sum += 7 - row;
		if (white_pawn_counts[col] >= 2)
			doubled_white -= white_pawn_counts[col];
		white_pawn_counts[col]++;
		if (white_pawn_counts[col] >= 2)
			doubled_white += white_pawn_counts[col];
		white_center += pawn_center[row][col];
		whitepawns.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BP)
	{
		blackpawn_row_sum += row;
		if (black_pawn_counts[col] >= 2)
			doubled_black -= black_pawn_counts[col];
		black_pawn_counts[col]++;
		if (black_pawn_counts[col] >= 2)
			doubled_black += black_pawn_counts[col];
		black_center += pawn_center[7 - row][col];
		blackpawns.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == WN)
	{
		white_center += knight_center[row][col];
		white_devel += knight_devel[row][col];
		whiteknights.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BN)
	{
		black_center += knight_center[7 - row][col];
		black_devel += knight_devel[7 - row][col];
		blackknights.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == WB)
	{
		white_devel += bishop_devel[row][col];
		whitebishops.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BB)
	{
		black_devel += bishop_devel[7 - row][col];
		blackbishops.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == WR)
	{
		whiterooks.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BR)
	{
		blackrooks.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == WQ)
	{
		whitequeens.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BQ)
	{
		blackqueens.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == WK)
	{
		whitekings.push_back(std::make_pair(row, col));
	}
	else if (board[row][col] == BK)
	{
		blackkings.push_back(std::make_pair(row, col));
	}
}

bool state::adjucation()
{
	if (fifty_move.top() >= 50)
		return true;
	if (cnts[WP + 6] == 0 && cnts[BP + 6] == 0)
	{
		if (3 * cnts[WB + 6] + 3 * cnts[WN + 6] + 5 * cnts[WR + 6] + 7 * cnts[WQ + 6] < 5)
		{
			if (3 * cnts[BB + 6] + 3 * cnts[BN + 6] + 5 * cnts[BR + 6] + 7 * cnts[BQ + 6] < 5)
			{
				return true;
			}
		}
		if (cnts[WB + 6] == 0 && cnts[BB + 6] == 0 && cnts[WR + 6] == 0 && cnts[BR + 6] == 0 && cnts[WQ + 6] == 0 && cnts[BQ + 6] == 0)
		{
			return true;
		}
	}
	return false;
}

// returns 2 if checkmate, 1 if stalemate, and 0 otherwise
int state::mate()
{
	for (int i : list_moves())
	{
		make_move(i);
		if (!to_move)
		{
			if (attacking(whitekings[0].first, whitekings[0].second, true) >= 7)
			{
				unmake_move(i);
				return 0;
			}
		}
		else
		{
			if (attacking(blackkings[0].first, blackkings[0].second, false) >= 7)
			{
				unmake_move(i);
				return 0;
			}
		}
		unmake_move(i);
	}
	if (to_move)
	{
		if (attacking(whitekings[0].first, whitekings[0].second, true) < 7)
			return 2;
		else
			return 1;
	}
	else
	{
		if (attacking(blackkings[0].first, blackkings[0].second, false) < 7)
			return 2;
		else
			return 1;
	}
}

//lowest piece of the opposite color that is attacking a square
int state::attacking(int row, int col, bool color)
{
	if (color)
	{
		if (!out_of_bounds(row - 1, col - 1))
		{
			if (board[row - 1][col - 1] == BP)
				return 1;
		}
		if (!out_of_bounds(row - 1, col + 1))
		{
			if (board[row - 1][col + 1] == BP)
				return 1;
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == BN)
				return 2;
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == BB)
					return 3;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == BR)
					return 4;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == BQ)
					return 5;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == BK)
				return 6;
		}
	}
	else
	{
		if (!out_of_bounds(row + 1, col - 1))
		{
			if (board[row + 1][col - 1] == WP)
				return 1;
		}
		if (!out_of_bounds(row + 1, col + 1))
		{
			if (board[row + 1][col + 1] == WP)
				return 1;
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == WN)
				return 2;
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == WB)
					return 3;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_rook[j] * i, col + dc_rook[j] * i))
					break;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] == WR)
					return 4;
				if (board[row + dr_rook[j] * i][col + dc_rook[j] * i] != 0)
					break;
			}
		}
		for (int j = 0; j < 8; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_queen[j] * i, col + dc_queen[j] * i))
					break;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] == WQ)
					return 5;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == WK)
				return 6;
		}
	}
	return 7;
}
