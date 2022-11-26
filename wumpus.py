from imports import *
from states import *

# wumpus class

class wumpus:
	# put wumpus in a random location where there is no pit and no gold
	def __init__(self, grid):
		# given the grid, find the indices and place wumpus there.
		self.location = grid.loc_wumpus[0]
		self.alive = True

	# WUMPUS IS STATIC

	# kill the wumpus
	def kill(self):
		self.alive = False

	# check if the wumpus is alive
	def is_alive(self):
		return self.alive

	# check if the wumpus is at a location
	def is_at(self, location):
		return self.location == location
