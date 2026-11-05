/* crash: N workers run for a moment; worker 3 touches memory it doesn't own (a segmentation fault). */
#include "common.h"
#include <pthread.h>
#include <signal.h>
#include <sys/wait.h>
#include <unistd.h>

static void work(int id, const char *kind) {
    if (id == 3) {
        usleep(500000);
        printf("%s 3: bad memory access!\n", kind);
        volatile int *bad = NULL;
        *bad = 1;                                 /* the bug */
    }
    usleep(1000000 + 100000 * id);
    printf("%s %d: finished\n", kind, id);
}

static void *thread_main(void *arg) { work((int)(long)arg, "thread"); return NULL; }

int main(int argc, char **argv) {
    parse(argc, argv, "--threads N | --processes N");
    setvbuf(stdout, NULL, _IONBF, 0);
    if (use_threads) {
        pthread_t t[64];
        printf("starting %d threads in one process\n", workers);
        for (int i = 0; i < workers; i++) pthread_create(&t[i], NULL, thread_main, (void *)(long)(i + 1));
        for (int i = 0; i < workers; i++) pthread_join(t[i], NULL);
        printf("all threads finished\n");
    } else {
        pid_t p[64];
        printf("starting %d processes\n", workers);
        for (int i = 0; i < workers; i++)
            if ((p[i] = fork()) == 0) { work(i + 1, "process"); exit(0); }
        int st[64];
        for (int i = 0; i < workers; i++) waitpid(p[i], &st[i], 0);
        for (int i = 0; i < workers; i++)
            if (WIFSIGNALED(st[i])) printf("parent: process %d was killed (%s)\n", i + 1, strsignal(WTERMSIG(st[i])));
        printf("parent: still running\n");
    }
    return 0;
}
