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
#include "options.h"

extern long long nodes, qsearch_nodes;
extern long long tb_hits, qsearch_hits;

extern bool break_now;

extern Depth depth_qsearched, qs_depth_floor;

Value search(Depth, Value, Value);

Value qsearch(Value, Value, Depth);

pii find_best_move();

const int RAZOR_MARGIN = 600;

int futility_margin(int, bool);
#endif // !SEARCH_H_INCLUDED
