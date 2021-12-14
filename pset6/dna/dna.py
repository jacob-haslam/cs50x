import csv
import sys
import random


def main():

    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Read sequence into memory from file
    with open(sys.argv[2]) as f:
        sequence = f.read()
    # Define lists
    database = []
    headers = []
    match = []
    # Import database as list
    with open(sys.argv[1], 'r') as csvfile:
        csv.DictReader(csvfile)
        for row in csv.DictReader(csvfile):
            database.append(row)
    # Get headers from entry 1 of db
    headers = [*database[0].keys()]

    for i in range(len(headers)):
        match.append(str_search(headers[i], sequence))

    for row in database:
        currName = row['name']
        row['name'] = 0
        succCount = 0

        for i in range(len(headers)):

            if match[i] == int(row[headers[i]]):
                succCount += 1

            if succCount == len(headers):
                print(currName)
                exit(0)

    print("No match")


def str_search(strtosearch, sequence):
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