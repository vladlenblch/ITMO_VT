#include "bst.h"
#include <stdlib.h>
#include <stdio.h>

static int date_cmp(const Purchase* a, const Purchase* b) {
    if (a->year != b->year) return a->year - b->year;
    if (a->month != b->month) return a->month - b->month;
    return a->day - b->day;
}

void bst_init(PurchaseBST* tree) {
    tree->root = NULL;
    tree->size = 0;
}

// команда 0 (логика)
static void bst_free_nodes(BSTNode* node) {
    if (!node) return;
    bst_free_nodes(node->left);
    bst_free_nodes(node->right);
    free(node);
}

// команда 0 (вызов)
void bst_free(PurchaseBST* tree) {
    bst_free_nodes(tree->root);
    tree->root = NULL;
    tree->size = 0;
}

// команда 1 (логика)
static BSTNode* bst_insert_node(BSTNode* node, const Purchase* p) {
    if (!node) {
        BSTNode* n = (BSTNode*)malloc(sizeof(BSTNode));
        n->data = *p;
        n->left = n->right = NULL;
        return n;
    }
    if (date_cmp(p, &node->data) < 0)
        node->left = bst_insert_node(node->left, p);
    else
        node->right = bst_insert_node(node->right, p);
    return node;
}

// команда 1 (вызов)
void bst_insert(PurchaseBST* tree, const Purchase* p) {
    tree->root = bst_insert_node(tree->root, p);
    tree->size++;
}

// команда 2 (логика)
static int bst_inorder_remove(BSTNode** node, int* curr, int target) {
    if (!*node) return 0;
    if (bst_inorder_remove(&(*node)->left, curr, target)) return 1;
    if (*curr == target) {
        BSTNode* tmp;
        if (!(*node)->left) {
            tmp = *node;
            *node = (*node)->right;
            free(tmp);
        } else if (!(*node)->right) {
            tmp = *node;
            *node = (*node)->left;
            free(tmp);
        } else {
            BSTNode** min = &(*node)->right;
            while ((*min)->left) min = &(*min)->left;
            (*node)->data = (*min)->data;
            return bst_inorder_remove(min, curr, 0);
        }
        return 1;
    }
    (*curr)++;
    return bst_inorder_remove(&(*node)->right, curr, target);
}

// команда 2 (вызов)
int bst_remove_by_index(PurchaseBST* tree, int index) {
    int curr = 0;
    int res = bst_inorder_remove(&tree->root, &curr, index);
    if (res) tree->size--;
    return res;
}

// команда 3 (логика)
static void bst_inorder_print_range(const BSTNode* node, int from, int to, int* idx, int fd, int fm, int fy, int td, int tm, int ty, int* found) {
    if (!node) return;
    bst_inorder_print_range(node->left, from, to, idx, fd, fm, fy, td, tm, ty, found);
    int after_from = (node->data.year > fy) || (node->data.year == fy && node->data.month > fm) || (node->data.year == fy && node->data.month == fm && node->data.day >= fd);
    int before_to = (node->data.year < ty) || (node->data.year == ty && node->data.month < tm) || (node->data.year == ty && node->data.month == tm && node->data.day <= td);
    if (after_from && before_to) {
        purchase_print(&node->data, *idx);
        *found = 1;
    }
    (*idx)++;
    bst_inorder_print_range(node->right, from, to, idx, fd, fm, fy, td, tm, ty, found);
}

// команда 3 (вызов)
void bst_print_range(const PurchaseBST* tree, int fd, int fm, int fy, int td, int tm, int ty) {
    int idx = 0;
    int found = 0;
    printf("\npurchases in selected interval:\n");
    bst_inorder_print_range(tree->root, 0, tree->size-1, &idx, fd, fm, fy, td, tm, ty, &found);
    if (!found) {
        printf("no purchases in selected interval\n");
    }
    printf("\n");
}

// команда 4 (логика)
static void bst_inorder_print(const BSTNode* node, int* idx, int* found) {
    if (!node) return;
    bst_inorder_print(node->left, idx, found);
    purchase_print(&node->data, *idx);
    *found = 1;
    (*idx)++;
    bst_inorder_print(node->right, idx, found);
}

// команда 4 (вызов)
void bst_print_all(const PurchaseBST* tree) {
    int idx = 0;
    int found = 0;
    printf("\nall purchases:\n");
    bst_inorder_print(tree->root, &idx, &found);
    if (!found) {
        printf("no purchases\n");
    }
    printf("\n");
}