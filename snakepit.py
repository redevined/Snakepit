#!/usr/bin/env python

import sys, os, random
from subprocess import check_output
from animation import Vector, Animation


def debug(*args) :
	maxlen = max(len(str(arg)) for arg in args)
	print "#" * (maxlen + 4)
	for arg in args :
		print "# {0} #".format(str(arg).ljust(maxlen))
	print "#" * (maxlen + 4)
	print


class Snake() :

	def __init__(self, inst, name, head, v) :
		self.pit = inst
		self.name = name
		with open(os.path.join("snakes", name, "cmd.txt")) as cmdfile :
			self.master, cmd = cmdfile.readlines()
			self.cmd = cmd.strip().split(" ")
		self.v = Vector(*v)
		self.segments = [Vector(*head), Vector(*head) - self.v, Vector(*head) - self.v * 2]
		self.head = lambda : self.segments[0]

	def __contains__(self, vec) :
		for segment in self.segments :
			if vec == segment :
				return True
		return False

	def __len__(self) :
		return len(self.segments)

	def __str__(self) :
		return "/".join(str(seg) for seg in self.segments)

	def getMove(self) :
		move = check_output(self.cmd + [str(self.pit.food), str(self)]).strip()
		return move

	def isEating(self) :
		return self.head() == self.pit.food

	def isAlive(self) :
		other = self.pit.getSnake(self.name, other = True)
		crashed = (self.head() in self.segments[1:]) or (self.head() in other)
		escaped = self.head() not in self.pit
		starved = len(other) >= 10
		return not (crashed or escaped or starved)

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

	def run(self) :
		frames = Animation(self, 0.2)

		while len(self.snakes) == 2 :
			for snake in self.snakes :
				snake.update()
			if any(snake.isEating() for snake in self.snakes) :
				self.generateFood()

			frames.renderFrame()
			self.snakes = [snake for snake in self.snakes if snake.isAlive()]

		frames.store("records")
		return self.snakes


if __name__ == "__main__" :
	snakes = sys.argv[1:3]
	game = Pit(snakes)
	winner = game.run()
	print "The winner is {0.name}!".format(*winner) if winner else "Draw."
