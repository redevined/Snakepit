#!/usr/bin/env python

import sys, os, random
from subprocess import check_output

def debug(*args) :
	maxlen = max(len(str(arg)) for arg in args)
	print "#" * (maxlen + 4)
	for arg in args :
		print "# {} #".format(str(arg).ljust(maxlen))
	print "#" * (maxlen + 4)
	print


class Vector() :

	def __init__(self, x, y) :
		self.x, self.y = x, y

	def __add__(self, vec) :
		return self.__class__(self.x + vec.x, self.y + vec.y)

	def __sub__(self, vec) :
		return self.__class__(self.x - vec.x, self.y - vec.y)

	def __eq__(self, vec) :
		return self.x == vec.x and self.y == vec.y

	def __str__(self) :
		return "{},{}".format(self.x, self.y)

	def rotate(self, direction) :
		x, y = self.x, self.y
		self.x = -y if direction == "R" else y
		self.y = -x if direction == "L" else x


class Snake() :

	def __init__(self, inst, name, head, v) :
		self.pit = inst
		self.name = name
		with open(os.path.join("snakes", name, "cmd.txt")) as cmdfile :
			self.master, cmd = cmdfile.readlines()
			self.cmd = cmd.strip().split(" ")
		self.v = Vector(*v)
		self.segments = [Vector(*head), Vector(*head) - self.v, Vector(*head) - self.v - self.v]
		self.head = lambda : self.segments[0]

	def __contains__(self, vec) :
		for segment in self.segments :
			if vec == segment :
				return True
		return False

	def __str__(self) :
		return "/".join(str(seg) for seg in self.segments)

	def getMove(self) :
		move = check_output(self.cmd + [str(self.pit.food), str(self)]).strip()
		return move

	def isEating(self) :
		if self.head() == self.pit.food :
			self.pit.generateFood()
			return True

	def isAlive(self) :
		crashed = self.head() in self.pit.getSnake(self.name, other = True)
		escaped = self.head() not in self.pit
		return not (crashed or escaped)

	def update(self) :
		move = self.getMove().upper()
		if move in ("R", "L") :
			self.v.rotate(move)

		self.segments.insert(0, self.head() + self.v)
		if not self.isEating() :
			self.segments.pop()


class Pit() :

	def __init__(self, snakes) :
		self.size = 11
		setup = ((3, self.size // 2), (1, 0)), ((self.size - 4, self.size // 2), (-1, 0))
		self.snakes = [Snake(self, name, *start) for name, start in zip(snakes, setup)]
		self.generateFood()

	def __contains__ (self, vec) :
		xin = 0 < vec.x < self.size - 1
		yin = 0 < vec.y < self.size - 1
		return xin and yin

	def generateFood(self) :
		self.food = random.choice([
			Vector(x, y) for y in range(1, self.size - 1) for x in range(1, self.size - 1)
			if not any(Vector(x, y) in snake for snake in self.snakes)
		])

	def getSnake(self, name, other = False) :
		for snake in self.snakes :
			if (snake.name == name) != other :
				return snake

	def getString(self, name = None) : # deprecated
		snakes = [(self.getSnake(name), "x")] if name else zip(self.snakes, ("x", "o"))

		def getChar(x, y) :
			v = Vector(x, y)
			for snake, c in snakes :
				if v in snake :
					if v == snake.head() :
						return c.upper()
					return c
			if v == self.food :
				return "*"
			elif v in self :
				return "."
			else :
				return "#"

		return "\n".join(
			str().join(
				getChar(x, y) for x in range(self.size)
			) for y in range(self.size)
		)

	def run(self) :
		print self.getString() # debug
		while len(self.snakes) == 2 :
			for snake in self.snakes :
				snake.update()
			print self.getString() # debug
			self.snakes = [snake for snake in self.snakes if snake.isAlive()]

		return self.snakes


if __name__ == "__main__" :
	snakes = sys.argv[1:3]
	game = Pit(snakes)
	winner = game.run()
	print "The winner is {}!".format(winner[0].name) if winner else "Draw."
