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

#define n 8
#define BP -1
#define WP 1
#define BN -2
#define WN 2
#define BB -3
#define WB 3
#define BR -4
#define WR 4
#define BQ -5
#define WQ 5
#define BK -6
#define WK 6

extern int default_board[8][8];

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
		if (row >= n)
			return true;
		if (column >= n)
			return true;
		return false;
	}

	int board[8][8];
	unsigned long long board_hash;

	void replace_board(int row, int col, int piece)
	{
		board_hash ^= rand_bitstrings[(row << 3) + col][board[row][col] + 6];
		board_hash ^= rand_bitstrings[(row << 3) + col][piece + 6];
		board[row][col] = piece;
	}

	 unsigned long long get_hash()
	{
		return board_hash ^ (to_move ? color_bitstring : 0) ^ ((en_passant_target.top() == -1) ? 0 : en_passant_bistrings[en_passant_target.top() / 8]) ^
			(wk_rights.top() ? castling_bitstrings[0] : 0) ^ (wq_rights.top() ? castling_bitstrings[1] : 0) ^ (bk_rights.top() ? castling_bitstrings[2] : 0) ^
			(bq_rights.top() ? castling_bitstrings[3] : 0);
	}

	std::stack<bool> wq_rights, bq_rights, wk_rights, bk_rights; // Castling rights
	std::stack<int> en_passant_target;							 // En passant target square
	bool white_castled = false, black_castled = false;
	int fifty_move;
	bool to_move; // true if white to move
	int full_move;

	state()
	{
		fifty_move = 0;
		full_move = 0;
		to_move = true;

		std::memset(board, 0, sizeof(board));

		for (int i = 0; i < 8; i++)
			for (int j = 0; j < 8; j++)
				replace_board(i, j, default_board[i][j]);

		board_hash = 0;

		wq_rights.push(true);
		wk_rights.push(true);
		bq_rights.push(true);
		bk_rights.push(true);

		en_passant_target.push(-1);
	}

	std::string to_piece(int x);
	int piece_to_int(char c);
	std::string move_to_string(int move);

	bool operator==(state s)
	{
		if (s.to_move != to_move)
			return false;
		if (s.en_passant_target.top() != en_passant_target.top())
			return false;
		if (s.wk_rights.top() != wk_rights.top())
			return false;
		if (s.wq_rights.top() != wq_rights.top())
			return false;
		if (s.bk_rights.top() != bk_rights.top())
			return false;
		if (s.bq_rights.top() != bq_rights.top())
			return false;
		for (int i = 0; i < 8; i++)
			for (int j = 0; j < 8; j++)
				if (s.board[i][j] != board[i][j])
					return false;
		return true;
	}

	void print();

	int parse_move(std::string move);

	void make_move(int move);
	void unmake_move(int move);

	int attacking(int row, int col, bool color);
	int num_attack(int row, int col, bool color);

	std::vector<int> list_moves();

	bool adjucation();

	int mate();

	bool legal_check(int move) {
		std::vector <int> moves = list_moves();
		for (int i : moves) {
			if (move == i) return true;
		}
		return false;
	}
	// bool operator<(const State &s){ return true; }
};

extern state curr_state;
#endif // !STATE_H_INCLUDED
