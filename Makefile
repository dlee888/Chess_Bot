CC = g++
CFLAGS = -O3 -std=c++17 -Wall -Wextra -Wshadow -pedantic $(FLAGS)
CFILES = engine_bin/Eval_info.o engine_bin/Evaluate.o engine_bin/List_moves.o \
	engine_bin/mainloop.o engine_bin/Make_move.o engine_bin/Search_util.o engine_bin/Search.o \
	engine_bin/State_constants.o engine_bin/State_io.o engine_bin/State_util.o \
	engine_bin/Transpose.o engine_bin/Unmake_move.o engine_bin/options.o engine_bin/psqt.o engine_bin/nnue.o engine_bin/debug.o

KERNEL = $(shell uname -s)
ifeq ($(KERNEL),Linux)
	CFLAGS +=  -lpthread
endif

engine: $(CFILES)
	$(CC) $(CFILES) $(CFLAGS) -o $@

engine_bin/%.o : engine_src/%.cpp
	mkdir -p engine_bin
	$(CC) -c $(CFLAGS) $< -o $@

clear:
	rm engine_bin/*.o engine