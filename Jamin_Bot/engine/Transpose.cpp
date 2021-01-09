#include <cstring>

#include "Transpose.h"
#include "State.h"

long long comp_exp[64];

long long f_exp2(long long power) {
	if (power == 0) return 1;
	if (power == 1) return (BASE + MOD) % MOD;
	if (comp_exp[power]) return comp_exp[power];
	long long ans = f_exp2(power / 2);
	ans = (ans * ans + MOD) % MOD;
	if (power % 2 == 1) ans = (ans * BASE + MOD) % MOD;
	return (ans + MOD) % MOD;
}

bool exists[TABLE_SIZE];
state positions[TABLE_SIZE];
int depths[TABLE_SIZE];
pdi best_moves[TABLE_SIZE];

void init_table() {
	memset(exists, 0, sizeof(exists));
	memset(depths, -1, sizeof(depths));
	for (int i = 0; i < TABLE_SIZE; i++) {
		positions[i] = state();
		best_moves[i] = pdi(0, -1);
	}
}
