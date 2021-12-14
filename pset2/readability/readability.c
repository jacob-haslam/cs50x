#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

int main(void)
{
    int i,x;
    int words = 1;
    int sentences = 0;
    int letters = 0;
    string text = get_string("Text: ");

    for(i = 0, x = strlen(text); i<x; i++)
    {
        if(text[i]>='A' && text[i]<='z')
        {
            letters++;
        }
        else if (text[i]==' ')
        {
            words++;
        }
        else if (text[i]=='.'||text[i]=='?'||text[i]=='!')
        {
            sentences++;
        }
    }

    float l = (letters / (float) words) * 100;
    float s = (sentences / (float) words) * 100;

    float index = 0.0588 * l - 0.296 * s - 15.8;

    if(index<1)
    {
        printf("Before Grade 1\n");
    }
    else if(index>16)
    {
        printf("Grade 16+\n");
    }
    else
    {
    printf("Grade %i\n",(int)round(index));
    }
}