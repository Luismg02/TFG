#include <stdlib.h>
#include <stdio.h>

typedef struct node
{
    char key;          // valor
    struct node *next; // puntero al siguiente elemento.
} Node;

int main(void)
{
    Node *n = malloc(sizeof(Node));
    n->key = 'K';
    n->next = NULL;

    free(n);

    printf("%c\n", n->key);
}
