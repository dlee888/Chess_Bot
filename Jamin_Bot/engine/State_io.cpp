#include "State.h"

std::string state::to_piece(int x)
{
	if (x == BK)
		return "BK";
	if (x == BQ)
		return "BQ";
	if (x == BR)
		return "BR";
	if (x == BB)
		return "BB";
	if (x == BN)
		return "BN";
	if (x == BP)
		return "BP";
	if (x == WK)
		return "WK";
	if (x == WQ)
		return "WQ";
	if (x == WR)
		return "WR";
	if (x == WB)
		return "WB";
	if (x == WN)
		return "WN";
	if (x == WP)
		return "WP";
	return "  ";
}
int state::piece_to_int(char c)
{
	if (c == 'P')
		return 1;
	if (c == 'N')
		return 2;
	if (c == 'B')
		return 3;
	if (c == 'R')
		return 4;
	if (c == 'Q')
		return 5;
	if (c == 'K')
		return 6;
	return 0;
}

void state::print()
{
	for (int i = 0; i < 8; i++)
	{
		for (int j = 0; j < n; j++)
		{
			std::cout << "---";
		}
		std::cout << '\n';
		for (int j = 0; j < n; j++)
		{
			std::cout << "|" << to_piece(board[i][j]);
		}
		std::cout << "|\n";
	}
	for (int j = 0; j < n; j++)
	{
		std::cout << "---";
	}
	std::cout << "\n";
}

std::string state::move_to_string(int move)
{
	if (move == 1835008)
	{
		return "O-O           (1835008)";
	}
	if (move == 2883584)
	{
		return "O-O-O         (2883584)";
	}
	int row_init = (move >> 3) & 7, row_final = (move >> 9) & 7, col_init = move & 7, col_final = (move >> 6) & 7;
	int piece = (move >> 12) & 7;
	std::string res;
	res += to_piece(piece)[1];
	res += " on ";
	res += col_init + 'a';
	res += '8' - row_init;
	res += " to ";
	res += col_final + 'a';
	res += '8' - row_final;
	res += " (" + std::to_string(move) + ")";
	return res;
}

