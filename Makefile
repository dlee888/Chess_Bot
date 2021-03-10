engine : engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o engine_bin/mainloop.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o engine_bin/Transpose.o engine_bin/Unmake_move.o
	g++ -o engine engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o engine_bin/mainloop.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o engine_bin/Transpose.o engine_bin/Unmake_move.o

engine_bin/Eval_info.o :
	g++ -c Chess_Bot/engine/Eval_info.cpp -o engine_bin/Eval_info.o

engine_bin/Evaluate.o : Chess_Bot/engine/Evaluate.cpp Chess_Bot/engine/Evaluate.h
	g++ -c Chess_Bot/engine/Evaluate.cpp -o engine_bin/Evaluate.o

engine_bin/List_moves.o : Chess_Bot/engine/List_moves.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/List_moves.cpp -o engine_bin/List_moves.o

engine_bin/mainloop.o : Chess_Bot/engine/mainloop.cpp Chess_Bot/engine/Engine.h Chess_Bot/engine/Bot_2_2.h
	g++ -c Chess_Bot/engine/mainloop.cpp -o engine_bin/mainloop.o

engine_bin/Make_move.o : Chess_Bot/engine/Make_move.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/Make_move.cpp -o engine_bin/Make_move.o

engine_bin/Search_util.o : Chess_Bot/engine/Search_util.cpp Chess_Bot/engine/Search.h
	g++ -c Chess_Bot/engine/Search_util.cpp -o engine_bin/Search_util.o

engine_bin/Search.o : Chess_Bot/engine/Search.cpp Chess_Bot/engine/Search.h
	g++ -c Chess_Bot/engine/Search.cpp -o engine_bin/Search.o

engine_bin/State_constants.o : Chess_Bot/engine/State_constants.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_constants.cpp -o engine_bin/State_constants.o

engine_bin/State_io.o : Chess_Bot/engine/State_io.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_io.cpp -o engine_bin/State_io.o

engine_bin/State_util.o : Chess_Bot/engine/Search_util.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_util.cpp -o engine_bin/State_util.o

engine_bin/Transpose.o : Chess_Bot/engine/Transpose.cpp Chess_Bot/engine/Transpose.h
	g++ -c Chess_Bot/engine/Transpose.cpp -o engine_bin/Transpose.o

engine_bin/Unmake_move.o : Chess_Bot/engine/Unmake_move.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/Unmake_move.cpp -o engine_bin/Unmake_move.o

clear : 
	rm engine test engine_bin/Tester.o engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o engine_bin/mainloop.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o engine_bin/Transpose.o engine_bin/Unmake_move.o

test : engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o engine_bin/Tester.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o engine_bin/Transpose.o engine_bin/Unmake_move.o
	g++ -o test engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o engine_bin/Tester.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o engine_bin/Transpose.o engine_bin/Unmake_move.o

engine_bin/Tester.o: Chess_Bot/engine/Tester.cpp
	g++ -c Chess_Bot/engine/Tester.cpp -o engine_bin/Tester.o