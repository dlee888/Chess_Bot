#include "nnue.h"

Model white_model, black_model;

void Model::load(std::string path) {
	std::ifstream archin(path + "/arch.txt");
	if (!archin) {
		std::cerr << "NNUE not found!" << std::endl;
		return;
	}
	int n;
	archin >> n;
	std::vector<int> dims(n + 1);
	for (int i = 0; i <= n; i++) {
		archin >> dims[i];
	}
	for (int i = 0; i < n; i++) {
		std::vector<std::vector<float>> layer_w(dims[i], std::vector<float>(dims[i + 1]));
		std::ifstream win(path + "/weights_" + std::to_string(i) + ".txt");
		if (!win) {
			std::cerr << "Weights for layer " << i << " not found!" << std::endl;
		}
		for (int j = 0; j < dims[i]; j++) {
			for (int k = 0; k < dims[i + 1]; k++) {
				win >> layer_w[j][k];
			}
		}
		std::vector<float> layer_b(dims[i + 1]);
		std::ifstream bin(path + "/biases_" + std::to_string(i) + ".txt");
		for (int j = 0; j < dims[i + 1]; j++) {
			bin >> layer_b[j];
		}
		weights.push_back(layer_w);
		biases.push_back(layer_b);
	}
}

float sigmoid(float x) { return 1 / (1 + exp(-x)); }
float swish(float x) { return x * sigmoid(x); }
float Model::run(const std::vector<int>& inputs) {
	std::vector<std::vector<float>> neurons(1, std::vector<float>(weights[0][0].size()));
	for (int i = 0; i < (int)inputs.size(); i++) {
		for (int j = 0; j < (int)weights[0][0].size(); j++) {
			neurons[0][j] += inputs[i] * weights[0][i][j];
		}
	}
	for (int i = 0; i < (int)weights[0][0].size(); i++) {
		neurons[0][i] = swish(neurons[0][i] + biases[0][i]);
	}
	for (int i = 1; i < (int)weights.size() - 1; i++) {
		std::vector<float> new_layer(weights[i][0].size());
		for (int k = 0; k < (int)weights[i - 1][0].size(); k++) {
			for (int j = 0; j < (int)weights[i][0].size(); j++) {
				new_layer[j] += neurons[i - 1][k] * weights[i][k][j];
			}
		}
		for (int j = 0; j < (int)weights[i][0].size(); j++) {
			new_layer[j] = swish(new_layer[j] + biases[i][j]);
		}
		neurons.push_back(new_layer);
	}
	float res = 0;
	for (int i = 0; i < (int)weights[weights.size() - 1][0].size(); i++) {
		res += neurons[weights.size() - 2][i] * weights[weights.size() - 1][i][0];
	}
	res = sigmoid(res + biases[biases.size() - 1][0]);
	return res;
}

Value get_value(float wdl) {
	if (wdl == 1) {
		return MATE;
	}
	float val = log(wdl / (1 - wdl));
	if (val > 0) {
		return Value(200.0 * sqrt(val));
	} else {
		return Value(-200.0 * sqrt(-val));
	}
}

Value run_nnue(state& s) {
	float prob;
	if (s.to_move) {
		prob = white_model.run(nnue_input);
	} else {
		prob = black_model.run(nnue_input);
	}
	// std::cout << prob << " " << get_value(prob) << std::endl;
	return get_value(prob);
}

void load_nnue(std::string path) {
	white_model.load(path + "/white");
	black_model.load(path + "/black");
	// white_model.print();
}
