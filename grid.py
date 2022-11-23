from imports import *
from tiles import *
from wumpus import *

START_POSITION = (0, 0)

def set_start_position(N):
	return (N - 1, 0)

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


		# setting up the grid
		self.matrix = [[Tile(self.p_pit) for j in range(M)] for i in range(N)]

		# pits cannot be at START_POSITION
		(i, j) = self.START_POSITION
		if (self.matrix[i][j].states[state_index.PIT]):
			self.matrix[i][j].states[state_index.PIT] = False

		# populating grid
		# placing gold and wumpus
		for k in range(n_gold):
			(i, j) = (num(1, self.N), num(1, self.M))
			while (self.matrix[i][j].states[state_index.PIT] or self.matrix[i][j].states[state_index.GOLD]):
				(i, j) = (num(1, self.N), num(1, self.M))
			self.matrix[i][j].states[state_index.GOLD] = True
<<<<<<< HEAD
			self.loc_gold.append((i, j))
=======
			print ("Gold location: ", (i, j))
>>>>>>> f661f3397a837a16c9522c704adbb8c9d74093fe

		for k in range(n_wumpus):
			(i, j) = (num(1, self.N), num(1, self.M))
			while (self.matrix[i][j].states[state_index.WUMPUS]):
				(i, j) = (num(1, self.N), num(1, self.M))
			self.matrix[i][j].states[state_index.WUMPUS] = True
<<<<<<< HEAD
			self.loc_wumpus.append((i, j))

=======
			

            
>>>>>>> f661f3397a837a16c9522c704adbb8c9d74093fe
	def __str__(self):
		string = ""
		for i in range(self.N):
			for j in range(self.M):
				string += str(self.matrix[i][j])
			string += "\n"
		return string
