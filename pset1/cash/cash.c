#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float change;
    int coins = 0;
//get change
    do
    {
        change = get_float("Change:");
    }
    while (change < 0);
//round to cents
    int cents = round(change * 100);
    
//divide
    while ((cents - 25) >= 0)
    {
        cents = cents-25;
        coins++;
    }
    while ((cents - 10) >= 0)
    {
        cents = cents-10;
        coins++;
    }
    while ((cents - 5) >= 0)
    {
        cents = cents-5;
        coins++;
    }
    while ((cents - 1) >= 0)
    {
        cents = cents-1;
        coins++;
    }

    printf("%i\n", coins);

}
    //quarters (25¢), dimes (10¢), nickels (5¢), pennies (1¢)