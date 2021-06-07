#include "Evaluate.h"

Value eval(state& s, bool trace)
{
	Value score = VALUE_ZERO;

	if ((10 * (cnts[BQ + 6] + cnts[WQ + 6]) + 5 * (cnts[BR + 6] + cnts[WR + 6]) +
		3 * (cnts[BB + 6] + cnts[WB + 6] + cnts[BN + 6] + cnts[WN + 6])) > 25)
	{
		if (trace) printf("Middle game:\n");
		// Development
		score += devel_coeff * (white_devel - black_devel);
		if (trace) printf("Development: %d\n", devel_coeff * (white_devel - black_devel));

		// Center control
		score += center_coeff * (white_center - black_center);
		if (trace) printf("Center control: %d\n", center_coeff * (white_center - black_center));

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
		if (trace) printf("King safety: %d\n", ksafety);
		
		// open files and rooks on the seventh
		int files = 0, wrooks = 0, brooks = 0;
		for (pii& p : whiterooks) {
			if (white_pawn_counts[p.second] == 0) {
				if (black_pawn_counts[p.second] == 0) {
					files += open_bonus;
				}
				else {
					files += semi_open_bonus;
				}
			}
			if (p.first == 1) wrooks++;
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
			if (p.first == 6) brooks++;
		}
		score += files;
		if (trace) printf("Open files: %d\n", files);

		int rook7 = seventh_rooks[wrooks] - seventh_rooks[brooks];
		score += rook7;
		if (trace) printf("Rooks on the seventh: %d\n", rook7);

		//material
		int mat = PawnValueMg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueMg * (cnts[WN + 6] - cnts[BN + 6]) + 
				BishopValueMg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueMg * (cnts[WR + 6] - cnts[BR + 6]) + 
				QueenValueMg * (cnts[WQ + 6] - cnts[BQ + 6]);
		score += mat;
		if (trace) printf("Material: %d\n", mat);
	}
	else
	{
		if (trace) printf("End game:\n");

		// Pushed pawns
		score += pass_pawn_coeff * (whitepawn_row_sum - blackpawn_row_sum);
		if (trace) printf("Pushed pawns: %d\n", pass_pawn_coeff * (whitepawn_row_sum - blackpawn_row_sum));

		// King activity
		int kactivity = 0;
		kactivity += (king_activity[whitekings[0].first][whitekings[0].second] - king_activity[7 - blackkings[0].first][blackkings[0].second]);
		score += activity_coeff * kactivity;
		if (trace) printf("King activity: %d\n", kactivity);
			
		//material
		int mat = PawnValueEg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueEg * (cnts[WN + 6] - cnts[BN + 6]) + 
				BishopValueEg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueEg * (cnts[WR + 6] - cnts[BR + 6]) + 
				QueenValueEg * (cnts[WQ + 6] - cnts[BQ + 6]);
		score += mat;
		if (trace) printf("Material: %d\n", mat);
	}

	//doubled pawns
	score -= dpawn_coeff * (doubled_white - doubled_black);
	if (trace) printf("Doubled pawns: %d\n", -dpawn_coeff * (doubled_white - doubled_black));

	// Bishop pair
	int bpair = 0;
	if (whitebishops.size() >= 2) {
		bpair += bishop_pair_bonus;
	}
	if (blackbishops.size() >= 2) {
		bpair -= bishop_pair_bonus;
	}
	score += bpair;
	if (trace) printf("Bishop pair: %d\n", bpair);
	
	if (!s.to_move) score *= -1;

	return score;
}