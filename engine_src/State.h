#ifndef STATE_H_INCLUDED
#define STATE_H_INCLUDED

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <stack>
#include <cstring>

#include "Eval_info.h"
#include "Transpose.h"

extern std::string start_fen;

extern int dr_knight[8], dc_knight[8], dr_bishop[4], dc_bishop[4], dr_rook[4],
dc_rook[4], dr_queen[8], dc_queen[8], dr_king[8], dc_king[8];

class state
{
public:
	bool out_of_bounds(int row, int column)
	{
		if (row < 0)
			return true;
		if (column < 0)
			return true;
		if (row >= 8)
			return true;
		if (column >= 8)
			return true;
		return false;
	}

	int board[8][8];
	Bitstring board_hash;

	void replace_board(int row, int col, int piece);

	Bitstring get_hash()
	{
		return board_hash ^ (to_move ? color_bitstring : 0) ^ ((en_passant_target.top() == -1) ? 0 : en_passant_bistrings[en_passant_target.top() >> 3]) ^
			(wk_rights.top() ? castling_bitstrings[0] : 0) ^ (wq_rights.top() ? castling_bitstrings[1] : 0) ^ (bk_rights.top() ? castling_bitstrings[2] : 0) ^
			(bq_rights.top() ? castling_bitstrings[3] : 0);
	}

	std::stack<bool> wq_rights, bq_rights, wk_rights, bk_rights; // Castling rights
	std::stack<int> en_passant_target;							 // En passant target square
	bool white_castled = false, black_castled = false;
	std::stack <int> fifty_move;
	bool to_move; // true if white to move
	int full_move;

	state()
	{
		load(start_fen);
	}
	void load(std::string fen);
	std::string to_fen();

	char to_piece(int x);
	int piece_to_int(char c);
	std::string move_to_string(int move);

	void print();

	int parse_move(std::string move);

	void make_move(int move);
	void unmake_move(int move);

	int attacking(int row, int col, bool color);

	std::vector<int> list_moves();

	bool adjucation();

	int mate();

	bool legal_check(int move) {
		std::vector <int> moves = list_moves();
		for (int i : moves) {
			if (move == i) {
				make_move(move);
				if (king_attacked()) {
					unmake_move(move);
					return false;
				}
				unmake_move(move);
				return true;
			}
		}
		return false;
	}

	bool is_check() {
		if (to_move) {
			return attacking(piecelists[WK + 6][0].first, piecelists[WK + 6][0].second, true) != 7;
		} else {
			return attacking(piecelists[BK + 6][0].first, piecelists[BK + 6][0].second, false) != 7;
		}
	}
	
	bool king_attacked() {
		if (!to_move) {
			return attacking(piecelists[WK + 6][0].first, piecelists[WK + 6][0].second, true) != 7;
		} else {
			return attacking(piecelists[BK + 6][0].first, piecelists[BK + 6][0].second, false) != 7;
		}
	}
};

extern state curr_state;
#endif // !STATE_H_INCLUDED
