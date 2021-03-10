#include <iostream>

#include "Search.h"

void init_everything()
{
	init_eval_info();
	init_table();
	curr_state = state();
}

int main() {
	init_everything();
	curr_state.make_move(curr_state.parse_move("b3"));
    std::cout << search(1, -INF, INF) << std::endl;
}