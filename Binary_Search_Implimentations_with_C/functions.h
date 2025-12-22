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

typedef struct queue
{
    node* data;
    struct queue* next; 
}queue;


node* CreateNode(int valeur);
void insertNewNode(node** racine, int val);

//Queue manipulation functions headers to display trees : 

queue* CreateQueue(node* data);

void enqueue(queue** q,node* N);
node* dequeue(queue** q);
int estVide(queue** file);

void DesplaybyLevel(node* racine);
#endif 