#include "options.h"

std::map <std::string, int> options;

void set_default_options() {
	options["time_limit"] = 969696;
	options["depth_limit"] = MAX_DEPTH;
	options["use_opening_book"] = 1;
	options["debug"] = 1;
	options["mcts_prob"] = 200000000; // Probability of a MCTS prune, multiplied by INT_MAX
	options["mctx_max_depth"] = 5;
}
