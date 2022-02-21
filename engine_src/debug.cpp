#include "Search.h"

int count_positions(int depth) {
	if (depth == 0) {
		return 1;
	}
	int ans = 0;
	auto moves = curr_state.list_moves();
	for (auto move : moves) {
		curr_state.make_move(move);
		if (curr_state.king_attacked()) {
			curr_state.unmake_move(move);
			continue;
		}
		ans += count_positions(depth - 1);
		curr_state.unmake_move(move);
	}
	return ans;
}