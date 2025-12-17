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



