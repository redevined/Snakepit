#!/usr/bin/env python

import os, itertools, time
import argparse
from snakepit import Snake, Pit


def parseArguments() :
    parser = argparse.ArgumentParser(description = "Snakepit tournament control program")
    parser.add_argument("-n", help = "rounds of battles for each combination of opponents", type = int, default = 5)
    parser.add_argument("-s", help = "determines the size of the grid (width and height)", type = int, default = 15)
    parser.add_argument("-l", help = "sets the required length to win", type = int, default = 7)
    parser.add_argument("-c", help = "sets the limit of cycles", type = int, default = 200)
    parser.add_argument("-g", "--no-gifs", help = "creates no gifs of the matches", action = "store_true")
    return parser.parse_args()


def timer(func) :
    def wrapper(*args) :
        start = time.time()
        val = func(*args)
        end = time.time()
        print "=> {0}() took {1} seconds".format(func.__name__, int(end - start))
        return val
    wrapper.__name__ = func.__name__
    return wrapper


def getScoreboard(bots) :
    lenmap = [
        (attr, max(map(len, [str(bot.__getattribute__(attr)) for bot in bots]) + [5]))
        for attr in ("name", "master", "score")
    ]

    yield "| {0} | {1} | {2} |\n".format(*[key.capitalize().center(val) for key, val in lenmap])
    yield "|-{0}-|-{1}-|-{2}-|\n".format(*["-" * val for key, val in lenmap])
    for bot in sorted(bots, key = lambda bot : bot.score, reverse = True) :
        yield "| {0} | {1} | {2} |\n".format(*[str(bot.__getattribute__(key)).ljust(val) for key, val in lenmap])


# @timer
def run(sns, opts) :
    for i in range(1, opts.n + 1) :
        game, winner = Pit(sns, pitsize = opts.s, lenlimit = opts.l, cyclimit = opts.c), None
        for winner in game.run(animate = False if opts.no_gifs else i) :
            winner.score += 1
        print "Finished round #{0} of {1.name} vs. {2.name}, ".format(i, *sns) + ("{0} won.".format(winner.name) if winner else "draw.")


# @timer
def main(opts) :
    with open(os.path.join("snakes", "list.txt")) as botlist :
        snakes = [Snake(*line.strip().split(" ")) for line in botlist]

    for sns in itertools.combinations(snakes, 2) :
        run(sns, opts)

    with open("scoreboard.md", "w") as scoreboard :
        scoreboard.writelines(getScoreboard(snakes))


if __name__ == '__main__' :
    args = parseArguments()
    main(args)
