#include <cstring>

#include "Transpose.h"
#include "State.h"

long long comp_exp[64];

long long f_exp2(long long power)
{
	long long base = BASE, ans = 1;
	power = power%(BASE-1);
	while(power){
		if(power&1) (ans*=base)%MOD;
		(base*=base)%MOD, power>>=1;
	}
	return ans;
}

bool exists[TABLE_SIZE];
state positions[TABLE_SIZE];
int depths[TABLE_SIZE];
pdi best_moves[TABLE_SIZE];

void init_table()
{
	memset(exists, 0, sizeof(exists));
	memset(depths, -1, sizeof(depths));
	for (int i = 0; i < TABLE_SIZE; i++)
	{
		positions[i] = state();
		best_moves[i] = pdi(0, -1);
	}
}
