#include "Eval_info.h"

Score curr_psqt;

int castle_bonus = 35, castle_right_bonus = 20, dpawn_coeff = 17, semi_open_bonus = 10, open_bonus = 16, bishop_pair_bonus = 43;

int cnts[13];

// counting the number of pawns in each row to compute doubled pawns
int white_pawn_counts[8], black_pawn_counts[8];

int doubled_white, doubled_black;

std::vector<pii> piecelists[13];

std::vector<int> nnue_input = std::vector<int>(384);