/*
turns algebraic notation into 'move' notation
A move is represented by a string of bits
First 6 bits = original position
Next 6 bits = final position
Next 3 bits = piece that is moved
Next 3 bits: If it is a capture, then the piece that is captured, or 0 if it is not a capture
Next 2 bits: This is for special moves
			0 = regular move
			1 = en passant
			2 = promotion
			3 = castle
Next 2 bits: This is also for special moves
			If it is a promotion, then the piece that is promoted to - 2
				For example, QUEEN = 5, so if the pawn is promoted to a queen, then the bits would by 5-2=3=11
			If it castle, 1 if kingside castle, 2 if queenside castle
note: the other 10 bits are not used
*/
int state::parse_move(std::string move)
{

	char last = move[move.size() - 1];
	while (last == '!' || last == '?' || last == '+' || last == '#')
	{
		move.erase(move.end() - 1);
		last = move[move.size() - 1];
	}

	if (move == "0-0")
	{
		if (to_move)
		{
			if (wk_rights.top() && !board[7][5] && !board[7][6] &&
				attacking(7, 4, true) == 7 && attacking(7, 5, true) == 7 && attacking(7, 6, true) == 7)
			{
				return 1835008;
			}
			else
			{
				return -1;
			}
		}
		else
		{
			if (bk_rights.top() && !board[0][5] && !board[0][6] &&
				attacking(0, 4, false) == 7 && attacking(0, 5, false) == 7 && attacking(0, 6, false) == 7)
			{
				return 1835008;
			}
			else
			{
				return -1;
			}
		}
	}
	else if (move == "0-0-0")
	{
		if (to_move)
		{
			if (wq_rights.top() && !board[7][2] && !board[7][3] && !board[7][1] &&
				attacking(7, 4, true) == 7 && attacking(7, 3, true) == 7 && attacking(7, 2, true) == 7)
			{
				return 2883584;
			}
			else
			{
				return -1;
			}
		}
		else
		{
			if (bq_rights.top() && !board[0][2] && !board[0][3] && !board[0][1] &&
				attacking(0, 4, false) == 7 && attacking(0, 3, false) == 7 && attacking(0, 2, false) == 7)
			{
				return 2883584;
			}
			else
			{
				return -1;
			}
		}
	}

	if (move[0] == 'K')
	{
		int row_final, col_final;
		if (move[1] == 'x')
		{
			row_final = '8' - move[3];
			col_final = move[2] - 'a';
		}
		else
		{
			row_final = '8' - move[2];
			col_final = move[1] - 'a';
		}
		int row_init = -1, col_init = -1;
		int king = BK;
		if (to_move)
			king = WK;
		for (int i = 0; i < 8; i++)
		{
			if (out_of_bounds(row_final - dr_king[i], col_final - dc_king[i]))
				continue;
			if (board[row_final - dr_king[i]][col_final - dc_king[i]] == king)
			{
				row_init = row_final - dr_king[i];
				col_init = col_final - dc_king[i];
				break;
			}
		}
		if (row_init == -1)
			return -1;
		return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) + (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
	}
	else if (move[0] == 'Q')
	{
		int row_final, col_final;
		if (move[1] == 'x')
		{
			row_final = '8' - move[3];
			col_final = move[2] - 'a';
		}
		else
		{
			row_final = '8' - move[2];
			col_final = move[1] - 'a';
		}
		int queen = BQ;
		if (to_move)
			queen = WQ;
		for (int x = 0; x < 8; x++)
		{
			for (int i = 1; i < 8; i++)
			{
				int row_init = row_final + dr_queen[x] * i, col_init = col_final + dc_queen[x] * i;
				if (out_of_bounds(row_init, col_init))
					break;
				if (board[row_init][col_init] == queen)
				{
					return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) + (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
				}
				if (board[row_init][col_init] != 0)
				{
					break;
				}
			}
		}
		return -1;
	}
	else if (move[0] == 'B')
	{
		int row_final, col_final;
		if (move[1] == 'x')
		{
			row_final = '8' - move[3];
			col_final = move[2] - 'a';
		}
		else
		{
			row_final = '8' - move[2];
			col_final = move[1] - 'a';
		}
		int bishop = BB;
		if (to_move)
			bishop = WB;
		for (int x = 0; x < 4; x++)
		{
			for (int i = 1; i < 8; i++)
			{
				int row_init = row_final + dr_bishop[x] * i, col_init = col_final + dc_bishop[x] * i;
				if (out_of_bounds(row_init, col_init))
					break;
				if (board[row_init][col_init] == bishop)
				{
					return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) + (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
				}
				if (board[row_init][col_init] != 0)
				{
					break;
				}
			}
		}
		return -1;
	}
	else if (move[0] == 'R')
	{
		int row_final, col_final;
		int flag = 0; // 0 if this is a regular move, 1 if it is like Rab1, 2 if it is like R1c2
		if (move[1] == 'x')
		{
			row_final = '8' - move[3];
			col_final = move[2] - 'a';
		}
		else if (move[2] == 'x')
		{
			if (move[1] <= 'h' && move[1] >= 'a')
			{
				flag = 1;
			}
			else
			{
				flag = 2;
			}
			row_final = '8' - move[4];
			col_final = move[3] - 'a';
		}
		else
		{
			if (move.size() == 3)
			{
				row_final = '8' - move[2];
				col_final = move[1] - 'a';
			}
			else
			{
				if (move[1] <= 'h' && move[1] >= 'a')
				{
					flag = 1;
				}
				else
				{
					flag = 2;
				}
				row_final = '8' - move[3];
				col_final = move[2] - 'a';
			}
		}
		int rook = BR;
		if (to_move)
			rook = WR;
		for (int x = 0; x < 4; x++)
		{
			for (int i = 1; i < 8; i++)
			{
				int row_init = row_final + dr_rook[x] * i, col_init = col_final + dc_rook[x] * i;
				if (out_of_bounds(row_init, col_init))
					continue;
				if (flag == 1 && col_init != move[1] - 'a')
					continue;
				if (flag == 2 && row_init != '8' - move[1])
					continue;
				if (board[row_init][col_init] == rook)
				{
					return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) + (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
				}
				if (board[row_init][col_init] != 0)
				{
					break;
				}
			}
		}
		return -1;
	}
	else if (move[0] == 'N')
	{
		int row_final, col_final;
		int flag = 0; // 0 if this is a regular move, 1 if it is like Nab1, 2 if it is like N1c2
		if (move[1] == 'x')
		{
			row_final = '8' - move[3];
			col_final = move[2] - 'a';
		}
		else if (move[2] == 'x')
		{
			if (move[1] <= 'h' && move[1] >= 'a')
			{
				flag = 1;
			}
			else
			{
				flag = 2;
			}
			row_final = '8' - move[4];
			col_final = move[3] - 'a';
		}
		else
		{
			if (move.size() == 3)
			{
				row_final = '8' - move[2];
				col_final = move[1] - 'a';
			}
			else
			{
				if (move[1] <= 'h' && move[1] >= 'a')
				{
					flag = 1;
				}
				else
				{
					flag = 2;
				}
				row_final = '8' - move[3];
				col_final = move[2] - 'a';
			}
		}
		int knight = BN;
		if (to_move)
			knight = WN;
		for (int x = 0; x < 8; x++)
		{
			int row_init = row_final + dr_knight[x], col_init = col_final + dc_knight[x];
			if (out_of_bounds(row_init, col_init))
				continue;
			if (flag == 1 && col_init != move[1] - 'a')
				continue;
			if (flag == 2 && row_init != '8' - move[1])
				continue;
			if (board[row_init][col_init] == knight)
			{
				return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) + (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
			}
		}
		return -1;
	}
	else if (move[0] <= 'h' && move[0] >= 'a')
	{
		if (move[move.size() - 2] == '=')
		{
			int row_final, col_final, row_init, col_init;
			if (to_move)
			{
				row_final = 0;
				row_init = 1;
			}
			else
			{
				row_final = 7;
				row_init = 6;
			}
			if (move[1] == 'x')
			{
				col_init = move[0] - 'a';
				if (move[2] < 'a' || move[2] > 'h')
					return -1;
				col_final = move[2] - 'a';
			}
			else
			{
				col_init = move[0] - 'a';
				col_final = move[0] - 'a';
			}
			int promote_to = piece_to_int(move[move.size() - 1]);
			if (promote_to < 2 || promote_to > 5)
				return -1;
			if (out_of_bounds(row_final, col_final) || out_of_bounds(row_init, col_init)) return -1;
			return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) +
				   (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15) + (1 << 19) + ((promote_to - 2) << 20);
		}
		else if (move[1] == 'x')
		{
			int row_init, row_final = '8' - move[3], col_init = move[0] - 'a', col_final = move[2] - 'a';
			bool en_passant = false;
			if (board[row_final][col_final] == 0)
			{
				en_passant = true;
			}
			if (to_move)
			{
				row_init = row_final + 1;
				if (board[row_init][col_init] != WP) return -1;
			}
			else
			{
				row_init = row_final - 1;
				if (board[row_init][col_init] != BP) return -1;
			}
			if (out_of_bounds(row_final, col_final) || out_of_bounds(row_init, col_init)) return -1;
			if (!en_passant)
			{
				return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) +
					   (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
			}
			else
			{
				if ((row_final << 3) + col_final != en_passant_target.top()) return -1;
				return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) +
					   (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15) + (1 << 18);
			}
		}
		else
		{
			int row_init, row_final = '8' - move[1], col_init = move[0] - 'a', col_final = move[0] - 'a';
			if (board[row_final][row_final] != 0) return -1;
			if (to_move)
			{
				if (row_final == 4 && board[row_final + 1][col_init] == 0)
				{
					row_init = row_final + 2;
				}
				else
				{
					row_init = row_final + 1;
				}
				if (board[row_init][col_init] != WP) return -1;
			}
			else
			{
				if (row_final == 3 && board[row_final - 1][col_init] == 0)
				{
					row_init = row_final - 2;
				}
				else
				{
					row_init = row_final - 1;
				}
				if (board[row_init][col_init] != BP) return -1;
			}
			return (row_init << 3) + col_init + (((row_final << 3) + col_final) << 6) +
				   (abs(board[row_init][col_init]) << 12) + (abs(board[row_final][col_final]) << 15);
		}
	}
	return -1;
}
