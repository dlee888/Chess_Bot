#ifndef EVALUATE_H_INCLUDED
#define EVALUATE_H_INCLUDED

#include "State.h"

double eval(state s)
{
	if (s.adjucation())
	{
		return 0;
	}
	double score = 0;
	if ((((double)cnts[BQ + 6] + cnts[WQ + 6]) * 9.3 + 5 * ((double)cnts[BR + 6] + cnts[WR + 6]) +
		 3.14 * ((double)cnts[BB + 6] + cnts[WB + 6]) + 3.02 * ((double)cnts[BN + 6] + cnts[WN + 6])) > 30.0)
	{
		//This is opening and middlegame
		RVAL = 5.0;
		BVAL = 3.2;
		NVAL = 3.1;
		PVAL = 1.0;

		//development
		score += devel_coeff * (white_devel - black_devel);

		//center control
		score += center_coeff * (white_center - black_center);

		//King safety
		double ksafety = 0;
		ksafety += ((double)king_safety[whitekings[0].first][whitekings[0].second] - king_safety[7 - blackkings[0].first][blackkings[0].second]);
		if (s.white_castled)
		{
			ksafety += castle_bonus;
		}
		if (s.black_castled)
		{
			ksafety -= castle_bonus;
		}
		score += ksafety_coeff * ksafety;
	}
	else
	{
		//This is for endgames
		RVAL = 5.5;
		BVAL = 3.5;
		NVAL = 2.7;
		PVAL = 1.3;

		//pushed pawns
		score += pass_pawn_coeff * ((double)whitepawn_row_sum - blackpawn_row_sum);

		//king activity
		double kactivity = 0;
		kactivity += ((double)king_activity[whitekings[0].first][whitekings[0].second] - king_activity[7 - blackkings[0].first][blackkings[0].second]);
		score += activity_coeff * kactivity;
	}
	//material
	double mat = KVAL * ((double)cnts[WK + 6] - cnts[BK + 6]) + QVAL * ((double)cnts[WQ + 6] - cnts[BQ + 6]) + RVAL * ((double)cnts[WR + 6] - cnts[BR + 6]) + BVAL * ((double)cnts[WB + 6] - cnts[BB + 6]) + NVAL * ((double)cnts[WN + 6] - cnts[BN + 6]) + ((double)cnts[WP + 6] - cnts[BP + 6]);
	score += mat;

	//doubled pawns
	score -= dpawn_coeff * ((double)doubled_white - doubled_black);
	for(int i = 0; i < 8; i++)
		for(int j = 0; j < 8; j++)
			score += attacking_coeff*s.board[i][j]*(s.attacking(i, j, s.board[i][j] < 0)-s.attacking(i, j, s.board[i][j] >= 0));
	return score;
}
#endif // !EVALUATE_H_INCLUDED
