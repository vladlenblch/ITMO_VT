#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "purchase.h"
#include "bst.h"

int is_valid_date(int d, int m, int y) {
    if (y < 1 || m < 1 || m > 12 || d < 1) return 0;
    int days_in_month[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int leap = (y % 4 == 0 && (y % 100 != 0 || y % 400 == 0));
    if (leap && m == 2) {
        if (d > 29) return 0;
    } else {
        if (d > days_in_month[m - 1]) return 0;
    }
    return 1;
}

void print_menu() {
    printf("\nmenu:\n");
    printf("1. add purchase\n");
    printf("2. remove purchase by an index\n");
    printf("3. print purchases in date range\n");
    printf("4. print all purchases\n");
    printf("0. exit\n");
    printf("choose: ");
}

void clear_input() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {}
}

int main() {
    PurchaseBST tree;
    bst_init(&tree);

    int choice;
    while (1) {
        print_menu();
        if (scanf_s("%d", &choice) != 1) break;
        clear_input();
        if (choice == 0) break;
        if (choice == 1) {
            char name[64], comment[128];
            double amount;
            int d, m, y;
            printf("name: ");
            scanf_s("%63s", name, (unsigned)_countof(name));
            printf("comment: ");
            scanf_s("%127s", comment, (unsigned)_countof(comment));
            printf("amount: ");
            scanf_s("%lf", &amount);
            clear_input();
            do {
                printf("date (dd mm yyyy): ");
                scanf_s("%d%d%d", &d, &m, &y);
                clear_input();
                if (!is_valid_date(d, m, y)) {
                    printf("incorrect date\n");
                }
            } while (!is_valid_date(d, m, y));
            Purchase p;
            purchase_init(&p, name, comment, amount, d, m, y);
            bst_insert(&tree, &p);
            printf("purchase added\n\n");
        } else if (choice == 2) {
            int idx;
            printf("enter a purchase index for removing: ");
            scanf_s("%d", &idx);
            if (!bst_remove_by_index(&tree, idx)) {
                printf("no purchase with this index\n");
            }
        } else if (choice == 3) {
            int fd, fm, fy, td, tm, ty;
            do {
                printf("enter a start of an interval (dd mm yyyy): ");
                scanf_s("%d%d%d", &fd, &fm, &fy);
                if (!is_valid_date(fd, fm, fy)) {
                    printf("incorrect date\n");
                }
            } while (!is_valid_date(fd, fm, fy));
            do {
                printf("enter an end of an interval (dd mm yyyy): ");
                scanf_s("%d%d%d", &td, &tm, &ty);
                if (!is_valid_date(td, tm, ty)) {
                    printf("incorrect date\n");
                }
            } while (!is_valid_date(td, tm, ty));
            bst_print_range(&tree, fd, fm, fy, td, tm, ty);
        } else if (choice == 4) {
            bst_print_all(&tree);
        }
    }
    bst_free(&tree);
    return 0;
}