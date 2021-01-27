#include "State.h"

bool state::quiescent()
{
	for (pii p : whiteknights)
	{
		if (attacking(p.first, p.second, true) < WN)
			return false;
	}
	for (pii p : whitebishops)
	{
		if (attacking(p.first, p.second, true) < WN)
			return false;
	}
	for (pii p : whiterooks)
	{
		if (attacking(p.first, p.second, true) < WR)
			return false;
	}
	for (pii p : whitequeens)
	{
		if (attacking(p.first, p.second, true) < WQ)
			return false;
	}
	for (pii p : whitekings)
	{
		if (attacking(p.first, p.second, true) < WK)
			return false;
	}
	for (pii p : blackknights)
	{
		if (attacking(p.first, p.second, false) < WN)
			return false;
	}
	for (pii p : blackbishops)
	{
		if (attacking(p.first, p.second, false) < WN)
			return false;
	}
	for (pii p : blackrooks)
	{
		if (attacking(p.first, p.second, false) < WR)
			return false;
	}
	for (pii p : blackqueens)
	{
		if (attacking(p.first, p.second, false) < WQ)
			return false;
	}
	for (pii p : blackkings)
	{
		if (attacking(p.first, p.second, false) < WK)
			return false;
	}
	return true;
}

bool state::adjucation()
{
	if (fifty_move >= 50)
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

int state::num_attack(int row, int col, bool color)
{
	int num_attack = 0;
	if (color)
	{
		if (!out_of_bounds(row - 1, col - 1))
		{
			if (board[row - 1][col - 1] == BP)
				num_attack++;
		}
		if (!out_of_bounds(row - 1, col + 1))
		{
			if (board[row - 1][col + 1] == BP)
				num_attack++;
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == BN)
				num_attack++;
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == BB)
					num_attack++;
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
					num_attack++;
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
					num_attack++;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == BK)
				num_attack++;
		}
	}
	else
	{
		if (!out_of_bounds(row + 1, col - 1))
		{
			if (board[row + 1][col - 1] == WP)
				num_attack++;
		}
		if (!out_of_bounds(row + 1, col + 1))
		{
			if (board[row + 1][col + 1] == WP)
				num_attack++;
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_knight[i], col + dc_knight[i]))
				continue;
			if (board[row + dr_knight[i]][col + dc_knight[i]] == WN)
				num_attack++;
		}
		for (int j = 0; j < 4; j++)
		{
			for (int i = 1; i < 8; i++)
			{
				if (out_of_bounds(row + dr_bishop[j] * i, col + dc_bishop[j] * i))
					break;
				if (board[row + dr_bishop[j] * i][col + dc_bishop[j] * i] == WB)
					num_attack++;
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
					num_attack++;
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
					num_attack++;
				if (board[row + dr_queen[j] * i][col + dc_queen[j] * i] != 0)
					break;
			}
		}
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row + dr_king[i], col + dc_king[i]))
				continue;
			if (board[row + dr_king[i]][col + dc_king[i]] == WK)
				num_attack++;
		}
	}
	return num_attack;
}

bool state::illegal(int move){
	curr_state.make_move(move);
	if (!curr_state.to_move)
	{
		if (curr_state.attacking(whitekings[0].first, whitekings[0].second, true) != 7)
		{
			curr_state.unmake_move(move);
			return true;
		}
	}
	else
	{
		if (curr_state.attacking(blackkings[0].first, blackkings[0].second, false) != 7)
		{
			curr_state.unmake_move(move);
			return true;
		}
	}
	curr_state.unmake_move(move);
	return false;
}