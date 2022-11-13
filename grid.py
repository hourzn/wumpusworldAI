from imports import *
from tiles import *
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