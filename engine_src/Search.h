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

void replace_tt(Bitstring, Depth, Value, Bitstring, int);

Value search(Depth, Value, Value);

Value qsearch(Value, Value, Depth);

pii find_best_move();

const int RAZOR_MARGIN = 600;
const int TEMPO = 15;

int futility_margin(int, bool);

extern std::mt19937 rng;

int count_positions(int);
#endif // !SEARCH_H_INCLUDED
