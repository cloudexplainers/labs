// One OS thread per waiting customer, the classic way (POSIX threads).
// Usage: ./threads N
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t open_now = PTHREAD_COND_INITIALIZER;
static int shop_open = 0;

static void *customer(void *arg) {
    pthread_mutex_lock(&mu);
    while (!shop_open) pthread_cond_wait(&open_now, &mu);   // wait, doing nothing
    pthread_mutex_unlock(&mu);
    return NULL;
}

static long kb(const char *file, const char *key) {          // a line from /proc, in kB
    char line[256]; long v = -1; FILE *f = fopen(file, "r");
    while (fgets(line, sizeof line, f))
        if (strncmp(line, key, strlen(key)) == 0) sscanf(line + strlen(key), " %ld", &v);
    fclose(f); return v;
}

static double now(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9;
}

int main(int argc, char **argv) {
    int n = atoi(argv[1]);
    pthread_t *t = malloc(sizeof(pthread_t) * n);
    long kstack0 = kb("/proc/meminfo", "KernelStack:");
    double t0 = now();
    int started = 0;
    for (int i = 0; i < n; i++) {
        int rc = pthread_create(&t[i], NULL, customer, NULL);
        if (rc) { printf("thread %d failed: %s\n", i + 1, strerror(rc)); break; }
        started++;
    }
    double took = now() - t0;
    long rss = kb("/proc/self/status", "VmRSS:"), vm = kb("/proc/self/status", "VmSize:");
    long kstack = kb("/proc/meminfo", "KernelStack:") - kstack0;
    printf("threads started:   %d\n", started);
    printf("OS threads:        %ld\n", kb("/proc/self/status", "Threads:"));
    printf("time to start:     %.3f s\n", took);
    printf("memory used:       %ld MB\n", rss / 1024);
    printf("kernel stacks:     %ld MB\n", kstack / 1024);
    printf("stack reserved:    %ld GB\n", vm / 1024 / 1024);
    pthread_mutex_lock(&mu); shop_open = 1; pthread_cond_broadcast(&open_now); pthread_mutex_unlock(&mu);
    for (int i = 0; i < started; i++) pthread_join(t[i], NULL);
    return 0;
}
