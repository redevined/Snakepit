#!/usr/bin/env python

import sys, os, random
from subprocess import check_output
from animation import *


class CDContext() :

	def __init__(self, *paths) :
		self.path = os.path.join(*paths)

	def __enter__(self, *args) :
		oldpath = os.getcwd()
		os.chdir(self.path)
		self.path = oldpath

	def __exit__(self, *args) :
		os.chdir(self.path)


class Snake(object) :

	def __init__(self, name, master, *cmd) :
		self.name = name
		self.master = master
		self.cmd = cmd
		self.score = 0

	def init(self, inst, length, head, v) :
		self.pit = inst
		self.v = Vector(*v)
		self.segments = [Vector(*head) - self.v * i for i in range(length)]
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
		try :
			with CDContext("snakes", self.name) :
				move = check_output(self.cmd + (str(self.pit.food), str(self))).strip()
		except Exception as e :
			print "Exception occured while executing {0}: {1}".format(self.name, e)
			self.cmd = ("echo",)
			move = self.getMove()
		return move

	def isEating(self) :
		return self.head() == self.pit.food

	def isAlive(self, lenlimit, cycle, cyclimit) :
		other = self.pit.getSnake(self.name, other = True)
		crashed = (self.head() in self.segments[1:]) or (self.head() in other)
		escaped = self.head() not in self.pit
		starved = len(other) >= lenlimit or cycle > cyclimit
		return not (crashed or escaped or starved)

	def update(self) :
		move = self.getMove().upper()
		if move in ("R", "L") :
			self.v.rotate(move)

		self.segments.insert(0, self.head() + self.v)
		if not self.isEating() :
			self.segments.pop()


class Pit() :

	def __init__(self, snakes, pitsize = 15, lenstart = 3, lenlimit = 7, cyclimit = 200) :
		self.size = pitsize
		self.limit = lenlimit
		self.climit = cyclimit

		setup = ((lenstart, self.size // 2), (1, 0)), ((self.size - 1 - lenstart, self.size // 2), (-1, 0))
		for snake, vecs in zip(snakes, setup) :
			snake.init(self, lenstart, *vecs)

		self.snakes = snakes
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

	def run(self, animate = False, tick = 0.2) :
		frames = Animation(self, animate, tick) if animate else Fake()
		frames.renderFrame()

		while all(snake.isAlive(self.limit, len(frames), self.climit) for snake in self.snakes) :
			for snake in self.snakes :
				snake.update()
			if any(snake.isEating() for snake in self.snakes) :
				self.generateFood()
			frames.renderFrame()

		frames.renderFrame(4)
		frames.store("records")
		return [snake for snake in self.snakes if snake.isAlive(self.limit, len(frames), self.climit)]


if __name__ == "__main__" :
	snakes = sys.argv[1:3]
	with open(os.path.join("snakes", "list.txt")) as botlist :
		snakes = [Snake(*line.strip().split(" ")) for line in botlist if line.split(" ")[0] in snakes]
	winner = Pit(snakes).run()
	print "The winner is {0.name}!".format(*winner) if winner else "Draw."
