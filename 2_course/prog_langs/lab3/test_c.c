#include <stdio.h>
#include <unistd.h>

int main() {
    for (int i = 1; i <= 5; i++) {
        printf("C: строка %d\n", i);
        fflush(stdout);
        usleep(200000);
    }
    return 0;
}
