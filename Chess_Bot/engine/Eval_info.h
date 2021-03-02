#ifndef EVAL_INFO_H_INCLUDED
#define EVAL_INFO_H_INCLUDED
#include <vector>
#include <map>
#include <cassert>

typedef std::pair<int, int> pii;

extern int QVAL;
extern int RVAL;
extern int BVAL;
extern int NVAL;
extern int PVAL;

extern int devel_coeff, center_coeff, ksafety_coeff, castle_bonus, castle_right_bonus, pass_pawn_coeff,
    dpawn_coeff, activity_coeff, semi_open_bonus, open_bonus, bishop_pair_bonus;

extern int default_cnts[13], cnts[13];

extern int white_devel, black_devel, white_center, black_center;

// counting the number of pawns in each row to compute doubled pawns
extern int white_pawn_counts[8], black_pawn_counts[8];

extern int doubled_white, doubled_black;
extern int whitepawn_row_sum, blackpawn_row_sum;

extern std::vector<pii> whitepawns, whiteknights, whitebishops, whiterooks, whitequeens, whitekings;
extern std::vector<pii> blackpawns, blackknights, blackbishops, blackrooks, blackqueens, blackkings;

inline void init_eval_info();

extern int king_safety[8][8], king_activity[8][8], knight_devel[8][8], bishop_devel[8][8], pawn_center[8][8], knight_center[8][8];
#endif // !EVAL_INFO_H_INCLUDED
