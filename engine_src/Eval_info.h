#ifndef EVAL_INFO_H_INCLUDED
#define EVAL_INFO_H_INCLUDED
#include <vector>
#include <map>
#include <cassert>

#include "types.h"
#include "psqt.h"

extern Score curr_psqt;

extern int castle_bonus, castle_right_bonus, dpawn_coeff, semi_open_bonus, open_bonus, bishop_pair_bonus, seventh_rooks[2];

extern int cnts[13];

// counting the number of pawns in each row to compute doubled pawns
extern int white_pawn_counts[8], black_pawn_counts[8];

extern int doubled_white, doubled_black;

extern std::vector<pii> piecelists[13];

extern std::vector <int> nnue_input;
#endif // !EVAL_INFO_H_INCLUDED
