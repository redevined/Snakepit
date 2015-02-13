#!/usr/bin/env python

import os, itertools
from snakepit import Snake, Pit


def getScoreboard(bots) :
    lm_name = max(map(len, [bot.name for bot in bots]))
    lm_master = max(map(len, [bot.master for bot in bots]))
    lm_score = max(map(len, [str(bot.score) for bot in bots]))
    lenmap = (("name", lm_name), ("master", lm_master), ("score", max(lm_score, 5)))

    yield "| {0} | {1} | {2} |\n".format(*[key.capitalize().center(val) for key, val in lenmap])
    yield "|-{0}-|-{1}-|-{2}-|\n".format(*["-" * val for key, val in lenmap])
    for bot in sorted(bots, key = lambda bot : bot.score, reverse = True) :
        yield "| {0} | {1} | {2} |\n".format(*[str(bot.__getattribute__(key)).ljust(val) for key, val in lenmap])


def main() :
    with open(os.path.join("snakes", "list.txt")) as botlist :
        snakes = [Snake(*line.strip().split(" ")) for line in botlist]

    for pitsize in range(10, 16) :
        for lenlimit in range(6, 11) :
            for sns in itertools.combinations(snakes, 2) :
                for r in range(10) :
                    game = Pit(sns, pitsize = pitsize, lenlimit = lenlimit, cyclimit = 100)
                    for winner in game.run(animate = False) :
                        winner.score += 1

            with open("scoreboard-{0}_{1}.txt".format(pitsize, lenlimit), "w") as scoreboard :
                scoreboard.writelines(getScoreboard(snakes))
            for snake in snakes :
                snake.score = 0


if __name__ == '__main__' :
    main()
