// The same deep call chain on an ordinary OS thread.
#include <stdio.h>

int depth(int n) {
    volatile char pad[64];   // a little room per call, like a real function
    pad[0] = 0; pad[n % 64] = 0;
    if (n == 0) return pad[0];
    return depth(n - 1) + pad[n % 64] + 1;
}

int main(void) {
    printf("calls deep: %d\n", depth(1000000));
    return 0;
}
