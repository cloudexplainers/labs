#include <stdio.h>
#include "times.h"
#include "fares.h"

int main(void) {
    printf("Next ferry: %s\n", next_ferry());
    printf("Last ferry: %s\n", last_ferry());
    printf("Adult fare: %.2f\n", adult_fare());
    return 0;
}
