#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED

#include <stdlib.h>

// 1. Structure Definition
typedef struct node
{
    int data; 
    struct node* left;
    struct node* right; 
} node;


node* CreateNode(int valeur);
void insertNewNode(node** racine, int val);

#endif 