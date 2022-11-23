from imports import *
from states import *

# wumpus class

class wumpus:
	# put wumpus in a random location where there is no pit and no gold
	def __init__(self, grid):
<<<<<<< HEAD
		# given the grid, find the indices and place wumpus there.
		self.location = grid.loc_wumpus[0]
		self.alive = True

	# WUMPUS IS STATIC
=======
		(i, j) = (num(0, grid.N), num(0, grid.M))
		while (grid.matrix[i][j].states[state_index.PIT] or grid.matrix[i][j].states[state_index.GOLD]):
			(i, j) = (num(0, grid.N), num(0, grid.M))
		self.location = (i, j)
		self.alive = True
		self.grid = grid
		# set adjacent tiles to stench
		(i, j) = self.location
		if i > 0:
			grid.matrix[i - 1][j].states[percept_index.STENCH] = True
		if i < grid.N - 1:
			grid.matrix[i + 1][j].states[percept_index.STENCH] = True
		if j > 0:
			grid.matrix[i][j - 1].states[percept_index.STENCH] = True
		if j < grid.M - 1:
			grid.matrix[i][j + 1].states[percept_index.STENCH] = True


	# move the wumpus to a random location where there is no pit and no gold
	def move(self):
		(i, j) = (num(0, self.grid.N), num(0, self.grid.M))
		while (self.grid.matrix[i][j].states[state_index.PIT] or self.grid.matrix[i][j].states[state_index.GOLD]):
			(i, j) = (num(0, self.grid.N), num(0, self.grid.M))
		self.location = (i, j)
>>>>>>> f661f3397a837a16c9522c704adbb8c9d74093fe

	# kill the wumpus
	def kill(self):
		self.alive = False

	# check if the wumpus is alive
	def is_alive(self):
		return self.alive

	# check if the wumpus is at a location
	def is_at(self, location):
		return self.location == location
