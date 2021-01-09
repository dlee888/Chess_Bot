#include "Eval_info.h"

double QVAL = 9.3;
double KVAL = 420.0;
double RVAL = 5.0;
double BVAL = 3.2;
double NVAL = 3.1;
double PVAL = 1.0;

double devel_coeff = 0.425, center_coeff = 0.185, ksafety_coeff = 0.1, castle_bonus = 1.5, pass_pawn_coeff = 0.35,
dpawn_coeff = 0.2, activity_coeff = 0.8;

int default_cnts[13] = { 1,1,2,2,2,8,32,8,2,2,2,1,1 }, cnts[13];

double white_devel, black_devel, white_center, black_center;

// counting the number of pawns in each row to compute doubled pawns
int white_pawn_counts[8] = { 1,1,1,1,1,1,1,1 }, black_pawn_counts[8] = { 1,1,1,1,1,1,1,1 };

int doubled_white, doubled_black;
int whitepawn_row_sum, blackpawn_row_sum;

std::vector <pii> whitepawns, whiteknights, whitebishops, whiterooks, whitequeens, whitekings;
std::vector <pii> blackpawns, blackknights, blackbishops, blackrooks, blackqueens, blackkings;

void init_eval_info() {
	white_devel = 0; black_devel = 0; white_center = 0; black_center = 0;

	for (int i = 0; i < 13; i++) {
		cnts[i] = default_cnts[i];
	}

	for (int i = 0; i < 8; i++) {
		white_pawn_counts[i] = 1;
		black_pawn_counts[i] = 1;
	}

	whitepawn_row_sum = blackpawn_row_sum = 8;
	doubled_black = 0; doubled_white = 0;

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

	for (int i = 0; i < 8; i++) {
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

double king_safety[8][8] =
{
{-15, -14, -14, -13, -13, -14, -14, -15},
{-14, -13, -13, -13, -13, -13, -13, -14},
{-13, -12, -12, -11, -11, -12, -12, -13},
{-10, -10, -10,  -9,  -9, -10, -10, -10},
{ -8,  -7,  -6,  -6,  -6,  -6,  -7,  -8},
{ -4,  -3,  -3,  -3,  -3,  -3,  -3,  -4},
{ -1,   0,   0,  -1,  -1,   0,   0,  -1},
{  1,   4,   3,   2,   2,   3,   4,   1}
};
double knight_devel[8][8] =
{
{-0.8, -0.7, -0.3, -0.1, -0.1, -0.3, -0.7, -0.8},
{-0.6, -0.1, 0.1, 0.0, 0.0, 0.1, -0.1, -0.6},
{0.0, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.0},
{0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1},
{0.1, 0.5, 0.8, 1.0, 1.0, 0.8, 0.5, 0.1},
{-0.1, 0.6, 1.3, 1.1, 1.1, 1.3, 0.6, -0.1},
{-0.3, 0.1, 0.0, 0.7, 0.7, 0.0, 0.1, -0.3},
{-0.4, -0.3, -0.2, -0.1, -0.1, -0.2, -0.3, -0.4}
};
double bishop_devel[8][8] =
{
{1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
{1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
{1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
{1.0, 1.1, 1.0, 1.1, 1.1, 1.0, 1.1, 1.0},
{1.0, 1.0, 1.2, 1.0, 1.0, 1.2, 1.0, 1.0},
{1.0, 1.2, 1.0, 1.0, 1.0, 1.0, 1.2, 1.0},
{1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1},
{0.1, 0.1, 0.0, 0.1, 0.1, 0.0, 0.1, 0.1},
};
double pawn_center[8][8] =
{
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 3.0, 3.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 2.0, 3.0, 3.0, 2.0, 0.0, 0.0},
{0.0, 0.0, 1.6, 1.0, 1.0, 1.6, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
};
double knight_center[8][8] =
{
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0},
{0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0},
{0.0, 1.0, 1.8, 1.0, 1.0, 1.8, 1.0, 0.0},
{0.0, 0.0, 0.0, 0.8, 0.8, 0.0, 0.0, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
};
double king_activity[8][8] =
{
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
{0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1},
{0.2, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.2},
{0.2, 0.3, 0.5, 0.7, 0.7, 0.5, 0.3, 0.2},
{0.1, 0.3, 0.5, 0.7, 0.7, 0.5, 0.3, 0.1},
{0.0, 0.2, 0.3, 0.5, 0.5, 0.3, 0.1, 0.0},
{0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0},
{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}
};
