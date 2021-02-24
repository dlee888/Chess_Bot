#ifndef EVALUATE_H_INCLUDED
#define EVALUATE_H_INCLUDED

#include "State.h"

int eval(state &s)
{
	if (s.adjucation())
		return 0;
	int score = 0;
	if ((9 * (cnts[BQ + 6] + cnts[WQ + 6]) + 5 * (cnts[BR + 6] + cnts[WR + 6]) +
		 3 * (cnts[BB + 6] + cnts[WB + 6] + cnts[BN + 6] + cnts[WN + 6])) > 30)
	{
		//This is opening and middlegame
		RVAL = 500;
		BVAL = 320;
		NVAL = 310;
		PVAL = 100;

		//development
		score += devel_coeff * (white_devel - black_devel);
		// printf("Development: %d\n", devel_coeff * (white_devel - black_devel));

		//center control
		score += center_coeff * (white_center - black_center);
		// printf("Center control: %d\n", center_coeff * (white_center - black_center));

		//King safety
		int ksafety = 0;
		ksafety += (king_safety[whitekings[0].first][whitekings[0].second] - king_safety[7 - blackkings[0].first][blackkings[0].second]);
		if (s.white_castled)
			ksafety += castle_bonus;
		if (s.black_castled)
			ksafety -= castle_bonus;
		score += ksafety_coeff * ksafety;
		// printf("King safety: %d\n", ksafety_coeff * ksafety);
	}
	else
	{
		//This is for endgames
		RVAL = 550;
		BVAL = 350;
		NVAL = 270;
		PVAL = 130;

		//pushed pawns
		score += pass_pawn_coeff * (whitepawn_row_sum - blackpawn_row_sum);

		//king activity
		int kactivity = 0;
		kactivity += (king_activity[whitekings[0].first][whitekings[0].second] - king_activity[7 - blackkings[0].first][blackkings[0].second]);
		score += activity_coeff * kactivity;
	}
	//material
	int mat = 100000 * (cnts[WK + 6] - cnts[BK + 6]) + QVAL * (cnts[WQ + 6] - cnts[BQ + 6]) + RVAL * (cnts[WR + 6] - cnts[BR + 6]) + BVAL * (cnts[WB + 6] - cnts[BB + 6]) + NVAL * (cnts[WN + 6] - cnts[BN + 6]) + PVAL * (cnts[WP + 6] - cnts[BP + 6]);
	score += mat;
	// printf("Material: %d\n", mat);

	//doubled pawns
	score -= dpawn_coeff * (doubled_white - doubled_black);
	// printf("Doubled pawns: %d\n", dpawn_coeff * (doubled_white - doubled_black));
	return score;
}
#endif // !EVALUATE_H_INCLUDED
