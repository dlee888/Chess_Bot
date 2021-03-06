#include "Search.h"

long long nodes, qsearch_nodes;
long long tb_hits, qsearch_hits;

int orig_eval;

int prune = 500;

 bool greater(const pdi &a, const pdi &b)
{
	return a.first > b.first;
}
 bool less(const pdi &a, const pdi &b)
{
	return a.first < b.first;
}