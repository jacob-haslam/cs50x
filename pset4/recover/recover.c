#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;


int main(int argc, char *argv[])
{

    BYTE buffer[512];
    int counter = 0;
    char text[8];
    FILE *output;

    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");

    while (fread(buffer, 512, 1, input))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0)
            {
                sprintf(text, "%03i.jpg", counter);
                output = fopen(text, "w");
                fwrite(buffer, 512, 1, output);
                counter++;
            }
            else
            {
                fclose(output);
                sprintf(text, "%03i.jpg", counter);
                output = fopen(text, "w");
                fwrite(buffer, 512, 1, output);
                counter++;
            }
        }
        else if (counter != 0)
        {
            fwrite(buffer, 512, 1, output);
        }
    }
    fclose(input);
    fclose(output);
}