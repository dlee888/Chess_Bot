#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#define TABLE_SIZE 7500013 // prime number

typedef unsigned long long Bitstring;

typedef std::pair<int, int> pdi;

extern bool exists[TABLE_SIZE];
extern int depths[TABLE_SIZE];
extern int best_eval[TABLE_SIZE];

extern Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

 void init_table();
#endif // !TRANSPOS_H_INCLUDED
