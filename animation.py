#!/usr/bin/env python

import sys, os, numpy
import gif
from PIL import Image


class Vector() :

    def __init__(self, x, y) :
        self.x, self.y = x, y

    def __add__(self, vec) :
        return self.__class__(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec) :
        return self.__class__(self.x - vec.x, self.y - vec.y)

    def __mul__(self, i) :
        return self.__class__(self.x * i, self.y * i)

    def __eq__(self, vec) :
        return self.x == vec.x and self.y == vec.y

    def __str__(self) :
        return "{0.x},{0.y}".format(self)

    def rotate(self, direction) :
        x, y = self.x, self.y
        self.x = -y if direction == "R" else y
        self.y = -x if direction == "L" else x


class Animation() :

    def __init__(self, inst, i, tick) :
        self.pit = inst
        self.filename = "{1.name}_vs_{2.name}.{0}.gif".format(i, *self.pit.snakes)
        self.duration = tick
        self.frames = []

    def __len__(self) :
        return len(self.frames)

    def getPixel(self, x, y) :
        v = Vector(x, y)
        if v == self.pit.snakes[0].head() :
            return (160, 0, 0)
        elif v == self.pit.snakes[1].head() :
            return (0, 140, 30)
        elif v in self.pit.snakes[0] :
            return (200, 0, 0)
        elif v in self.pit.snakes[1] :
            return (0, 160, 50)
        elif v == self.pit.food :
            return (70, 160, 255)
        elif v in self.pit :
            return (240, 240, 240)
        else :
            return (10, 10, 20)

    def renderFrame(self, n = 1) :
        for _ in range(n) :
            array = numpy.array(
                [[self.getPixel(x, y) for x in range(self.pit.size)] for y in range(self.pit.size)],
                dtype = "uint8"
            ).repeat(20, axis = 0).repeat(20, axis = 1)

            self.frames.append(Image.fromarray(array))

    def store(self, folder) :
        path = os.path.join(folder, self.filename)
        gif.writeGif(path, self.frames, duration = self.duration)


class Fake() :

    def __init__(self, *args) :
        self.counter = 0

    def __len__(self) :
        return self.counter

    def renderFrame(self, *args) :
        self.counter += 1

    def store(self, *args) :
        pass
