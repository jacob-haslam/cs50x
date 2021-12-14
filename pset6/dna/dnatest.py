import csv
import sys
import random

def main():

    database = {}
    with open(sys.argv[1], 'r') as csvfile:
         csv.DictReader(csvfile)
         for row in csv.DictReader(csvfile):
             database.update(row)
    print(database)

def str_search(strtosearch,sequence):
    counter = 0
    strlen = len(strtosearch)

    for i in range(len(sequence)):
        temp = 0
        if sequence[i:i+strlen] == strtosearch:
            temp += 1
            x = 0
            while sequence[i+x+strlen:i+x+strlen*2] == strtosearch:
                temp += 1
                x += strlen
        if temp > counter:
            counter = temp
    return counter


main()
