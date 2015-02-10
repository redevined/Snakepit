#!/usr/bin/env python

import sys, random

def main(food, me) :
    food = [int(i) for i in food.split(",")]
    me = [[int(i) for i in seg.split(",")] for seg in me.split("/")]
    head = me[0]
    v = [head[0] - me[1][0], head[1] - me[1][1]]

    if food[0] < head[0] :
        vn = [-1, 0]
    elif food[0] > head[0] :
        vn = [1, 0]
    elif food[0] == head[0] :
        if food[1] < head[1] :
            vn = [0, -1]
        elif food[1] > head[1] :
            vn = [0, 1]

    if v == vn :
        return "..."
    elif [-v[1], v[0]] == vn :
        return "R"
    elif [v[1], -v[0]] == vn :
        return "L"
    else :
        return random.choice(("R", "L"))

if __name__ == "__main__" :
    print main(*sys.argv[1:3])
