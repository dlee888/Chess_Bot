#include <chrono>
#include <cstring>
#include <random>

#include "Transpose.h"

std::vector<bool> tt_exists;
std::vector<Depth> tt_depths;
std::vector<Value> tt_evals;
std::vector<Bitstring> tt_hashes;
std::vector<int> tt_fullmove;

int table_size;

Bitstring rand_bitstrings[64][13], color_bitstring, en_passant_bistrings[8], castling_bitstrings[4];

void init_table(int new_table_size) {
	clear_table();
	table_size = new_table_size;
	tt_exists.resize(table_size);
	tt_depths.resize(table_size);
	tt_evals.resize(table_size);
	tt_hashes.resize(table_size);
	tt_fullmove.resize(table_size);

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
	tt_exists.clear();
	tt_depths.clear();
	tt_evals.clear();
	tt_hashes.clear();
	tt_fullmove.clear();
}

void replace_tt(Depth depth, Value value, Bitstring hash, int fullmove) {
	int key = get_key(hash);
	if (!tt_exists[key] || (tt_exists[key] && tt_fullmove[key] + tt_depths[key] <= fullmove + depth)) {
		tt_exists[key] = true;
		tt_fullmove[key] = fullmove;
		tt_depths[key] = depth;
		tt_evals[key] = value;
		tt_hashes[key] = hash;
	}
}
