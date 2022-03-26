#include <chrono>
#include <cstring>
#include <random>

#include "Transpose.h"

bool* tt_exists;
Depth* tt_depths;
Value* tt_evals;
Bitstring* tt_hashes;
int* tt_fullmove;

int table_size;

Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table(int new_table_size) {
	clear_table();
	table_size = new_table_size;
	tt_exists = new bool[table_size];
	tt_depths = new Depth[table_size];
	tt_evals = new Value[table_size];
	tt_hashes = new Bitstring[table_size];
	tt_fullmove = new int[table_size];

	Bitstring seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::mt19937_64 generator(seed);

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
	delete[] tt_exists;
	delete[] tt_depths;
	delete[] tt_evals;
	delete[] tt_hashes;
	delete[] tt_fullmove;
}
