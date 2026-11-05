/* The same loop in C: plain 8-byte integers, compiled to machine code ahead of time (best of 3). */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 10000000
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
int main(void) {
    long long *prices = malloc(N * sizeof *prices);
    for (long long i = 0; i < N; i++) prices[i] = i % 50;
    double best = 1e9; volatile long long total = 0;
    for (int r = 0; r < 3; r++) {
        double t = now(); long long s = 0;
        for (long long i = 0; i < N; i++) s += prices[i];
        total = s; double d = now() - t; if (d < best) best = d;
    }
    printf("total:  %lld dollars\nC loop: %.4f s\n", (long long)total, best);
    return 0;
}
