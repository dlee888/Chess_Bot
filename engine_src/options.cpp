#include "options.h"

std::map <std::string, int> options;

void set_default_options() {
	options["time_limit"] = 969000;
	options["depth_limit"] = MAX_DEPTH;
	options["use_opening_book"] = 1;
	options["debug"] = 1;
}
