#!/usr/bin/env python

import sys, random

def main(food, me) :
    food = [int(i) for i in food.split(",")]
    me = [[int(i) for i in seg.split(",")] for seg in me.split("/")]
    head = me[0]
    v = [head[0] - me[1][0], head[1] - me[1][1]]
    vn = [food[0] - head[0], food[1] - head[1]]
    if 0 not in vn :
        vn[v.index(0)-1] = 0
    vn[vn.index(0)-1] = vn[vn.index(0)-1] / abs(vn[vn.index(0)-1])

    if v == vn :
        return "..."
    elif [v[0] + vn[0], v[1] + vn[1]] == [0, 0] :
        return random.choice(("R", "L"))
    else :
        return "R" if [-v[1], v[0]] == vn else "L"

if __name__ == "__main__" :
    print main(*sys.argv[1:3])
