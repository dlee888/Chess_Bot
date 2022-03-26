#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#include "types.h"

extern std::vector<bool> tt_exists;
extern std::vector<Depth> tt_depths;
extern std::vector<Value> tt_evals;
extern std::vector<Bitstring> tt_hashes;
extern std::vector<int> tt_fullmove;

extern int table_size;

extern Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table(int);
void clear_table();

inline int get_key(Bitstring hash) { return hash % table_size; }

void replace_tt(Depth, Value, Bitstring, int);
#endif // !TRANSPOS_H_INCLUDED
