#include "Evaluate.h"

Value eval(state& s)
{
	Value score = VALUE_ZERO;

	if ((9 * (cnts[BQ + 6] + cnts[WQ + 6]) + 5 * (cnts[BR + 6] + cnts[WR + 6]) +
		3 * (cnts[BB + 6] + cnts[WB + 6] + cnts[BN + 6] + cnts[WN + 6])) > 30)
	{
		// Development
		score += devel_coeff * (white_devel - black_devel);
		// printf("Development: %d\n", devel_coeff * (white_devel - black_devel));

		// Center control
		score += center_coeff * (white_center - black_center);
		// printf("Center control: %d\n", center_coeff * (white_center - black_center));

		// King safety
		int ksafety = 0;
		ksafety += ksafety_coeff * (king_safety[whitekings[0].first][whitekings[0].second] - king_safety[7 - blackkings[0].first][blackkings[0].second]);
		// Castled?
		if (s.white_castled)
			ksafety += castle_bonus;
		if (s.black_castled)
			ksafety -= castle_bonus;
		// Castling rights?
		if (s.wq_rights.top() || s.wk_rights.top()) {
			ksafety += castle_right_bonus;
		}
		if (s.bq_rights.top() || s.bk_rights.top()) {
			ksafety -= castle_right_bonus;
		}
		score += ksafety;
		// printf("King safety: %d\n", ksafety_coeff * ksafety);

		// open files
		int files = 0;
		for (pii& p : whiterooks) {
			if (white_pawn_counts[p.second] == 0) {
				if (black_pawn_counts[p.second] == 0) {
					files += open_bonus;
				}
				else {
					files += semi_open_bonus;
				}
			}
		}
		for (pii& p : blackrooks) {
			if (black_pawn_counts[p.second] == 0) {
				if (white_pawn_counts[p.second] == 0) {
					files -= open_bonus;
				}
				else {
					files -= semi_open_bonus;
				}
			}
		}
		score += files;
		
		//material
		int mat = PawnValueMg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueMg * (cnts[WN + 6] - cnts[BN + 6]) + 
				BishopValueMg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueMg * (cnts[WR + 6] - cnts[BR + 6]) + 
				QueenValueMg * (cnts[WQ + 6] - cnts[BQ + 6]);
		score += mat;
		// printf("Material: %d\n", mat);
	}
	else
	{
		// Pushed pawns
		score += pass_pawn_coeff * (whitepawn_row_sum - blackpawn_row_sum);

		// King activity
		int kactivity = 0;
		kactivity += (king_activity[whitekings[0].first][whitekings[0].second] - king_activity[7 - blackkings[0].first][blackkings[0].second]);
		score += activity_coeff * kactivity;
			
		//material
		int mat = PawnValueEg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueEg * (cnts[WN + 6] - cnts[BN + 6]) + 
				BishopValueEg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueEg * (cnts[WR + 6] - cnts[BR + 6]) + 
				QueenValueEg * (cnts[WQ + 6] - cnts[BQ + 6]);
		score += mat;
		// printf("Material: %d\n", mat);
	}

	//doubled pawns
	score -= dpawn_coeff * (doubled_white - doubled_black);
	// printf("Doubled pawns: %d\n", dpawn_coeff * (doubled_white - doubled_black));

	// Bishop pair
	if (whitebishops.size() >= 2) {
		score += bishop_pair_bonus;
	}
	if (blackbishops.size() >= 2) {
		score -= bishop_pair_bonus;
	}

	score += MATE * (cnts[WK + 6] - cnts[BK + 6]);
	
	if (!s.to_move) score *= -1;

	return score;
}