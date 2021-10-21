#include "Evaluate.h"

Value eval(state& s, bool trace, bool use_nnue) {
	if (use_nnue) {
		return run_nnue(s);
	}

	Value score = VALUE_ZERO;

	if ((10 * (cnts[BQ + 6] + cnts[WQ + 6]) + 5 * (cnts[BR + 6] + cnts[WR + 6]) + 3 * (cnts[BB + 6] + cnts[WB + 6] + cnts[BN + 6] + cnts[WN + 6])) >
		25) {
		if (trace)
			printf("Middle game:\n");

		// Castled?
		int ksafety = 0;
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
		if (trace)
			printf("King safety: %d\n", ksafety);

		// open files and rooks on the seventh
		int files = 0, wrooks = 0, brooks = 0;
		for (pii& p : piecelists[WR + 6]) {
			if (white_pawn_counts[p.second] == 0) {
				if (black_pawn_counts[p.second] == 0) {
					files += open_bonus;
				} else {
					files += semi_open_bonus;
				}
			}
			if (p.first == 1)
				wrooks++;
		}
		for (pii& p : piecelists[BR + 6]) {
			if (black_pawn_counts[p.second] == 0) {
				if (white_pawn_counts[p.second] == 0) {
					files -= open_bonus;
				} else {
					files -= semi_open_bonus;
				}
			}
			if (p.first == 6)
				brooks++;
		}
		score += files;
		if (trace)
			printf("Open files: %d\n", files);

		score += mg_value(curr_psqt);

		// material
		int mat = PawnValueMg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueMg * (cnts[WN + 6] - cnts[BN + 6]) +
				  BishopValueMg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueMg * (cnts[WR + 6] - cnts[BR + 6]) +
				  QueenValueMg * (cnts[WQ + 6] - cnts[BQ + 6]);
		score += mat;
		if (trace)
			printf("Material: %d\n", mat);
	} else {
		if (trace)
			printf("End game:\n");

		score += eg_value(curr_psqt);

		// material
		score += PawnValueEg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueEg * (cnts[WN + 6] - cnts[BN + 6]) +
				 BishopValueEg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueEg * (cnts[WR + 6] - cnts[BR + 6]) +
				 QueenValueEg * (cnts[WQ + 6] - cnts[BQ + 6]);
		if (trace)
			printf("Material: %d\n", PawnValueEg * (cnts[WP + 6] - cnts[BP + 6]) + KnightValueEg * (cnts[WN + 6] - cnts[BN + 6]) +
										 BishopValueEg * (cnts[WB + 6] - cnts[BB + 6]) + RookValueEg * (cnts[WR + 6] - cnts[BR + 6]) +
										 QueenValueEg * (cnts[WQ + 6] - cnts[BQ + 6]));
	}

	// doubled pawns
	score -= dpawn_coeff * (doubled_white - doubled_black);
	if (trace)
		printf("Doubled pawns: %d\n", -dpawn_coeff * (doubled_white - doubled_black));

	// Bishop pair
	int bpair = 0;
	if (piecelists[WB + 6].size() >= 2) {
		bpair += bishop_pair_bonus;
	}
	if (piecelists[BB + 6].size() >= 2) {
		bpair -= bishop_pair_bonus;
	}
	score += bpair;
	if (trace)
		printf("Bishop pair: %d\n", bpair);

	if (!s.to_move)
		score *= -1;

	return score;
}