#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED
#include <vector>
#include <map>
#include <algorithm>
#include <functional>
#include <cassert>

#include "State.h"
#include "Evaluate.h"
#include "Transpose.h"

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

const int RAZOR_MARGIN = 600;

extern std::map <int, int> eval_cache;
#endif // !SEARCH_H_INCLUDED
