#ifndef BITBOARDS_INCLUDED
#define BITBOARDS_INCLUDED
#include "types.h"

extern Bitboard white_pawn_bb, black_pawn_bb;

Bitboard shift(Bitboard b, Direction d);
#endif