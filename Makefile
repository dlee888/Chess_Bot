a : bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o
	g++ bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o

bin/Eval_info.o : Chess_bot/engine/Eval_info.cpp Chess_bot/engine/Eval_info.h
	g++ -c Chess_bot/engine/Eval_info.cpp -o bin/Eval_info.o

bin/Evaluate.o : Chess_bot/engine/Evaluate.cpp Chess_bot/engine/Evaluate.h
	g++ -c Chess_bot/engine/Evaluate.cpp -o bin/Evaluate.o

bin/List_moves.o : Chess_bot/engine/List_moves.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/List_moves.cpp -o bin/List_moves.o

bin/mainloop.o : Chess_bot/engine/mainloop.cpp Chess_bot/engine/Engine.h Chess_bot/engine/Bot_2_2.h
	g++ -c Chess_bot/engine/mainloop.cpp -o bin/mainloop.o

bin/Make_move.o : Chess_bot/engine/Make_move.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/Make_move.cpp -o bin/Make_move.o

bin/Search_util.o : Chess_bot/engine/Search_util.cpp Chess_bot/engine/Search.h
	g++ -c Chess_bot/engine/Search_util.cpp -o bin/Search_util.o

bin/Search.o : Chess_bot/engine/Search.cpp Chess_bot/engine/Search.h
	g++ -c Chess_bot/engine/Search.cpp -o bin/Search.o

bin/State_constants.o : Chess_bot/engine/State_constants.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/State_constants.cpp -o bin/State_constants.o

bin/State_io.o : Chess_bot/engine/State_io.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/State_io.cpp -o bin/State_io.o

bin/State_util.o : Chess_bot/engine/Search_util.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/State_util.cpp -o bin/State_util.o

bin/Transpose.o : Chess_bot/engine/Transpose.cpp Chess_bot/engine/Transpose.h
	g++ -c Chess_bot/engine/Transpose.cpp -o bin/Transpose.o

bin/Unmake_move.o : Chess_bot/engine/Unmake_move.cpp Chess_bot/engine/State.h
	g++ -c Chess_bot/engine/Unmake_move.cpp -o bin/Unmake_move.o

clear : 
	rm a bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o