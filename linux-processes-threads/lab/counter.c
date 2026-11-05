/* counter: N workers each add 1 to "the number" a million times.
 * Threads share one number (and race without --lock); processes each get their own copy. */
#include "common.h"
#include <pthread.h>
#include <sys/wait.h>
#include <unistd.h>

#define TIMES 1000000
static volatile long number = 0;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void *add(void *arg) {
    (void)arg;
    for (long i = 0; i < TIMES; i++) {
        if (use_lock) pthread_mutex_lock(&m);
        number = number + 1;
        if (use_lock) pthread_mutex_unlock(&m);
    }
    return NULL;
}

int main(int argc, char **argv) {
    parse(argc, argv, "--threads N [--lock] | --processes N");
    setvbuf(stdout, NULL, _IONBF, 0);
    if (use_threads) {
        pthread_t t[256];
        printf("%d threads share one number%s.\n", workers, use_lock ? ", with a lock" : "");
        for (int i = 0; i < workers; i++) pthread_create(&t[i], NULL, add, NULL);
        for (int i = 0; i < workers; i++) pthread_join(t[i], NULL);
        printf("expected: %ld\n", (long)workers * TIMES);
        printf("result:   %ld\n", number);
    } else {
        printf("%d processes, each with its own copy.\n", workers);
        for (int i = 0; i < workers; i++) {
            if (fork() == 0) {
                add(NULL);
                usleep(20000 * i);   /* print in order */
                printf("process %d: its copy is %ld\n", i + 1, number);
                exit(0);
            }
        }
        while (wait(NULL) > 0) {}
        printf("parent:    its copy is %ld\n", number);
    }
    return 0;
}
