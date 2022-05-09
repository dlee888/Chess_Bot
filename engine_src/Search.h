#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED
#include <algorithm>
#include <cassert>
#include <functional>
#include <map>
#include <random>
#include <vector>

#include "Evaluate.h"
#include "State.h"
#include "Transpose.h"
#include "options.h"

extern long long nodes, qsearch_nodes;
extern long long tb_hits, qsearch_hits;

extern bool break_now;

extern Depth depth_qsearched, qs_depth_floor;

extern unsigned int mcts_prob;
extern int mcts_depth;
extern bool use_nnue;

Value search(Depth, Value, Value, bool = true);

Value qsearch(Value, Value, Depth);

pii find_best_move();

const int RAZOR_MARGIN = 600, TEMPO = 25, LMR_CUTOFF = 300;

int futility_margin(int);

extern std::mt19937 rng;

int count_positions(int);
#endif // !SEARCH_H_INCLUDED
