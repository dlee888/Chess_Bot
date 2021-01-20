#include "State.h"

void state::make_move(int move)
{
	if (move == -1)
	{
		//throw std::exception("Trying to make an illegal move");
		return;
	}

	int row_init = (move >> 3) & 7, row_final = (move >> 9) & 7, col_init = move & 7, col_final = (move >> 6) & 7;
	int piece = (move >> 12) & 7, piece_captured = (move >> 15) & 7;

	if (piece_captured != 0)
	{
		fifty_move = 0;
	}

	int color = -1;
	if (to_move)
		color = 1;

	bool wk_pushed = false, bk_pushed = false, wq_pushed = false, bq_pushed = false;

	en_passant_target.push(-1);

	if (((move >> 18) & 3) == 3)
	{
		if (to_move)
		{
			white_castled = true;
			if ((move >> 20) == 1)
			{ //kingside castle
				replace_board(7, 6, WK);
				replace_board(7, 5, WR);
				replace_board(7, 7, 0);
				replace_board(7, 4, 0);
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == 7 && whiterooks[i].second == 7)
					{
						whiterooks[i].second = 5;
						break;
					}
				}
				whitekings[0].second = 6;
				wk_rights.push(false);
				wk_pushed = true;
			}
			else
			{
				replace_board(7, 3, WR);
				replace_board(7, 2, WK);
				replace_board(7, 0, 0);
				replace_board(7, 4, 0);
				whitekings[0].second = 2;
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == 7 && whiterooks[i].second == 0)
					{
						whiterooks[i].second = 3;
						break;
					}
				}
				wq_rights.push(false);
				wq_pushed = true;
			}
		}
		else
		{
			black_castled = true;
			if ((move >> 20) == 1)
			{ //kingside castle
				replace_board(0, 6, BK);
				replace_board(0, 5, BR);
				replace_board(0, 7, 0);
				replace_board(0, 4, 0);
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == 0 && blackrooks[i].second == 7)
					{
						blackrooks[i].second = 5;
						break;
					}
				}
				blackkings[0].second = 6;
				bk_rights.push(false);
				bk_pushed = true;
			}
			else
			{
				replace_board(0, 3, BR);
				replace_board(0, 2, BK);
				replace_board(0, 0, 0);
				replace_board(0, 4, 0);
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == 0 && blackrooks[i].second == 0)
					{
						blackrooks[i].second = 3;
						break;
					}
				}
				blackkings[0].second = 2;
				bq_rights.push(false);
				bq_pushed = true;
			}
		}
	}
	else if (((move >> 18) & 3) == 2)
	{
		fifty_move = 0;
		int promote_to = (move >> 20) + 2;
		cnts[color * WP + 6]--;
		cnts[promote_to * color + 6]++;
		cnts[piece_captured * color * -1 + 6]--;
		cnts[6]++;

		replace_board(row_final, col_final, promote_to * color);
		replace_board(row_init, col_init, 0);

		if (to_move)
		{
			whitepawn_row_sum -= 6;
			if (white_pawn_counts[col_init] >= 2)
				doubled_white -= white_pawn_counts[col_init];
			white_pawn_counts[col_init]--;
			if (white_pawn_counts[col_init] >= 2)
				doubled_white += white_pawn_counts[col_init];
			for (int i = 0; i < whitepawns.size(); i++)
			{
				if (whitepawns[i].first == row_init && whitepawns[i].second == col_init)
				{
					whitepawns.erase(whitepawns.begin() + i);
					break;
				}
			}
		}
		else
		{
			blackpawn_row_sum -= 6;
			if (black_pawn_counts[col_init] >= 2)
				doubled_black -= black_pawn_counts[col_init];
			black_pawn_counts[col_init]--;
			if (black_pawn_counts[col_init] >= 2)
				doubled_black += black_pawn_counts[col_init];
			for (int i = 0; i < blackpawns.size(); i++)
			{
				if (blackpawns[i].first == row_init && blackpawns[i].second == col_init)
				{
					blackpawns.erase(blackpawns.begin() + i);
					break;
				}
			}
		}

		if (promote_to == WN)
		{
			if (to_move)
			{
				whiteknights.push_back(std::make_pair(row_final, col_final));
				white_devel += knight_devel[row_final][col_final];
				white_center += knight_center[row_final][col_final];
			}
			else
			{
				blackknights.push_back(std::make_pair(row_final, col_final));
				black_devel += knight_devel[7 - row_final][col_final];
				black_center += knight_center[7 - row_final][col_final];
			}
		}
		if (promote_to == WB)
		{
			if (to_move)
			{
				whitebishops.push_back(std::make_pair(row_final, col_final));
				white_devel += bishop_devel[row_final][col_final];
			}
			else
			{
				blackbishops.push_back(std::make_pair(row_final, col_final));
				black_devel += bishop_devel[7 - row_final][col_final];
			}
		}
		if (promote_to == WR)
		{
			if (to_move)
			{
				whiterooks.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				blackrooks.push_back(std::make_pair(row_final, col_final));
			}
		}
		if (promote_to == WQ)
		{
			if (to_move)
			{
				whitequeens.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				blackqueens.push_back(std::make_pair(row_final, col_final));
			}
		}

		if (piece_captured == WN)
		{
			if (to_move)
			{
				black_devel -= knight_devel[7 - row_final][col_final];
				black_center -= knight_center[7 - row_final][col_final];
				for (int i = 0; i < blackknights.size(); i++)
				{
					if (blackknights[i].first == row_final && blackknights[i].second == col_final)
					{
						blackknights.erase(blackknights.begin() + i);
						break;
					}
				}
			}
			else
			{
				white_devel -= knight_devel[row_final][col_final];
				white_center -= knight_center[row_final][col_final];
				for (int i = 0; i < whiteknights.size(); i++)
				{
					if (whiteknights[i].first == row_final && whiteknights[i].second == col_final)
					{
						whiteknights.erase(whiteknights.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WB)
		{
			if (to_move)
			{
				black_devel -= bishop_devel[7 - row_final][col_final];
				for (int i = 0; i < blackbishops.size(); i++)
				{
					if (blackbishops[i].first == row_final && blackbishops[i].second == col_final)
					{
						blackbishops.erase(blackbishops.begin() + i);
						break;
					}
				}
			}
			else
			{
				white_devel -= bishop_devel[row_final][col_final];
				for (int i = 0; i < whitebishops.size(); i++)
				{
					if (whitebishops[i].first == row_final && whitebishops[i].second == col_final)
					{
						whitebishops.erase(whitebishops.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WR)
		{
			if (to_move)
			{
				if (row_final == 0 && col_final == 0)
				{
					bq_rights.push(false);
					bq_pushed = true;
				}
				if (row_final == 0 && col_final == 7)
				{
					bk_rights.push(false);
					bk_pushed = true;
				}
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == row_final && blackrooks[i].second == col_final)
					{
						blackrooks.erase(blackrooks.begin() + i);
						break;
					}
				}
			}
			else
			{
				if (row_final == 7 && col_final == 0)
				{
					wq_rights.push(false);
					wq_pushed = true;
				}
				if (row_final == 7 && col_final == 7)
				{
					wk_rights.push(false);
					wk_pushed = true;
				}
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == row_final && whiterooks[i].second == col_final)
					{
						whiterooks.erase(whiterooks.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WQ)
		{
			if (to_move)
			{
				for (int i = 0; i < blackqueens.size(); i++)
				{
					if (blackqueens[i].first == row_final && blackqueens[i].second == col_final)
					{
						blackqueens.erase(blackqueens.begin() + i);
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < whitequeens.size(); i++)
				{
					if (whitequeens[i].first == row_final && whitequeens[i].second == col_final)
					{
						whitequeens.erase(whitequeens.begin() + i);
						break;
					}
				}
			}
		}
	}
	else if (((move >> 18) & 3) == 1)
	{
		if (to_move)
		{
			replace_board(row_final, col_final, WP);
		}
	}
	else
	{
		//making the move
		replace_board(row_init, col_init, 0);
		replace_board(row_final, col_final, piece * color);

		//updating eval info
		cnts[piece_captured * color * -1 + 6]--;
		cnts[6]++;

		if (piece == WN)
		{
			if (to_move)
			{
				white_center += knight_center[row_final][col_final] - knight_center[row_init][col_init];
				white_devel += knight_devel[row_final][col_final] - knight_devel[row_init][col_init];
				for (int i = 0; i < whiteknights.size(); i++)
				{
					if (whiteknights[i].first == row_init && whiteknights[i].second == col_init)
					{
						whiteknights[i].first = row_final;
						whiteknights[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				black_center += knight_center[7 - row_final][col_final] - knight_center[7 - row_init][col_init];
				black_devel += knight_devel[7 - row_final][col_final] - knight_devel[7 - row_init][col_init];
				for (int i = 0; i < blackknights.size(); i++)
				{
					if (blackknights[i].first == row_init && blackknights[i].second == col_init)
					{
						blackknights[i].first = row_final;
						blackknights[i].second = col_final;
						break;
					}
				}
			}
		}
		else if (piece == WP)
		{
			fifty_move = 0;
			if (to_move)
			{
				white_center += pawn_center[row_final][col_final] - pawn_center[row_init][col_init];
				whitepawn_row_sum -= row_final - row_init;
				if (white_pawn_counts[col_final] >= 2)
					doubled_white -= white_pawn_counts[col_final];
				if (white_pawn_counts[col_init] >= 2)
					doubled_white -= white_pawn_counts[col_init];
				white_pawn_counts[col_final]++;
				white_pawn_counts[col_init]--;
				if (col_init - col_final == 2)
				{
					en_passant_target.pop();
					en_passant_target.push(row_final << 3 + col_init - 1);
				}
				if (white_pawn_counts[col_final] >= 2)
					doubled_white += white_pawn_counts[col_final];
				if (white_pawn_counts[col_init] >= 2)
					doubled_white += white_pawn_counts[col_init];
				for (int i = 0; i < whitepawns.size(); i++)
				{
					if (whitepawns[i].first == row_init && whitepawns[i].second == col_init)
					{
						whitepawns[i].first = row_final;
						whitepawns[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				black_center += pawn_center[7 - row_final][col_final] - pawn_center[7 - row_init][col_init];
				blackpawn_row_sum += row_final - row_init;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black -= black_pawn_counts[col_final];
				if (black_pawn_counts[col_init] >= 2)
					doubled_black -= black_pawn_counts[col_init];
				black_pawn_counts[col_final]++;
				black_pawn_counts[col_init]--;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black += black_pawn_counts[col_final];
				if (black_pawn_counts[col_init] >= 2)
					doubled_black += black_pawn_counts[col_init];
				if (col_final - col_init == 2)
				{
					en_passant_target.pop();
					en_passant_target.push(row_final << 3 + col_init + 1);
				}
				for (int i = 0; i < blackpawns.size(); i++)
				{
					if (blackpawns[i].first == row_init && blackpawns[i].second == col_init)
					{
						blackpawns[i].first = row_final;
						blackpawns[i].second = col_final;
						break;
					}
				}
			}
		}
		else if (piece == WB)
		{
			if (to_move)
			{
				white_devel += bishop_devel[row_final][col_final] - bishop_devel[row_init][col_init];
				for (int i = 0; i < whitebishops.size(); i++)
				{
					if (whitebishops[i].first == row_init && whitebishops[i].second == col_init)
					{
						whitebishops[i].first = row_final;
						whitebishops[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				black_devel += bishop_devel[7 - row_final][col_final] - bishop_devel[7 - row_init][col_init];
				for (int i = 0; i < blackbishops.size(); i++)
				{
					if (blackbishops[i].first == row_init && blackbishops[i].second == col_init)
					{
						blackbishops[i].first = row_final;
						blackbishops[i].second = col_final;
						break;
					}
				}
			}
		}
		else if (piece == WR)
		{
			if (to_move)
			{
				if (row_init == 7 && col_init == 0)
				{
					wq_rights.push(false);
					wq_pushed = true;
				}
				if (row_init == 7 && col_init == 7)
				{
					wk_rights.push(false);
					wk_pushed = true;
				}
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == row_init && whiterooks[i].second == col_init)
					{
						whiterooks[i].first = row_final;
						whiterooks[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				if (row_init == 0 && col_init == 0)
				{
					bq_rights.push(false);
					bq_pushed = true;
				}
				if (row_init == 0 && col_init == 7)
				{
					bk_rights.push(false);
					bk_pushed = true;
				}
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == row_init && blackrooks[i].second == col_init)
					{
						blackrooks[i].first = row_final;
						blackrooks[i].second = col_final;
						break;
					}
				}
			}
		}
		else if (piece == WQ)
		{
			if (to_move)
			{
				for (int i = 0; i < whitequeens.size(); i++)
				{
					if (whitequeens[i].first == row_init && whitequeens[i].second == col_init)
					{
						whitequeens[i].first = row_final;
						whitequeens[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < blackqueens.size(); i++)
				{
					if (blackqueens[i].first == row_init && blackqueens[i].second == col_init)
					{
						blackqueens[i].first = row_final;
						blackqueens[i].second = col_final;
						break;
					}
				}
			}
		}
		else if (piece == WK)
		{
			if (to_move)
			{
				wq_rights.push(false);
				wq_pushed = true;
				wk_rights.push(false);
				wk_pushed = true;
				for (int i = 0; i < whitekings.size(); i++)
				{
					if (whitekings[i].first == row_init && whitekings[i].second == col_init)
					{
						whitekings[i].first = row_final;
						whitekings[i].second = col_final;
						break;
					}
				}
			}
			else
			{
				bq_rights.push(false);
				bq_pushed = true;
				bk_rights.push(false);
				bk_pushed = true;
				for (int i = 0; i < blackkings.size(); i++)
				{
					if (blackkings[i].first == row_init && blackkings[i].second == col_init)
					{
						blackkings[i].first = row_final;
						blackkings[i].second = col_final;
						break;
					}
				}
			}
		}

		if (piece_captured == WP)
		{
			if (to_move)
			{
				blackpawn_row_sum -= row_final;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black -= black_pawn_counts[col_final];
				black_pawn_counts[col_final]--;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black += black_pawn_counts[col_final];
				black_center -= pawn_center[7 - row_final][col_final];
				for (int i = 0; i < blackpawns.size(); i++)
				{
					if (blackpawns[i].first == row_final && blackpawns[i].second == col_final)
					{
						blackpawns.erase(blackpawns.begin() + i);
						break;
					}
				}
			}
			else
			{
				whitepawn_row_sum -= 7 - row_final;
				if (white_pawn_counts[col_final] >= 2)
					doubled_white -= white_pawn_counts[col_final];
				white_pawn_counts[col_final]--;
				if (white_pawn_counts[col_final] >= 2)
					doubled_white += white_pawn_counts[col_final];
				white_center -= pawn_center[row_final][col_final];
				for (int i = 0; i < whitepawns.size(); i++)
				{
					if (whitepawns[i].first == row_final && whitepawns[i].second == col_final)
					{
						whitepawns.erase(whitepawns.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WN)
		{
			if (to_move)
			{
				black_devel -= knight_devel[7 - row_final][col_final];
				black_center -= knight_center[7 - row_final][col_final];
				for (int i = 0; i < blackknights.size(); i++)
				{
					if (blackknights[i].first == row_final && blackknights[i].second == col_final)
					{
						blackknights.erase(blackknights.begin() + i);
						break;
					}
				}
			}
			else
			{
				white_devel -= knight_devel[row_final][col_final];
				white_center -= knight_center[row_final][col_final];
				for (int i = 0; i < whiteknights.size(); i++)
				{
					if (whiteknights[i].first == row_final && whiteknights[i].second == col_final)
					{
						whiteknights.erase(whiteknights.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WB)
		{
			if (to_move)
			{
				black_devel -= bishop_devel[7 - row_final][col_final];
				for (int i = 0; i < blackbishops.size(); i++)
				{
					if (blackbishops[i].first == row_final && blackbishops[i].second == col_final)
					{
						blackbishops.erase(blackbishops.begin() + i);
						break;
					}
				}
			}
			else
			{
				white_devel -= bishop_devel[row_final][col_final];
				for (int i = 0; i < whitebishops.size(); i++)
				{
					if (whitebishops[i].first == row_final && whitebishops[i].second == col_final)
					{
						whitebishops.erase(whitebishops.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WR)
		{
			if (to_move)
			{
				if (row_final == 0 && col_final == 0)
				{
					bq_rights.push(false);
					bq_pushed = true;
				}
				if (row_final == 0 && col_final == 7)
				{
					bk_rights.push(false);
					bk_pushed = true;
				}
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == row_final && blackrooks[i].second == col_final)
					{
						blackrooks.erase(blackrooks.begin() + i);
						break;
					}
				}
			}
			else
			{
				if (row_final == 7 && col_final == 0)
				{
					wq_rights.push(false);
					wq_pushed = true;
				}
				if (row_final == 7 && col_final == 7)
				{
					wk_rights.push(false);
					wk_pushed = true;
				}
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == row_final && whiterooks[i].second == col_final)
					{
						whiterooks.erase(whiterooks.begin() + i);
						break;
					}
				}
			}
		}
		else if (piece_captured == WQ)
		{
			if (to_move)
			{
				for (int i = 0; i < blackqueens.size(); i++)
				{
					if (blackqueens[i].first == row_final && blackqueens[i].second == col_final)
					{
						blackqueens.erase(blackqueens.begin() + i);
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < whitequeens.size(); i++)
				{
					if (whitequeens[i].first == row_final && whitequeens[i].second == col_final)
					{
						whitequeens.erase(whitequeens.begin() + i);
						break;
					}
				}
			}
		}
	}
	if (!wk_pushed)
		wk_rights.push(wk_rights.top());
	if (!wq_pushed)
		wq_rights.push(wq_rights.top());
	if (!bk_pushed)
		bk_rights.push(bk_rights.top());
	if (!bq_pushed)
		bq_rights.push(bq_rights.top());
	to_move = !to_move;
}