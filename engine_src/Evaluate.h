#ifndef EVALUATE_H_INCLUDED
#define EVALUATE_H_INCLUDED
#include "State.h"
#include "nnue.h"

Value eval(state &s, bool trace = false, bool use_nnue = false);
#endif // !EVALUATE_H_INCLUDED
