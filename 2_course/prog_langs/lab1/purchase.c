#include "purchase.h"
#include <stdio.h>
#include <string.h>

void purchase_init(Purchase* p, const char* name, const char* comment, double amount, int day, int month, int year) {
    strncpy_s(p->name, sizeof(p->name), name, 63); p->name[63] = 0;
    strncpy_s(p->comment, sizeof(p->comment), comment, 127); p->comment[127] = 0;
    p->amount = amount;
    p->day = day; p->month = month; p->year = year;
}

void purchase_print(const Purchase* p, int index) {
    printf("%d. %s | %s | %.2f | %02d.%02d.%04d\n", index, p->name, p->comment, p->amount, p->day, p->month, p->year);
}