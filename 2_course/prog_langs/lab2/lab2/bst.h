#ifndef BST_H
#define BST_H

#include "purchase.h"

typedef struct BSTNode {
    Purchase data;
    struct BSTNode* left;
    struct BSTNode* right;
} BSTNode;

typedef struct {
    BSTNode* root;
    int size;
} PurchaseBST;

void bst_init(PurchaseBST* tree);
void bst_free(PurchaseBST* tree);
void bst_insert(PurchaseBST* tree, const Purchase* p);
int bst_remove_by_index(PurchaseBST* tree, int index);
void bst_print_range(const PurchaseBST* tree, int from_day, int from_month, int from_year, int to_day, int to_month, int to_year);
void bst_print_all(const PurchaseBST* tree);

#endif
