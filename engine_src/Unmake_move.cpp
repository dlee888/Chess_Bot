#include "State.h"

void state::unmake_move(int move)
{
	if (move == -1)
	{
		//throw std::exception("Trying to unmake an illegal move");
		return;
	}

	int row_init = (move >> 3) & 7, row_final = (move >> 9) & 7, col_init = move & 7, col_final = (move >> 6) & 7;
	int piece = (move >> 12) & 7, piece_captured = (move >> 15) & 7;

	int color = 1;
	if (to_move)
		color = -1;

	wk_rights.pop();
	bk_rights.pop();
	wq_rights.pop();
	bq_rights.pop();
	en_passant_target.pop();

	if (!to_move) full_move--;

	if (((move >> 18) & 3) == 3)
	{
		if ((move >> 20) == 1)
		{
			if (!to_move)
			{
				white_castled = false;
				replace_board(7, 6, 0);
				replace_board(7, 5, 0);
				replace_board(7, 4, WK);
				replace_board(7, 7, WR);
				whitekings[0].second = 4;
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == 7 && whiterooks[i].second == 5)
					{
						whiterooks[i].second = 7;
						break;
					}
				}
			}
			else
			{
				black_castled = false;
				replace_board(0, 6, 0);
				replace_board(0, 5, 0);
				replace_board(0, 4, BK);
				replace_board(0, 7, BR);
				blackkings[0].second = 4;
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == 0 && blackrooks[i].second == 5)
					{
						blackrooks[i].second = 7;
						break;
					}
				}
			}
		}
		else
		{
			if (!to_move)
			{
				white_castled = false;
				replace_board(7, 2, 0);
				replace_board(7, 3, 0);
				replace_board(7, 4, WK);
				replace_board(7, 0, WR);
				whitekings[0].second = 4;
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == 7 && whiterooks[i].second == 3)
					{
						whiterooks[i].second = 0;
						break;
					}
				}
			}
			else
			{
				black_castled = false;
				replace_board(0, 2, 0);
				replace_board(0, 3, 0);
				replace_board(0, 4, BK);
				replace_board(0, 0, BR);
				blackkings[0].second = 4;
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == 0 && blackrooks[i].second == 3)
					{
						blackrooks[i].second = 0;
						break;
					}
				}
			}
		}
	}
	else if (((move >> 18) & 3) == 2)
	{
		int promote_to = (move >> 20) + 2;

		cnts[color * WP + 6]++;
		cnts[color * promote_to + 6]--;
		cnts[color * -1 * piece_captured + 6]++;
		cnts[6]--;

		replace_board(row_final, col_final, piece_captured * color * -1);
		replace_board(row_init, col_init, piece * color);

		if (!to_move)
		{
			whitepawn_row_sum += 6;
			if (white_pawn_counts[col_init] >= 2)
				doubled_white -= white_pawn_counts[col_init];
			white_pawn_counts[col_init]++;
			if (white_pawn_counts[col_init] >= 2)
				doubled_white += white_pawn_counts[col_init];
			whitepawns.push_back(std::make_pair(row_init, col_init));
		}
		else
		{
			blackpawn_row_sum += 6;
			if (black_pawn_counts[col_init] >= 2)
				doubled_black -= black_pawn_counts[col_init];
			black_pawn_counts[col_init]++;
			if (black_pawn_counts[col_init] >= 2)
				doubled_black += black_pawn_counts[col_init];
			blackpawns.push_back(std::make_pair(row_init, col_init));
		}

		if (promote_to == WN)
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
		else if (promote_to == WB)
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
		if (promote_to == WR)
		{
			if (to_move)
			{
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
		if (promote_to == WQ)
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

		if (piece_captured == WN)
		{
			if (!to_move)
			{
				black_devel += knight_devel[7 - row_final][col_final];
				black_center += knight_center[7 - row_final][col_final];
				blackknights.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				white_devel += knight_devel[row_final][col_final];
				white_center += knight_center[row_final][col_final];
				whiteknights.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WB)
		{
			if (!to_move)
			{
				black_devel += bishop_devel[7 - row_final][col_final];
				blackbishops.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				white_devel += bishop_devel[row_final][col_final];
				whitebishops.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WR)
		{
			if (!to_move)
			{
				blackrooks.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				whiterooks.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WQ)
		{
			if (!to_move)
			{
				blackqueens.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				whitequeens.push_back(std::make_pair(row_final, col_final));
			}
		}
	}
	else if (((move >> 18) & 3) == 1)
	{
		if (!to_move)
		{
			replace_board(row_final, col_final, 0);
			replace_board(row_init, col_init, WP);
			replace_board(row_final + 1, col_final, BP);

			fifty_move = 0;

			cnts[BP + 6]++;

			white_center -= pawn_center[row_final][col_final] - pawn_center[row_init][col_init];
			whitepawn_row_sum += row_final - row_init;

			if (white_pawn_counts[col_final] >= 2)
				doubled_white -= white_pawn_counts[col_final];
			if (white_pawn_counts[col_init] >= 2)
				doubled_white -= white_pawn_counts[col_init];
			white_pawn_counts[col_final]--;
			white_pawn_counts[col_init]++;
			if (white_pawn_counts[col_final] >= 2)
				doubled_white += white_pawn_counts[col_final];
			if (white_pawn_counts[col_init] >= 2)
				doubled_white += white_pawn_counts[col_init];

			for (int i = 0; i < whitepawns.size(); i++)
			{
				if (whitepawns[i].first == row_final && whitepawns[i].second == col_final)
				{
					whitepawns[i].first = row_init;
					whitepawns[i].second = col_init;
					break;
				}
			}

			blackpawn_row_sum += row_final + 1;
			black_center += pawn_center[6 - row_final][col_final];

			if (black_pawn_counts[col_final] >= 2)
				doubled_black -= black_pawn_counts[col_final];
			black_pawn_counts[col_final]++;
			if (black_pawn_counts[col_final] >= 2)
				doubled_black += black_pawn_counts[col_final];

			blackpawns.push_back({row_final + 1, col_final});
		}
		else
		{
			replace_board(row_final, col_final, 0);
			replace_board(row_init, col_init, BP);
			replace_board(row_final - 1, col_final, WP);

			fifty_move = 0;

			cnts[WP + 6]++;

			black_center -= pawn_center[7 - row_final][col_final] - pawn_center[7 - row_init][col_init];
			blackpawn_row_sum -= row_final - row_init;

			if (black_pawn_counts[col_final] >= 2)
				doubled_black -= black_pawn_counts[col_final];
			if (black_pawn_counts[col_init] >= 2)
				doubled_black -= black_pawn_counts[col_init];
			black_pawn_counts[col_final]--;
			black_pawn_counts[col_init]++;
			if (black_pawn_counts[col_final] >= 2)
				doubled_black += black_pawn_counts[col_final];
			if (black_pawn_counts[col_init] >= 2)
				doubled_black += black_pawn_counts[col_init];

			for (int i = 0; i < blackpawns.size(); i++)
			{
				if (blackpawns[i].first == row_final && blackpawns[i].second == col_final)
				{
					blackpawns[i].first = row_init;
					blackpawns[i].second = col_init;
					break;
				}
			}

			whitepawn_row_sum += 8 - row_final;
			white_center += pawn_center[row_final - 1][col_final];

			if (white_pawn_counts[col_final] >= 2)
				doubled_white -= white_pawn_counts[col_final];
			white_pawn_counts[col_final]++;
			if (white_pawn_counts[col_final] >= 2)
				doubled_white += white_pawn_counts[col_final];

			whitepawns.push_back({row_final - 1, col_final});
		}
	}
	else
	{
		//unmaking the move
		replace_board(row_init, col_init, piece * color);
		replace_board(row_final, col_final, piece_captured * color * -1);

		//updating eval info
		cnts[piece_captured * color * -1 + 6]++;
		cnts[6]--;

		if (piece == WP)
		{
			if (!to_move)
			{
				whitepawn_row_sum += row_final - row_init;
				white_center += pawn_center[row_init][col_init] - pawn_center[row_final][col_final];
				if (white_pawn_counts[col_init] >= 2)
					doubled_white -= white_pawn_counts[col_init];
				if (white_pawn_counts[col_final] >= 2)
					doubled_white -= white_pawn_counts[col_final];
				white_pawn_counts[col_init]++;
				white_pawn_counts[col_final]--;
				if (white_pawn_counts[col_init] >= 2)
					doubled_white += white_pawn_counts[col_init];
				if (white_pawn_counts[col_final] >= 2)
					doubled_white += white_pawn_counts[col_final];
				for (int i = 0; i < whitepawns.size(); i++)
				{
					if (whitepawns[i].first == row_final && whitepawns[i].second == col_final)
					{
						whitepawns[i].first = row_init;
						whitepawns[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				blackpawn_row_sum -= row_final - row_init;
				black_center += pawn_center[7 - row_init][col_init] - pawn_center[7 - row_final][col_final];
				if (black_pawn_counts[col_init] >= 2)
					doubled_black -= black_pawn_counts[col_init];
				if (black_pawn_counts[col_final] >= 2)
					doubled_black -= black_pawn_counts[col_final];
				black_pawn_counts[col_init]++;
				black_pawn_counts[col_final]--;
				if (black_pawn_counts[col_init] >= 2)
					doubled_black += black_pawn_counts[col_init];
				if (black_pawn_counts[col_final] >= 2)
					doubled_black += black_pawn_counts[col_final];
				for (int i = 0; i < blackpawns.size(); i++)
				{
					if (blackpawns[i].first == row_final && blackpawns[i].second == col_final)
					{
						blackpawns[i].first = row_init;
						blackpawns[i].second = col_init;
						break;
					}
				}
			}
		}
		else if (piece == WN)
		{
			if (!to_move)
			{
				white_center += knight_center[row_init][col_init] - knight_center[row_final][col_final];
				white_devel += knight_devel[row_init][col_init] - knight_devel[row_final][col_final];
				for (int i = 0; i < whiteknights.size(); i++)
				{
					if (whiteknights[i].first == row_final && whiteknights[i].second == col_final)
					{
						whiteknights[i].first = row_init;
						whiteknights[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				black_center += knight_center[7 - row_init][col_init] - knight_center[7 - row_final][col_final];
				black_devel += knight_devel[7 - row_init][col_init] - knight_devel[7 - row_final][col_final];
				for (int i = 0; i < blackknights.size(); i++)
				{
					if (blackknights[i].first == row_final && blackknights[i].second == col_final)
					{
						blackknights[i].first = row_init;
						blackknights[i].second = col_init;
						break;
					}
				}
			}
		}
		else if (piece == WB)
		{
			if (!to_move)
			{
				white_devel += bishop_devel[row_init][col_init] - bishop_devel[row_final][col_final];
				for (int i = 0; i < whitebishops.size(); i++)
				{
					if (whitebishops[i].first == row_final && whitebishops[i].second == col_final)
					{
						whitebishops[i].first = row_init;
						whitebishops[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				black_devel += bishop_devel[7 - row_init][col_init] - bishop_devel[7 - row_final][col_final];
				for (int i = 0; i < blackbishops.size(); i++)
				{
					if (blackbishops[i].first == row_final && blackbishops[i].second == col_final)
					{
						blackbishops[i].first = row_init;
						blackbishops[i].second = col_init;
						break;
					}
				}
			}
		}
		else if (piece == WR)
		{
			if (!to_move)
			{
				for (int i = 0; i < whiterooks.size(); i++)
				{
					if (whiterooks[i].first == row_final && whiterooks[i].second == col_final)
					{
						whiterooks[i].first = row_init;
						whiterooks[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < blackrooks.size(); i++)
				{
					if (blackrooks[i].first == row_final && blackrooks[i].second == col_final)
					{
						blackrooks[i].first = row_init;
						blackrooks[i].second = col_init;
						break;
					}
				}
			}
		}
		else if (piece == WQ)
		{
			if (!to_move)
			{
				for (int i = 0; i < whitequeens.size(); i++)
				{
					if (whitequeens[i].first == row_final && whitequeens[i].second == col_final)
					{
						whitequeens[i].first = row_init;
						whitequeens[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < blackqueens.size(); i++)
				{
					if (blackqueens[i].first == row_final && blackqueens[i].second == col_final)
					{
						blackqueens[i].first = row_init;
						blackqueens[i].second = col_init;
						break;
					}
				}
			}
		}
		else if (piece == WK)
		{
			if (!to_move)
			{
				for (int i = 0; i < whitekings.size(); i++)
				{
					if (whitekings[i].first == row_final && whitekings[i].second == col_final)
					{
						whitekings[i].first = row_init;
						whitekings[i].second = col_init;
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i < blackkings.size(); i++)
				{
					if (blackkings[i].first == row_final && blackkings[i].second == col_final)
					{
						blackkings[i].first = row_init;
						blackkings[i].second = col_init;
						break;
					}
				}
			}
		}

		if (piece_captured == WP)
		{
			if (!to_move)
			{
				blackpawn_row_sum += row_final;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black -= black_pawn_counts[col_final];
				black_pawn_counts[col_final]++;
				if (black_pawn_counts[col_final] >= 2)
					doubled_black += black_pawn_counts[col_final];
				black_center += pawn_center[7 - row_final][col_final];
				blackpawns.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				whitepawn_row_sum += 7 - row_final;
				if (white_pawn_counts[col_final] >= 2)
					doubled_white -= white_pawn_counts[col_final];
				white_pawn_counts[col_final]++;
				if (white_pawn_counts[col_final] >= 2)
					doubled_white += white_pawn_counts[col_final];
				white_center += pawn_center[row_final][col_final];
				whitepawns.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WN)
		{
			if (!to_move)
			{
				black_center += knight_center[7 - row_final][col_final];
				black_devel += knight_devel[7 - row_final][col_final];
				blackknights.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				white_center += knight_center[row_final][col_final];
				white_devel += knight_devel[row_final][col_final];
				whiteknights.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WB)
		{
			if (!to_move)
			{
				black_devel += bishop_devel[7 - row_final][col_final];
				blackbishops.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				white_devel += bishop_devel[row_final][col_final];
				whitebishops.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WR)
		{
			if (!to_move)
			{
				blackrooks.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				whiterooks.push_back(std::make_pair(row_final, col_final));
			}
		}
		else if (piece_captured == WQ)
		{
			if (!to_move)
			{
				blackqueens.push_back(std::make_pair(row_final, col_final));
			}
			else
			{
				whitequeens.push_back(std::make_pair(row_final, col_final));
			}
		}
	}
	to_move = !to_move;
}