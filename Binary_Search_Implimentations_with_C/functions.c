#include <stdio.h>
#include <stdlib.h>
#include "functions.h"

// Implementation of createNode
node* createNode(int valeur) {
    // 1. Allocate memory
    node* N = (node*) malloc(sizeof(node));
    N->data = valeur ; 
    N->left = N->right = NULL ; 
    return N ; 
}

//tow  cases to handle if the tree is Empty or there are at least one node 
void insertNewNode(node** racine, int val){
    node* N; 
    node* tmp;
    N=createNode(val);
    if(*racine == NULL)
        {
            *racine = N ;
            return;
        }
    tmp = *racine;
    while(1){
        if(N->data > tmp->data){
            if(tmp->right == NULL){
                tmp->right == N ;
                break;
            }
            else
                tmp = tmp->right ; 
            
        }
        else{
            if(tmp->left == NULL){
                tmp->left = N ;
                break;
            }
            else
                tmp = tmp->left ;
        }
    }  
}

queue* CreateQueue(node* data) {
    queue* p;
    p = (queue*)malloc(sizeof(queue));
    p->data = data;
    p->next = p ; 
    return p;
}

void enqueue(queue** q,node* N){
    queue* p;
    p=CreateQueue(N);

    if(*q!=NULL){
        p->next = (*q)->next ; 
        (*q)->next = p;
    }
    *q = p;
}

node* dequeue(queue** q)
{
    queue* temp;
    node* N=NULL;
    if(*q!=NULL)
    {
        temp=(*q)->next;
        if(temp==*q)
            *q=NULL;
        else
            (*q)->next=temp->next;
        N=temp->data;
        free(temp);

    }
     return N;
}
int estVide(queue** file)
 {
     return *file==NULL;
 }

 void DesplaybyLevel(node* racine){
    queue* q = NULL;
    node* Toprint=racine;
    while(Toprint!=NULL){
        if(Toprint->left!=NULL)
            enqueue(&q,Toprint->left);
        if(Toprint->right!=NULL)
            enqueue(&q,Toprint->right);
        
        printf("%d  ",Toprint->data);
        Toprint = dequeue(&q);
    }
}





