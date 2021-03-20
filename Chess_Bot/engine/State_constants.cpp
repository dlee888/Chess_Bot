#include "State.h"

int default_board[8][8] =
    {
        {-4, -2, -3, -5, -6, -3, -2, -4},
        {-1, -1, -1, -1, -1, -1, -1, -1},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {1, 1, 1, 1, 1, 1, 1, 1},
        {4, 2, 3, 5, 6, 3, 2, 4}};

int dr_knight[8] = {2, 2, 1, 1, -1, -1, -2, -2}, dc_knight[8] = {1, -1, 2, -2, 2, -2, 1, -1};
int dr_bishop[4] = {1, 1, -1, -1}, dc_bishop[4] = {1, -1, 1, -1};
int dr_rook[4] = {1, -1, 0, 0}, dc_rook[4] = {0, 0, 1, -1};
int dr_queen[8] = {1, 1, 1, 0, 0, -1, -1, -1}, dc_queen[8] = {1, 0, -1, 1, -1, 1, 0, -1};
int dr_king[8] = {1, 1, 1, 0, 0, -1, -1, -1}, dc_king[8] = {1, 0, -1, 1, -1, 1, 0, -1};