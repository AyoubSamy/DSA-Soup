#include <stdio.h>
#include <stdlib.h>
#include "functions.h"

int main()
{
    node * arbre = NULL;
    insertNewNode(&arbre,70);
    insertNewNode(&arbre,77);
    insertNewNode(&arbre,75);
    insertNewNode(&arbre,63);
    return 0 ;
}