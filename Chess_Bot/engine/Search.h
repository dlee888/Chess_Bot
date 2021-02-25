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
extern long long tb_hits, collisions;

extern int orig_eval;

extern int prune;

bool greater(const pdi &a, const pdi &b);
bool less(const pdi &a, const pdi &b);

pdi search(int, int, int, int = -1);

pdi qsearch(int, int);
#endif // !SEARCH_H_INCLUDED
