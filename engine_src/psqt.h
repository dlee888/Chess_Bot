#ifndef PSQT_INCLUDED
#define PSQT_INCLUDED
#include "types.h"

extern Score piece_bonus[][8][4];
extern Score pawn_bonus[8][8];

Score get_psqt(int, int, int);
#endif