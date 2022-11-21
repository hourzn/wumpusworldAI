from imports import *
from grid import *
from states import *

# this is the implementation file for the Map component class for the Agent class. The Map is composed of Tiles.
# these Tiles are NOT the same as the Grid Tiles, as what they keep track of is different.
# The Grid is used for the Agent to interact with the environment. It is the world.
# The Map is what the Agent uses to do reasoning and make decisions.


def str_indices(M):
	s = ""
	for i in range(M):
		s += (6 * " ") + str(i) + (6 * " ")
	s += "\n"
	return s

class MTile:
	def __init__(self, i, j):
		self.location = (i, j)
		self.observance = observances.UNKNOWN
		self.percepts = [False for i in range(percept_index.N_STATES)]
		self.marks = [False for i in range(state_index.N_STATES)]
		self.safe = False
		self.has_agent = False

	def __str__(self):
		(b, s, gl) = (self.percepts[percept_index.BREEZE], self.percepts[percept_index.STENCH], self.percepts[percept_index.GLITTER])
		(b, s, gl) = (bool_to_intch(b), bool_to_intch(s), bool_to_intch(gl))
		(p, w, g) = (self.marks[state_index.PIT],self.marks[state_index.WUMPUS], self.marks[state_index.GOLD])
		(p, w, g) = (bool_to_intch(p), bool_to_intch(w), bool_to_intch(g))
		agentch = "A" if self.has_agent else "~"
		obvs = ["V", "O", "U"]
		string = "|" + agentch + " " + obvs[self.observance] + " " + b + s + gl + " " + p + w + g + "| "
		return string


class Map:
	def __init__(self, grid):
		# making map
		self.N = grid.N
		self.M = grid.M
		self.matrix = [[MTile(i, j) for j in range(self.M)] for i in range(self.N)]

		# list to hold OBSERVED Tile locations
		self.observed = []

		# list to hold possibilities of PIT/WUMPUS/GOLD
		worlds = [[] for i in range(percept_index.BUMP)]

	def _str_grid(self):
		# string of grid
		# top indices
		s = ""
		s += str_indices(self.M)

		# Tiles
		for i in range(self.N):
			s += str(i)
			for j in range(self.M):
				s += str(self.matrix[i][j])
			s += "\n"

		# bottom indices
		s += str_indices(self.M)
		return s

	def _str_observed(self):
		s = ""
		s += "Observed:"
		for i in range(len(self.observed)):
			s += i + ": [" + str(observed[i]) + "]\t"
		s += "\n"
		return s

	def _str_worlds(self):
		s = ""
		s += "Worlds:\n"
		labels = ["Pit", "Wumpus", "Gold"]
		for i in range(len(labels)):
			s += labels[i]
			for j in range(len(labels[i])):
				s += labels[i]
			s += "\n"
		return s

	def __str__(self):
		string = "\nCurrent map:\n"
		string += self._str_grid()
		string += self._str_observed()
		#string += self._str_worlds() # buggy
		return string
