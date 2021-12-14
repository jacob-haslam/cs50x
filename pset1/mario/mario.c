#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Enter Height");
    }

    while (height < 1 || height > 8);

    for (int row = 0; row < height; row++)
    {
        for (int col = 1; col < height - row; col++)
        {
            printf(" ");
        }

        for (int col = -1; col < row; col++)
        {
            printf("#");
        }

        printf("\n");
    }
}