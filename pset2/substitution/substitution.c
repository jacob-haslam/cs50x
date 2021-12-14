#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int main(int argc,string argv[])
{
    char cipher[25];
    int i,l,j;
    string result;
    char currVal;

    if(argc!=2)
    {
        printf("Usage: ./substitution key\n");
        return(1);
    }
    else if(strlen(argv[1])!=26)
    {
        printf("Key must contain 26 characters.\n");
        return(1);
    }
    for(i=0; i<26; i++)
    {
        cipher[i] = toupper(argv[1][i]);

        if (cipher[i]>'Z'|| cipher[i]<'A')
        {
            printf("Key must contain only characters.\n");
            return(1);
        }
    }
    for(i=0; i<26; i++)
    {
        for(j=0; j<26; j++)
        {
            if (cipher[i]==cipher[j] && i!=j)
            {
            printf("Key must not contain duplicate characters.\n");
            return(1);
            }
        }
    }
    string input = get_string("plaintext: ");
    l=strlen(input);
    char text[l];
    for(i=0; i<=l; i++)
    {
        if(isupper(input[i]))
        {
            text[i] = cipher[input[i] - 65];
        }
        else if(islower(input[i]))
        {
            text[i] = tolower(cipher[input[i] - 97]);
        }
        else
        {
            text[i]=input[i];
        }
    }

    printf("ciphertext:%s\n",text);
    return 0;
}