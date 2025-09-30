#ifndef PURCHASE_H
#define PURCHASE_H

typedef struct {
    char name[64];
    char comment[128];
    double amount;
    int day, month, year;
} Purchase;

void purchase_init(Purchase* p, const char* name, const char* comment, double amount, int day, int month, int year);
void purchase_print(const Purchase* p, int index);

#endif
