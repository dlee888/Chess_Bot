#ifndef NNUE_INCLUDED
#define NNUE_INCLUDED
#include <vector>
#include <fstream>
#include <cmath>

#include "types.h"
#include "State.h"

void load_nnue(std::string path);

Value run_nnue(state& s);

class Model {
public:
	std::vector <std::vector <std::vector <float> > > weights;
	std::vector <std::vector <float> > biases;

	void load(std::string path);

	float run(const std::vector <int>& inputs);

	void print() {
		for (auto i : weights) {
			for (auto j : i) {
				for (float k : j) {
					std::cout << k << " ";
				}
				std::cout << std::endl;
			}
			std::cout << std::endl;
		}
	}
};

extern Model white_model, black_model;
#endif