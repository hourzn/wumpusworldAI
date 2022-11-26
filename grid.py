from imports import *
from tiles import *
from wumpus import *

START_POSITION = (0, 0)

# helper functions
def set_start_position(N):
	return (N - 1, 0)

def valid_index(k, N):
	return not(k < 0 or k >= N)

def valid_location(i, j, N, M):
	return valid_index(i, N) and valid_index(j, M)

def get_adjacent_position(i, j, facing):
	if (facing == directions.RIGHT):
		j += 1
	elif (facing == directions.DOWN):
		i += 1
	elif (facing == directions.LEFT):
		j -= 1
	elif (facing == directions.UP):
		i -= 1
	return (i, j)


# Grid class
# is composed of Tiles
class Grid:
	def __init__(self, N = 4, M = 4, p_pit = 0.2, n_wumpus = 1, n_gold = 1):
		# fixing constant
		self.START_POSITION = set_start_position(N)
		# setting values
		self.N = N
		self.M = M
		self.p_pit = 0.2
		self.n_wumpus = 1
		self.n_gold = 1
		self.p_wumpus = self.n_wumpus * ((self.N * self.M) - 1)**-1
		self.p_gold = self.n_gold * ((self.N * self.M) - 1)**-1
		self.loc_gold = []
		self.loc_wumpus = []
		self.impossible = False


		# setting up the grid
		self.matrix = [[Tile(self.p_pit) for j in range(M)] for i in range(N)]

		# pits cannot be at START_POSITION
		(i, j) = self.START_POSITION
		if (self.matrix[i][j].states[state_index.PIT]):
			self.matrix[i][j].states[state_index.PIT] = False

		# populating grid
		# placing gold and wumpus
		for k in range(n_gold):
			(i, j) = (num(0, self.N), num(0, self.M))
			while (self.matrix[i][j].states[state_index.PIT] or self.matrix[i][j].states[state_index.GOLD]):
				(i, j) = (num(0, self.N), num(0, self.M))
			self.matrix[i][j].states[state_index.GOLD] = True
			self.loc_gold.append((i, j))




		# the wumpus cannot be at the start position
		for k in range(n_wumpus):
			(i, j) = (num(0, self.N), num(0, self.M))
			while (self.matrix[i][j].states[state_index.WUMPUS] or (i, j) == self.START_POSITION):
				(i, j) = (num(0, self.N), num(0, self.M))
			self.matrix[i][j].states[state_index.WUMPUS] = True
			self.loc_wumpus.append((i, j))

	def __str__(self):
		string = ""
		for i in range(self.N):
			for j in range(self.M):
				string += str(self.matrix[i][j])
			string += "\n"
		return string

	# check grid for impossible states
	def check_impossible(self):
		# check if startiing position is surrounded by pits
		(i, j) = self.START_POSITION
		if self.matrix[3][1].states[state_index.PIT] and self.matrix[2][0].states[state_index.PIT]:
			self.impossible = True
			return
		# check if wumpus and gold are in the same location and surrounded by pits
		for (i, j) in self.loc_wumpus:
			if self.matrix[i][j].states[state_index.GOLD]:
				if (valid_location(i + 1, j, self.N, self.M) and self.matrix[i + 1][j].states[state_index.PIT]) and (valid_location(i - 1, j, self.N, self.M) and self.matrix[i - 1][j].states[state_index.PIT]) and (valid_location(i, j + 1, self.N, self.M) and self.matrix[i][j + 1].states[state_index.PIT]) and (valid_location(i, j - 1, self.N, self.M) and self.matrix[i][j - 1].states[state_index.PIT]):
					self.impossible = True
					return


