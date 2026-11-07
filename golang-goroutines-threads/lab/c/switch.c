// Two OS threads hand a token back and forth (a mutex and a condition variable).
#include <pthread.h>
#include <stdio.h>
#include <time.h>

#define ROUNDS 200000
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv = PTHREAD_COND_INITIALIZER;
static int turn = 0;

static void *player(void *arg) {
    int me = *(int *)arg;
    for (int i = 0; i < ROUNDS; i++) {
        pthread_mutex_lock(&mu);
        while (turn != me) pthread_cond_wait(&cv, &mu);
        turn = 1 - me;
        pthread_cond_signal(&cv);
        pthread_mutex_unlock(&mu);
    }
    return NULL;
}

int main(void) {
    struct timespec a, b; int ids[2] = {0, 1}; pthread_t t[2];
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (int i = 0; i < 2; i++) pthread_create(&t[i], NULL, player, &ids[i]);
    for (int i = 0; i < 2; i++) pthread_join(t[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &b);
    double ns = ((b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec)) / (2.0 * ROUNDS);
    printf("threads, one hand-off:    %.0f ns\n", ns);
    return 0;
}
