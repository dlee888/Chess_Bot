#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#define TABLE_SIZE 5000011 // prime number close to 5000000

typedef std::pair<int, int> pdi;

extern bool exists[TABLE_SIZE];
// extern state positions[TABLE_SIZE];
extern int depths[TABLE_SIZE];
extern pdi best_moves[TABLE_SIZE];

extern unsigned long long rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table();
#endif // !TRANSPOS_H_INCLUDED
