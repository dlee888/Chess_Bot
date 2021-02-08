#ifndef TRANSPOSE_INFO_H_INCLUDED
#define TRANSPOSE_INFO_H_INCLUDED

#define TABLE_SIZE 200003 // prime number close to 200000

#define SAFETY 3000045 // 15 * table_size

#define MOD TABLE_SIZE
#define BASE 13

extern long long comp_exp[64];

long long f_exp2(long long power);
#endif // !TRANSPOSE_INFO_H_INCLUDED
