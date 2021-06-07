#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#include "types.h"

#define TABLE_SIZE 10000019 // prime number

extern bool tt_exists[TABLE_SIZE];
extern Depth tt_depths[TABLE_SIZE];
extern Value tt_evals[TABLE_SIZE];
extern Bitstring tt_hashes[TABLE_SIZE];

extern Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table();
void clear_table();
#endif // !TRANSPOS_H_INCLUDED
