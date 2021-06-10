#include "State.h"

std::string start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

int dr_knight[8] = {2, 2, 1, 1, -1, -1, -2, -2}, dc_knight[8] = {1, -1, 2, -2, 2, -2, 1, -1};
int dr_bishop[4] = {1, 1, -1, -1}, dc_bishop[4] = {1, -1, 1, -1};
int dr_rook[4] = {1, -1, 0, 0}, dc_rook[4] = {0, 0, 1, -1};
int dr_queen[8] = {1, 1, 1, 0, 0, -1, -1, -1}, dc_queen[8] = {1, 0, -1, 1, -1, 1, 0, -1};
int dr_king[8] = {1, 1, 1, 0, 0, -1, -1, -1}, dc_king[8] = {1, 0, -1, 1, -1, 1, 0, -1};