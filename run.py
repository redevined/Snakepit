#!/usr/bin/env python

import os, itertools, time
from snakepit import Snake, Pit


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


@timer
def run(sns, n) :
    for i in range(1, n + 1) :
        game, winner = Pit(sns), None
        for winner in game.run(animate = i) :
            winner.score += 1
        print "Finished round #{0} of {1.name} vs. {2.name}, ".format(i, *sns) + ("{0} won.".format(winner.name) if winner else "draw.")


@timer
def main(rounds) :
    with open(os.path.join("snakes", "list.txt")) as botlist :
        snakes = [Snake(*line.strip().split(" ")) for line in botlist]

    for sns in itertools.combinations(snakes, 2) :
        run(sns, rounds)

    with open("scoreboard.md", "w") as scoreboard :
        scoreboard.writelines(getScoreboard(snakes))


if __name__ == '__main__' :
    main(5)
