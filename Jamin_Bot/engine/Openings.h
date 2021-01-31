#ifndef OPENINGS_H_INCLUDED
#define OPENINGS_H_INCLUDED
#include <string>
#include <cstring>

#include "State.h"

#define NUM_ALL 20
#define NUM_WHITE 2
#define NUM_BLACK 2

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

std::string all[NUM_ALL][100] = {
	{"Queen's gambit declined, modern variation", "d4", "d5", "c4", "e6", "Nc3", "Nf6", "Bg5", "Be7", "e3", "O-O", "Nf3", "h6", "Bh4"}, 
	{"Tarrasach defense, two knights variation", "d4", "d5", "c4", "e6", "Nc3", "c5", "cxd5", "exd5", "Nf3", "Nc6", "g3"}, 
	{"Ruy lopez, morphy defense, caro", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "b5", "Bb3", "Nf6"}, 
	{"Semi slav defense", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "e6", "e3", "Nbd7", "Bd3", "dxc4", "Bxc4"}, 
	{"Ruy lopez, morphy defense, closed", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "0-0", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "0-0", "d4"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "a4", "Bf5"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "e4", "b5", "Be2"}, 
	{"Slav Defense: Modern, Geller Gambit", "e4", "e5", "Nf3", "Nf6", "Nxe5", "d6", "Nf3", "Nxe4"}, 
	{"Pirc Defense : Classical Variation", "e4", "d6", "d4", "Nf6", "Nc3", "g6", "Nf3", "Bg7", "Bc4", "O-O", "O-O"}, 
	{"Semi Slav Defense", "d4", "d5", "c4", "e6", "Nc3", "c6", "Nf3", "Nf6", "Bg5", "h6"}, 
	{"Queen's gambit accepted", "d4", "d5", "c4", "dxc4", "e4", "Nf6", "e5", "Nd5", "Bxc4", "Nc6", "Nc3"}, 
	{"Queen's gambit accepted, McDonell defense", "d4", "d5", "c4", "dxc4", "e4", "e5", "Nf3", "exd4", "Bxc4", "Nc6", "O-O"}, 
	{"King's indian defense", "d4", "Nf6", "c4", "g6", "Nc3", "Bg7", "e4", "d6", "Nf3", "O-O", "Be2", "e5", "O-O", "Nc6", "d5", "Ne7"}, 
	{"Grunfeld defense", "d4", "Nf6", "c4", "g6", "Nc3", "d5", "cxd5", "Nxd5", "e4", "Nxc3", "bxc3"}, 
	{"Four Knights Game: Double Spanish Variation", "e4", "e5", "Nf3", "Nc6", "Bb5", "Nf6", "Nc3", "Bb4", "O-O", "O-O"}, 
	{"Sicilian defense: Sheveningen Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Be3", "e6", "Qd2", "Nd7", "f3", "b5", "a3", "Bb7", "0-0-0", "Rc8"}, 
	{"Silician defense: Sveshnikov Variation", "e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "e5", "Ndb5", "d6", "Nd5", "Nxd5", "exd5", "Ne7", "c4", "Nf5"}, 
	{"Silician defense: Lasker-Pelikan Variation", "e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "e5", "Ndb5", "a6", "Nd6+", "Bxd6", "Qxd6"},
	{"Sicilian defense: Open, Najdorf Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Bg5", "Nbd7", "Bc4", "Qb6", "Bb3", "e6", "Qd2", "Be7", "0-0-0", "Nc5"},
	{"Sicilian defense: Open, Najdorf Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Bg5", "Nbd7", "f4", "e6", "Qf3", "Qc7", "0-0-0", "Be7", "g4", "b5", "Bxf6", "Nxf6", "g5", "Nd7", "f5", "Bxg5", "Kb1", "Ne5", "Qh5"}
};

std::string white[NUM_WHITE][100] = {
	{"French defense: Winnever variation", "e4", "e6", "d4", "d5", "Nc3", "Bb4", "Nf3"}, // petition to get rid of the french
	{"blah", "d4"}
};

std::string black[NUM_BLACK][100] = {
	{"blah", "d4"}, // temporary holder
	{"blah", "e4"} // temporary holder
};

std::vector<opening> openings, black_openings, white_openings;
// black openings are really good for black (engine will never play it as white)
// white openings are really good for white (engine will never play it as black)

void load_openings()
{
	for (int i = 0; i < NUM_ALL; i++)
		openings.push_back(opening(all[i][0], all[i] + 1));
	for (int i = 0; i < NUM_WHITE; i++)
		white_openings.push_back(opening(white[i][0], white[i] + 1));
	for (int i = 0; i < NUM_BLACK; i++)
		black_openings.push_back(opening(black[i][0], black[i] + 1));
}

void scramble_openings()
{
	for (int iter = 0; iter < (int)openings.size(); iter++)
		for (int ind = iter; ind < (int)openings.size() - 1; ind++)
			if (rand()&1)
				std::swap(openings[ind], openings[ind + 1]);
	for (int iter = 0; iter < (int) white_openings.size(); iter++)
		for (int ind = iter; ind < (int) white_openings.size() - 1; ind++)
			if (rand()&1)
				std::swap(white_openings[ind], white_openings[ind + 1]);
	for (int iter = 0; iter < (int) black_openings.size(); iter++)
		for (int ind = iter; ind < (int) black_openings.size() - 1; ind++)
			if (rand()&1)
				std::swap(black_openings[ind], black_openings[ind + 1]);
}

#endif // !OPENINGS_H_INCLUDED
