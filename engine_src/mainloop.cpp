#include <ctime>

#include "Bot_2_5.h"
#include "types.h"

void init_everything()
{
	init_table();
	curr_state = state();
	load_openings();
	scramble_openings();
	init_eval_info();
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
				int move_i;
				while (true)
				{
					std::cin >> move_i;
					if (move_i == -1) {
						break;
					}

					curr_state.make_move(move_i);
					num_move++;
				}
			}

			std::string res;
			for (int i = 0; i < 8; i++)
			{
				int last = -1;
				for (int j = 0; j < 8; j++)
				{
					std::string piece = curr_state._to_piece(curr_state.board[i][j]);
					if (piece == "  ")
					{
						if (last == -1)
						{
							last = j;
						}
					}
					else
					{
						if (last != -1)
						{
							res += std::to_string(j - last);
							last = -1;
						}
						if (piece[0] == 'B')
						{
							res += piece[1] - 'A' + 'a';
						}
						else
						{
							res += piece[1];
						}
					}
				}
				if (last != -1)
				{
					res += std::to_string(8 - last);
				}
				if (i != 7)
					res += '/';
			}
			res += ' ';

			if (curr_state.to_move)
			{
				res += "w ";
			}
			else
			{
				res += "b ";
			}

			if (curr_state.wk_rights.top())
			{
				res += 'K';
			}
			if (curr_state.wq_rights.top())
			{
				res += 'Q';
			}
			if (curr_state.bk_rights.top())
			{
				res += 'k';
			}
			if (curr_state.bq_rights.top())
			{
				res += 'q';
			}
			if (res[res.size() - 1] == ' ')
			{
				res += '-';
			}
			res += ' ';
			if (curr_state.en_passant_target.top() == -1)
			{
				res += "- ";
			}
			else
			{
				int targ = curr_state.en_passant_target.top();
				res += (char)((targ & 7) + 'a');
				res += (char)('8' - (targ >> 3));
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
