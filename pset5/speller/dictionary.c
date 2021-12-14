// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int wordcount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    node *n = table[index];

    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (&word[0] == NULL)
    {
        return 0;
    }
    int hashedindex = toupper(word[0]) - 65;
    return hashedindex;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    int index = 0;
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char newWord[LENGTH + 1];

    while (fscanf(file, "%s", newWord) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, newWord);
        index = hash(newWord);
        n->next = table[index];
        table[index] = n;
        wordcount ++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        while (n != NULL)
        {
            node *buffer = n;
            n = n->next;
            free(buffer);
        }

        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}