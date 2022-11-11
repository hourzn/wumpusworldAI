# class implementation file for the main classes involved in the wumpus environment
# Tiles, which make up the Grid
# The Grid, which the Agent interacts with
# The Agent, which performs actions and reasoning

from enum import IntEnum # python 3.4 or higher
import random # python 3.6 or higher


# some good functions
def num(start, end):
	return random.choice(range(start, end))

# important enumerations to have states/indices with meaningful names
# indices to access any particular state of a given Tile
class state_index(IntEnum):
	PIT = 0
	WUMPUS = 1
	GOLD = 2
	N_STATES = 3

# state variables for observance state of a given Tile
class observances(IntEnum):
	VISITED = 0
	OBSERVED = 1
	UNKNOWN = 2
	N_STATES = 3

# state variables for Agent's facing direction
class directions(IntEnum):
	RIGHT = 0
	DOWN = 1
	LEFT = 2
	UP = 3
	N_STATES = 4

# indices to access any particular percept
class percept_index(IntEnum):
	BREEZE = 0
	STENCH = 1
	GLITTER = 2
	BUMP = 3
	SCREAM = 4
	N_STATES = 5


# Tile class
# each Tile keeps track of what lies on them as well as observance state
def bool_to_intch(b):
	ch = '1'
	if b == False:
		ch = '0'
	return ch

class Tile:
	def __init__(self, p_pit = 0):
		self.states = [False for i in range(state_index.N_STATES)]
		# place pit (or not!)
		self.states[state_index.PIT] = random.choices([True, False], weights=(p_pit, 1 - p_pit), k = 1)[0]

	def __str__(self):
		(p, w, g) = (self.states[state_index.PIT], self.states[state_index.WUMPUS], self.states[state_index.GOLD])
		(p, w, g) = (bool_to_intch(p), bool_to_intch(w), bool_to_intch(g))
		string = "[" + p + w + g + "]\t"
		return string


# Grid class
# is composed of Tiles
class Grid:
	def __init__(self, N = 4, M = 4, p_pit = 0.2, n_wumpus = 1, n_gold = 1):
		# setting values
		self.N = N
		self.M = M
		self.p_pit = 0.2
		self.n_wumpus = 1
		self.n_gold = 1
		self.p_wumpus = self.n_wumpus * ((self.N * self.M) - 1)**-1
		self.p_gold = self.n_gold * ((self.N * self.M) - 1)**-1

		# setting up the grid
		self.matrix = [[Tile(self.p_pit) for i in range(M)] for i in range(M)]

		# populating grid
		# placing gold and wumpus
		for k in range(n_gold):
			(i, j) = (num(1, self.N), num(1, self.M))
			while (self.matrix[i][j].states[state_index.PIT] or self.matrix[i][j].states[state_index.GOLD]):
				(i, j) = (num(1, self.N), num(1, self.M))
			self.matrix[i][j].states[state_index.GOLD] = True

		for k in range(n_wumpus):
			(i, j) = (num(1, self.N), num(1, self.M))
			while (self.matrix[i][j].states[state_index.WUMPUS]):
				(i, j) = (num(1, self.N), num(1, self.M))
			self.matrix[i][j].states[state_index.WUMPUS] = True


	def __str__(self):
		string = ""
		for i in range(self.N):
			for j in range(self.M):
				string += str(self.matrix[i][j])
			string += "\n"
		return string
