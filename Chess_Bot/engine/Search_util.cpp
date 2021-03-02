#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits;

int orig_eval;

int prune = 500;

inline bool greater(const pdi &a, const pdi &b)
{
	return a.first > b.first;
}
inline bool less(const pdi &a, const pdi &b)
{
	return a.first < b.first;
}