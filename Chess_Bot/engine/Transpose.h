#ifndef TRANSPOS_H_INCLUDED
#define TRANSPOS_H_INCLUDED
#include <map>

#include "State.h"

typedef std::pair<double, int> pdi;

extern long long comp_exp[64];

extern bool exists[TABLE_SIZE];
extern state positions[TABLE_SIZE];
extern int depths[TABLE_SIZE];
extern pdi best_moves[TABLE_SIZE];

void init_table();
#endif // !TRANSPOS_H_INCLUDED
