/* burn: N workers keep one CPU core busy each, for 6 seconds. */
#include "common.h"
#include <pthread.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static void *spin(void *arg) {
    time_t end = time(NULL) + 6;
    volatile unsigned long x = 0;
    while (time(NULL) < end) x++;
    return arg;
}

int main(int argc, char **argv) {
    parse(argc, argv, "--threads N | --processes N");
    if (use_threads) {
        pthread_t t[64];
        for (int i = 0; i < workers; i++) pthread_create(&t[i], NULL, spin, NULL);
        for (int i = 0; i < workers; i++) pthread_join(t[i], NULL);
    } else {
        for (int i = 0; i < workers; i++) if (fork() == 0) { spin(NULL); _exit(0); }
        while (wait(NULL) > 0) {}
    }
    return 0;
}
