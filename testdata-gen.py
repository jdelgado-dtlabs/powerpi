#!/usr/bin/python3

import random

def generateData(start, end):
    rand = random.randrange(start, end)
    return rand

f = open("testdata.txt", "w+")

for l in range(90):
    data = ""
    for i in range(15):
        i += 1
        if i == 1 or i == 6 or i == 11:
            data += str(generateData(100, 250)) + " "
        if i == 2 or i == 7 or i == 12:
            data += str(generateData(100, 250)) + " "
        if i == 3 or i == 8 or i == 13:
            data += str(generateData(5000, 11000)) + " "
        if i == 4 or i == 9 or i == 14:
            data += str(generateData(100, 120)) + " "
        if i == 5 or i == 10 or i == 15:
            data += str(generateData(0, 1)) + " "

    f.write("%s\n" % (data))

f.close()
