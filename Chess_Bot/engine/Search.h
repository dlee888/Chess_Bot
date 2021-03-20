#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED
#include <vector>
#include <algorithm>
#include <functional>
#include <cassert>

#include "State.h"
#include "Evaluate.h"
#include "Transpose.h"

#define INF 1000000007

extern long long nodes, qsearch_nodes;
extern long long tb_hits, qsearch_hits;

extern int orig_eval;

extern int prune, RESIGN;

extern int priority;

extern bool break_now;

bool move_comparator(const int &a, const int &b);

int search(int, int, int);

int qsearch(int, int);

pdi find_best_move(int);

enum {
	MATE = 100000,
	MATED = -100000,
	DRAWN = 0
};

const int RAZOR_MARGIN = 100, EXTENDED_RAZOR_MARGIN = 250;
#endif // !SEARCH_H_INCLUDED
