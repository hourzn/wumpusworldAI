from imports import *
from grid import *
from states import *
from tiles import *

# wumpus class

class wumpus:
	# put wumpus in a random location where there is no pit and no gold
	def __init__(self, grid):
		(i, j) = (num(1, grid.N), num(1, grid.M))
		while (grid.matrix[i][j].states[state_index.PIT] or grid.matrix[i][j].states[state_index.GOLD]):
			(i, j) = (num(1, grid.N), num(1, grid.M))
		self.location = (i, j)
		self.alive = True
		self.grid = grid

	# move the wumpus to a random location where there is no pit and no gold
	def move(self):
		(i, j) = (num(1, self.grid.N), num(1, self.grid.M))
		while (self.grid.matrix[i][j].states[state_index.PIT] or self.grid.matrix[i][j].states[state_index.GOLD]):
			(i, j) = (num(1, self.grid.N), num(1, self.grid.M))
		self.location = (i, j)

	# kill the wumpus
	def kill(self):
		self.alive = False
	
	# check if the wumpus is alive
	def is_alive(self):
		return self.alive

	# check if the wumpus is at a location
	def is_at(self, location):
		return self.location == location

	
