Food shortage in the Snakepit
=============================

For the first time in 35 years, the snakepit is running out of food. The inhabitant snakes now have to __fight__ each other in order to survive this food shortage. Only one snake can stand at the top of the food chain!

---

Leaderboard
-----------

_Not here yet!_

_Last update on February, 24th_

[Link to visualizations of last matches](https://github.com/redevined/Snakepit/tree/master/records)

---

Description
-----------

If you want to fight for the last remaining apples/cherries/whatever, you have to provide a snake in form of a program that accepts a given input and returns its next move.

The only twist is that you're not alone in your pit. Another snake will try to get the rare food too! But it's dark inside the snakepit so you can only see yourself and the apple. Crashing into your opponent will result in your death, just like biting yourself or hitting a wall. Additionally, because apples are rare these days, you starve if your opponent ate enough to reach a length of 7.

The snakepit is a two-dimensional map with a width and height of 15, while the outermost tiles build an impassable wall:

      0 1 2 . . . c d e
    0 # # # # # # # # #
    1 #               #
    2 #           x   #
    . #               #
    . #               #
    . #               #
    c #               #
    d #               #
    e # # # # # # # # #

Coordinates are zero-indexed, so the point where the `x` is would be `12,2`.

Your bot will be called with two arguments:
- The location of the food
- The locations of your body segments, separated by `/`

It should then write one of the following to stdout:
- `L` for a quarter left turn as its next move
- `R` for a quarter right turn
- Anything else for a move in the same direction

Example:

    Projects/Snakepit> python bot.py 12,2 4,8/4,9/3,9/2,9
    'R'
    Projects/Snakepit>

---

Rules
-----

Your bot is allowed to:
- Output anything, because anything is a valid move
- Read/write files in its own directory which is located under ./snakes/ThisIsYourSnake
- Run on Ubuntu 14.04 and Windows 7 (it actually has to)

Your bot must not:
- Read/write files outside its own directory
- Use external resources such as the internet
- Have a runtime above 10 seconds per execution

You have to provide in your answer:
- The source code of the bot
- A bot/snake name
- (Your own name)
- A command to run your bot

If you want to make my life easier, please provide a line like `CoolSnake MyOwnName python bot.py`.

---

Scoring
-------

Your snake gets a point for winning a game against another snake. A game is won under the following circumstances:
- Your opponent hits himself, you or a wall
- You reach length 7

Additionally, both snakes starve after 200 cycles.

Each snake will fight 10 matches for their survival against each other snake.

---

Example Bots
------------

Just to give you an idea, I'll provide these two (participating) example snakes:

__SneakySnake__

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

`SneakySnake Cipher python bot.py`

__ViciousViper__

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

`ViciousViper Cipher python bot.py`

And their matches:

![Example match 1](https://github.com/redevined/Snakepit/blob/master/records/example1.gif)
![Example match 2](https://github.com/redevined/Snakepit/blob/master/records/example2.gif)
![Example match 3](https://github.com/redevined/Snakepit/blob/master/records/example3.gif)

---

Control program
---------------

You can find the control program on [github](https://github.com/redevined/Snakepit), along with all bots and records of past matches.

_Documentation follows..._
