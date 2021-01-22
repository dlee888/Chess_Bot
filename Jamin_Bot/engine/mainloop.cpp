#include <ctime>

#include "Engine.h"
#include "Bot_2_2.h"

state curr_state;

void init_everything()
{
	curr_state = state();
	load_openings();
	scramble_openings();
	init_eval_info();
}

void instructions()
{
	printf("Beat Jamin supports 3 commands: analyse, play, and find_best_move\n\nanalyse requires you to input a game and a depth.\n"
		   "Depth 4 is recommended, since anything higher would take more than a few seconds per move. Depth 7 may take up to a few hours per move, though it is sometimes faster.\n\n"
		   "play lets you play against the program.\n\n"
		   "find_best_move finds the best move in a given position. You will be required to enter a game in progress.\n"
		   "find_best_move also has a second version, activated by entering find_best_move2. This will ask for a specific depth to search instead of asking for how long you want it to think for.\n\n"
		   "When entering a game, enter it in this format: 1. [white\'s move] [black\'s move] 2. [white\'s move] [black\'s move] 3. ... *\n"
		   "For example, to enter the main line of the french defense advance variation, you would enter: 1. e4 e6 2. d4 d5 3. e5 c5 4. c3 *\n\n"
		   "You can view this message by typing \'help\'.\n\n"
		   "You can exit the program by typing \'quit\'\n\n\n");
}

void intro()
{
	printf(
		".----------------.  .----------------.  .----------------.  .----------------.        .----------------.  .----------------.  .----------------.  .----------------.  .---------------- - .\n"
		"| .--------------. || .--------------. || .--------------. || .--------------. |      | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. | \n"
		"| |   ______     | || |  _________   | || |      __      | || |  _________   | |      | |     _____    | || |      __      | || | ____    ____ | || |     _____    | || | ____  _____  | |\n"
		"| |  |_   _ \\    | || | |_   ___  |  | || |     /  \\     | || | |  _   _  |  | |      | |    |_   _|   | || |     /  \\     | || ||_   \\  / _|| ||   |    |_   _|   | || ||_   \\ | _   _| |\n"
		"| |    | |_) |   | || |   | |_  \\_|  | || |    / /\\ \\    | || | |_/ | | \\_|  | |      | |      | |     | || |    / /\\ \\    | || |  |   \\/   |  | || |      | |     | || |  |   \\ | |   | |\n"
		"| |    |  __\'.   | || |   |  _|  _   | || |   / ____ \\   | || |     | |      | |      | |   _  | |     | || |   / ____ \\   | || |  | |\\  /| |  | || |      | |     | || |  | |\\ \\| |   | |\n"
		"| |   _| |__) |  | || |  _| |___/ |  | || | _/ /    \\ \\_ | || |    _| |_     | |      | |  | |_\' |     | || | _/ /    \\ \\_ | || | _| |_\\/_| |_ | || |     _| |_    | || | _| |_\\   |_  | |\n"
		"| |  |_______/   | || | |_________|  | || ||____|  |____|| || |   |_____|    | |      | |  `.___.'     | || ||____|  |____|| || ||_____||_____|| || |    |_____|   | || ||_____|\\____| | |\n"
		"| |              | || |              | || |              | || |              | |      | |              | || |              | || |              | || |              | || |              | |\n"
		"| \'--------------\' || \'--------------\' || \'--------------\' || \'--------------\' |      | \'--------------\' || \'--------------\' || \'--------------\' || \'--------------\' || \'--------------\' | \n"
		"\'----------------\'  \'----------------\'  \'----------------\'  \'----------------\'        \'----------------\'  \'----------------\'  \'----------------\'  \'----------------\'  \'----------------\'\n\n");
	printf("Version 2.2.11");
	instructions();
}

int main()
{
	srand(time(NULL));
	//intro();
	std::string cmnd;
	while (cmnd != "exit")
	{
		init_everything();
		std::cout << ">>>\n";
		std::cin >> cmnd;
		if (cmnd == "play")
		{
			play();
		}
		else if (cmnd == "analyse")
		{
			std::cout << "What depth do you want?\n";
			int depth;
			std::cin >> depth;
			analyse_game(depth);
		}
		else if (cmnd == "find_best_move")
		{
			get_best_move();
		}
		else if (cmnd == "find_best_move2")
		{
			get_best_move2();
		}
		else if (cmnd == "help")
		{
			instructions();
		}
		else if (cmnd == "fen")
		{
			int num_move = 0;
			std::string move;
			std::cout << "Do you want to load a game in progress?\n";
			std::cin >> move;
			if (move == "yes")
			{
				std::cout << "Please enter the game:\n";
				//loading by typing in moves, such as 1. e4 e5 2. d4 ...
				while (!(move == "*"))
				{
					if (num_move % 2 == 0)
						std::cin >> move;
					if (move == "*")
						break;
					std::cin >> move;
					if (move == "*")
						break;
					int move_i = curr_state.parse_move(move);
					curr_state.make_move(move_i);
					num_move++;
					for (int i = 0; i < openings.size(); i++)
					{
						if (openings[i].moves[num_move - 1] != move_i)
						{
							openings.erase(openings.begin() + i);
							i--;
						}
					}
				}
			}
			else if (move == "yes2")
			{
				std::cout << "Please enter the game:\n";
				//loading by typing in moves, such as 1. e4 e5 2. d4 ...
				while (!(move == "*"))
				{
					if (num_move % 2 == 0)
						std::cin >> move;
					if (move == "*")
						break;
					std::cin >> move;
					if (move == "*")
						break;
					int move_i = std::stoi(move);
					curr_state.make_move(move_i);
					num_move++;
					for (int i = 0; i < openings.size(); i++)
					{
						if (openings[i].moves[num_move - 1] != move_i)
						{
							openings.erase(openings.begin() + i);
							i--;
						}
					}
				}
			}
			std::string res;
			for (int i = 0; i < 8; i++)
			{
				int last = -1;
				for (int j = 0; j < 8; j++)
				{
					std::string piece = curr_state.to_piece(curr_state.board[i][j]);
					if (piece == "  ") {
						if (last == -1) {
							last = j;
						}
					} else {
						if (last != -1) {
							res += std::to_string(j - last);
							last = -1;
						}
					if (piece[0] == 'B') {
						res += piece[1] - 'A' + 'a';
					} else {
						res += piece[1];
					}
					}
				}
				res += '/';
			}
			res += ' ';
			if (curr_state.wk_rights.top()) {
				res += 'K';
			}
			if (curr_state.wq_rights.top()) {
				res += 'Q';
			}
			if (curr_state.bk_rights.top()) {
				res += 'k';
			}
			if (curr_state.bq_rights.top()) {
				res += 'q';
			}
			if (res[res.size() - 1] == ' ') {
				res += '-';
			}
			res += ' ';
			if (curr_state.en_passant_target.top() == -1) {
				res += "- ";
			} else {
				int targ = curr_state.en_passant_target.top();
				res += targ&7 + 'a';
				res += '8' - (targ>>3);
				res += ' ';
			}
			res += std::to_string(curr_state.fifty_move) + " ";
			res += std::to_string(curr_state.full_move);
			std::cout << res << std::endl;
		}
		else if (cmnd == "quit")
		{
			break;
		}
		else
		{
			std::cout << "COMMAND NOT RECOGNIZED\n";
		}
	}
	return 0;
}
