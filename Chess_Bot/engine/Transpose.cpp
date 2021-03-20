#include <cstring>
#include <chrono>
#include <random>

#include "Transpose.h"

bool exists[TABLE_SIZE];
int depths[TABLE_SIZE];
int best_eval[TABLE_SIZE];

Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table()
{
	clear_table();
	
	Bitstring seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::mt19937 generator(seed);

	for (int square = 0; square < 64; square++) {
		for (int piece = 0; piece < 13; piece++) {
			rand_bitstrings[square][piece] = generator();
		}
	}
	color_bitstring = generator();
	for (int col = 0; col < 8; col++) {
		en_passant_bistrings[col] = generator();
	}
	for (int i = 0; i < 4; i++) {
		castling_bitstrings[i] = generator();
	}
}

void clear_table() {
	std::memset(exists, 0, sizeof(exists));
	std::memset(depths, 0, sizeof(depths));
}
