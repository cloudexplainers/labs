/* spawn: start N workers that do nothing, wait for all of them, print how long that took. */
#include "common.h"
#include <pthread.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static void *nothing(void *arg) { return arg; }

int main(int argc, char **argv) {
    parse(argc, argv, "--threads N | --processes N");
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (int i = 0; i < workers; i++) {
        if (use_threads) {
            pthread_t t;
            pthread_create(&t, NULL, nothing, NULL);
            pthread_join(t, NULL);
        } else {
            pid_t p = fork();
            if (p == 0) _exit(0);
            waitpid(p, NULL, 0);
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &b);
    double ms = (b.tv_sec - a.tv_sec) * 1e3 + (b.tv_nsec - a.tv_nsec) / 1e6;
    printf("%d %s started and finished in %.0f ms\n", workers, use_threads ? "threads" : "processes", ms);
    return 0;
}
