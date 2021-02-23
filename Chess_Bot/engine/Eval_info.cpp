#include "Eval_info.h"

int QVAL = 930;
int RVAL = 500;
int BVAL = 320;
int NVAL = 305;
int PVAL = 100;

int devel_coeff = 4, center_coeff = 18, ksafety_coeff = 10, castle_bonus = 25, pass_pawn_coeff = 45,
	   dpawn_coeff = 10, activity_coeff = 8;

int default_cnts[13] = {1, 1, 2, 2, 2, 8, 32, 8, 2, 2, 2, 1, 1}, cnts[13];

int white_devel, black_devel, white_center, black_center;

// counting the number of pawns in each row to compute doubled pawns
int white_pawn_counts[8] = {1, 1, 1, 1, 1, 1, 1, 1}, black_pawn_counts[8] = {1, 1, 1, 1, 1, 1, 1, 1};

int doubled_white, doubled_black;
int whitepawn_row_sum, blackpawn_row_sum;

std::vector<pii> whitepawns, whiteknights, whitebishops, whiterooks, whitequeens, whitekings;
std::vector<pii> blackpawns, blackknights, blackbishops, blackrooks, blackqueens, blackkings;

void init_eval_info()
{
	white_devel = 0;
	black_devel = 0;
	white_center = 0;
	black_center = 0;

	for (int i = 0; i < 13; i++)
	{
		cnts[i] = default_cnts[i];
	}

	for (int i = 0; i < 8; i++)
	{
		white_pawn_counts[i] = 1;
		black_pawn_counts[i] = 1;
	}

	whitepawn_row_sum = blackpawn_row_sum = 8;
	doubled_black = 0;
	doubled_white = 0;

	whitepawns.clear();
	whiteknights.clear();
	whitebishops.clear();
	whiterooks.clear();
	whitequeens.clear();
	whitekings.clear();
	blackpawns.clear();
	blackknights.clear();
	blackbishops.clear();
	blackrooks.clear();
	blackqueens.clear();
	blackkings.clear();

	for (int i = 0; i < 8; i++)
	{
		whitepawns.push_back(std::make_pair(6, i));
		blackpawns.push_back(std::make_pair(1, i));
	}

	whiteknights.push_back(std::make_pair(7, 1));
	whiteknights.push_back(std::make_pair(7, 6));
	blackknights.push_back(std::make_pair(0, 1));
	blackknights.push_back(std::make_pair(0, 6));

	whitekings.push_back(std::make_pair(7, 4));
	blackkings.push_back(std::make_pair(0, 4));

	whitequeens.push_back(std::make_pair(7, 3));
	blackqueens.push_back(std::make_pair(0, 3));

	whiterooks.push_back(std::make_pair(7, 0));
	whiterooks.push_back(std::make_pair(7, 7));
	blackrooks.push_back(std::make_pair(0, 0));
	blackrooks.push_back(std::make_pair(0, 7));

	whitebishops.push_back(std::make_pair(7, 2));
	whitebishops.push_back(std::make_pair(7, 5));
	blackbishops.push_back(std::make_pair(0, 2));
	blackbishops.push_back(std::make_pair(0, 5));
}

int king_safety[8][8] = {
	{-15, -14, -14, -13, -13, -14, -14, -15},
	{-14, -13, -13, -13, -13, -13, -13, -14},
	{-13, -12, -12, -11, -11, -12, -12, -13},
	{-10, -10, -10, -9, -9, -10, -10, -10},
	{-8, -7, -6, -6, -6, -6, -7, -8},
	{-4, -3, -3, -3, -3, -3, -3, -4},
	{-1, 0, 0, -1, -1, 0, 0, -1},
	{1, 4, 3, 2, 2, 3, 4, 1}
};
int knight_devel[8][8] = {
	{-8, -7, -3, -1, -1, -3, -7, -8},
	{-6, -1, 1, 0, 0, 1, -1, -6},
	{0, 2, 3, 4, 4, 3, 2, 0},
	{1, 4, 5, 7, 7, 5, 4, 1},
	{1, 5, 8, 10, 10, 8, 5, 1},
	{-1, 6, 10, 9, 9, 10, 6, -1},
	{-3, 1, 0, 7, 7, 0, 1, -3},
	{-4, -3, -2, -1, -1, -2, -3, -4}
};
int bishop_devel[8][8] = {
	{1, 4, 6, 8, 8, 6, 4, 1},
	{10, 10, 10, 10, 10, 10, 10, 10},
	{10, 10, 10, 11, 11, 10, 10, 10},
	{10, 12, 8, 10, 10, 8, 12, 10},
	{11, 10, 12, 10, 10, 12, 10, 11},
	{10, 12, 10, 8, 8, 10, 12, 10},
	{11, 11, 10, 6, 6, 10, 11, 11},
	{1, 1, 0, 1, 1, 0, 1, 1},
};
int pawn_center[8][8] = {
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 30, 30, 0, 0, 0},
	{0, 0, 20, 30, 30, 20, 0, 0},
	{0, 0, 16, 10, 10, 16, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
};
int knight_center[8][8] = {
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 5, 5, 0, 0, 0},
	{0, 0, 10, 10, 10, 10, 0, 0},
	{0, 10, 18, 10, 10, 18, 10, 0},
	{0, 0, 0, 8, 8, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0},
};
int king_activity[8][8] = {
	{0, 0, 0, 0, 0, 0, 0, 0},
	{1, 2, 2, 2, 2, 2, 2, 1},
	{2, 3, 4, 5, 5, 4, 3, 2},
	{2, 3, 5, 7, 7, 5, 3, 2},
	{1, 3, 5, 7, 7, 5, 3, 1},
	{0, 2, 3, 5, 5, 3, 1, 0},
	{0, 2, 2, 2, 2, 2, 2, 0},
	{0, 0, 0, 0, 0, 0, 0, 0}
};
