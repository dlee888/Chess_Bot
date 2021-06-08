#ifndef OPTIONS_H_INCLUDED
#define OPTIONS_H_INCLUDED
#include <map>
#include <string>

#include "types.h"

std::map <std::string, int> options;

void set_default_options() {
	options["time_limit"] = 5;
	options["depth_limit"] = MAX_DEPTH;
}
#endif