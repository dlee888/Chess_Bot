a : Eval_info.o Evaluate.o List_moves.o mainloop.o Make_move.o Search_util.o Search.o State_constants.o State_io.o State_util.o Transpose.o Unmake_move.o
	g++ Eval_info.o Evaluate.o List_moves.o mainloop.o Make_move.o Search_util.o Search.o State_constants.o State_io.o State_util.o Transpose.o Unmake_move.o

Eval_info.o : Eval_info.cpp Eval_info.h
	g++ -c Eval_info.cpp

Evaluate.o : Evaluate.cpp Evaluate.h
	g++ -c Evaluate.cpp

List_moves.o : List_moves.cpp State.h
	g++ -c List_moves.cpp

mainloop.o : mainloop.cpp Engine.h Bot_2_2.h
	g++ -c mainloop.cpp

Make_move.o : Make_move.cpp State.h
	g++ -c Make_move.cpp

Search_util.o : Search_util.cpp Search.h
	g++ -c Search_util.cpp

Search.o : Search.cpp Search.h
	g++ -c Search.cpp

State_constants.o : State_constants.cpp State.h
	g++ -c State_constants.cpp

State_io.o : State_io.cpp State.h
	g++ -c State_io.cpp

Transpose.o : Transpose.cpp Transpose.h
	g++ -c Transpose.cpp

Unmake_move.o : Unmake_move.cpp State.h
	g++ -c Unmake_move.cpp

clean : 
	rm a Eval_info.o Evaluate.o List_moves.o mainloop.o Make_move.o Search_util.o Search.o State_constants.o State_io.o State_util.o Transpose.o Unmake_move.o