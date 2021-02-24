#include <cstring>
#include <chrono>
#include <random>

#include "Transpose.h"

bool exists[TABLE_SIZE];
// state positions[TABLE_SIZE];
int depths[TABLE_SIZE];
pdi best_moves[TABLE_SIZE];

unsigned long long rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table()
{
	unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::mt19937 generator(seed);

	memset(exists, 0, sizeof(exists));
	memset(depths, -1, sizeof(depths));
	for (int i = 0; i < TABLE_SIZE; i++)
	{
		best_moves[i] = pdi(0, -1);
	}

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
