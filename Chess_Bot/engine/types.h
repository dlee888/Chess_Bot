#ifndef TYPES_INCLUDED
#define TYPES_INCLUDED
#include <map>

typedef std::pair<int, int> pii;

typedef unsigned long long Bitstring;

// Definitely not copied from SF
enum Value : int {
	VALUE_ZERO = 0,
    VALUE_INFINITE = 1000000,

	MATE = 100000,
	MATED = -100000,
	DRAWN = 0,

	PawnValueMg   =  100,  PawnValueEg   =  133,
	KnightValueMg =  325,  KnightValueEg =  300,
	BishopValueMg =  371,  BishopValueEg =  380,
	RookValueMg   =  563,  RookValueEg   =  669,
	QueenValueMg  = 1000,  QueenValueEg  = 1033,

	RESIGN = 1000
};

enum Depth : int {
	ONE_PLY = 1,

	DEPTH_ZERO          =  0,
	DEPTH_QS_NO_CHECKS  = -1
};

#define ENABLE_BASE_OPERATORS_ON(T)                                \
constexpr T operator+(T d1, T d2) { return T(int(d1) + int(d2)); } \
constexpr T operator-(T d1, T d2) { return T(int(d1) - int(d2)); } \
constexpr T operator-(T d) { return T(-int(d)); }                  \
inline T& operator+=(T& d1, T d2) { return d1 = d1 + d2; }         \
inline T& operator-=(T& d1, T d2) { return d1 = d1 - d2; }

#define ENABLE_INCR_OPERATORS_ON(T)                                \
inline T& operator++(T& d) { return d = T(int(d) + 1); }           \
inline T& operator--(T& d) { return d = T(int(d) - 1); }

#define ENABLE_FULL_OPERATORS_ON(T)                                \
ENABLE_BASE_OPERATORS_ON(T)                                        \
constexpr T operator*(int i, T d) { return T(i * int(d)); }        \
constexpr T operator*(T d, int i) { return T(int(d) * i); }        \
constexpr T operator/(T d, int i) { return T(int(d) / i); }        \
constexpr int operator/(T d1, T d2) { return int(d1) / int(d2); }  \
inline T& operator*=(T& d, int i) { return d = T(int(d) * i); }    \
inline T& operator/=(T& d, int i) { return d = T(int(d) / i); }

ENABLE_FULL_OPERATORS_ON(Value)
ENABLE_FULL_OPERATORS_ON(Depth)

#undef ENABLE_FULL_OPERATORS_ON
#undef ENABLE_INCR_OPERATORS_ON
#undef ENABLE_BASE_OPERATORS_ON

/// Additional operators to add integers to a Value
constexpr Value operator+(Value v, int i) { return Value(int(v) + i); }
constexpr Value operator-(Value v, int i) { return Value(int(v) - i); }
inline Value& operator+=(Value& v, int i) { return v = v + i; }
inline Value& operator-=(Value& v, int i) { return v = v - i; }

#endif