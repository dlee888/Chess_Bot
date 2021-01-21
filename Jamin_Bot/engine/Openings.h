#ifndef OPENINGS_H_INCLUDED
#define OPENINGS_H_INCLUDED
#include <string>
#include <cstring>

#include "State.h"

#define NUM_OPENINGS 16

class opening
{
public:
	std::string name;
	int moves[100];
	opening(std::string _name, std::string m[100])
	{
		name = _name;
		memset(moves, -1, sizeof(moves));
		init_eval_info();
		state temp = state();
		for (int i = 0; i < 100; i++)
		{
			if (m[i].size() < 2)
				break;
			moves[i] = temp.parse_move(m[i]);
			temp.make_move(moves[i]);
		}
	}
	opening()
	{
		memset(moves, -1, sizeof(moves));
	}
};

std::string temp[NUM_OPENINGS][100] = {
	{"Queen's gambit declined, modern variation", "d4", "d5", "c4", "e6", "Nc3", "Nf6", "Bg5", "Be7", "e3", "O-O", "Nf3", "h6", "Bh4"}, 
	{"French defense advance variation, Paulsen attack", "e4", "e6", "d4", "d5", "e5", "c5", "c3", "Nc6", "Nf3", "Nge7"}, 
	{"Tarrasach defense, two knights variation", "d4", "d5", "c4", "e6", "Nc3", "c5", "cxd5", "exd5", "Nf3", "Nc6", "g3"}, 
	{"Ruy lopez, morphy defense, caro", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "b5", "Bb3", "Nf6"}, 
	{"Semi slav defense", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "e6", "e3", "Nbd7", "Bd3", "dxc4", "Bxc4"}, 
	{"Ruy lopez, morphy defense, closed", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "d4"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "a4", "Bf5"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "e4", "b5", "Be2"}, 
	{"Slav Defense: Modern, Geller Gambit", "e4", "e5", "Nf3", "Nf6", "Nxe5", "d6", "Nf3", "Nxe4"}, 
	{"Pirc Defense : Classical Variation", "e4", "d6", "d4", "Nf6", "Nc3", "g6", "Nf3", "Bg7", "Bc4", "O-O", "O-O"}, 
	{"Semi Slav Defense", "d4", "d5", "c4", "e6", "Nc3", "c6", "Nf3", "Nf6", "Bg5", "h6"}, 
	{"Queen's gambit accepted", "d4", "d5", "c4", "dxc4", "e4", "Nf6", "e5", "Nd5", "Bxc4", "Nc6", "Nc3"}, 
	{"Queen's gambit accepted, McDonell defense", "d4", "d5", "c4", "dxc4", "e4", "e5", "Nf3", "exd4", "Bxc4", "Nc6", "O-O"}, 
	{"King's indian defense", "d4", "Nf6", "c4", "g6", "Nc3", "Bg7", "e4", "d6", "Nf3", "O-O", "Be2", "e5", "O-O", "Nc6", "d5", "Ne7"}, 
	{"Grunfeld defense", "d4", "Nf6", "c4", "g6", "Nc3", "d5", "cxd5", "Nxd5", "e4", "Nxc3", "bxc3"}, 
	{"Four Knights Game: Double Spanish Variation", "e4", "e5", "Nf3", "Nc6", "Bb5", "Nf6", "Nc3", "Bb4", "O-O", "O-O"}};

std::vector<opening> openings;

void load_openings()
{
	for (int i = 0; i < NUM_OPENINGS; i++)
	{
		openings.push_back(opening(temp[i][0], temp[i] + 1));
	}
}

void scramble_openings()
{
	for (int iter = 0; iter < (int)openings.size(); iter++)
	{
		for (int ind = iter; ind < (int)openings.size() - 1; ind++)
		{
			if (rand() % 2 == 1)
			{
				std::swap(openings[ind], openings[ind + 1]);
			}
		}
	}
}

#endif // !OPENINGS_H_INCLUDED
