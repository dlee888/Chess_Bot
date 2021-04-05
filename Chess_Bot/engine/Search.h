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

extern int priority;

extern bool break_now;

bool move_comparator(const int &a, const int &b);

Value search(Depth, Value, Value);

Value qsearch(Value, Value);

pii find_best_move(Depth);

const int RAZOR_MARGIN = 600;

int futility_margin(int, bool);

extern std::map <int, int> eval_cache;
#endif // !SEARCH_H_INCLUDED
