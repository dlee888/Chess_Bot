#ifndef OPTIONS_H_INCLUDED
#define OPTIONS_H_INCLUDED
#include <map>
#include <string>

#include "types.h"

extern std::map<std::string, int> options;

void set_default_options();
#endif