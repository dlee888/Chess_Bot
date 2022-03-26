#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#include "types.h"

extern bool* tt_exists;
extern Depth* tt_depths;
extern Value* tt_evals;
extern Bitstring* tt_hashes;
extern int* tt_fullmove;

extern int table_size;

extern Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table(int);
void clear_table();

inline int get_key(Bitstring hash) { return hash % table_size; }
#endif // !TRANSPOS_H_INCLUDED
