/* Shared by the lab programs: read "--threads N" or "--processes N" (and "--lock"). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int use_threads = -1, workers = 0, use_lock = 0;

static void parse(int argc, char **argv, const char *usage) {
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--threads") && i + 1 < argc) { use_threads = 1; workers = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--processes") && i + 1 < argc) { use_threads = 0; workers = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--lock")) use_lock = 1;
    }
    if (use_threads < 0 || workers < 1) { fprintf(stderr, "usage: %s %s\n", argv[0], usage); exit(2); }
}
