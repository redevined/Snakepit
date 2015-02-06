#!/usr/bin/env python

import sys

def main(food, me) :
    size = 11
    food = [int(i) for i in food.split(",")]
    me = [[int(i) for i in seg.split(",")] for seg in me.split("/")]
    v = [me[0][0] - me[1][0], me[0][1] - me[1][1]]

if __name__ == "__main__" :
    print main(*sys.argv[1:3])
