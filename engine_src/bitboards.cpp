#include "bitboards.h"

Bitboard white_pawn_bb, black_pawn_bb;

const Bitboard FILE_A = 0x8080808080808080,
               FILE_H = 0x0101010101010101;

Bitboard shift(Bitboard b, Direction d) {
    if (d == UP) {
        return b << 8;
    }
    if (d == DOWN) {
        return b >> 8;
    }
    if (d == RIGHT) {
        
    }
}