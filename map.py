from imports import *
from grid import *
from states import *

# this is the implementation file for the Map component class for the Agent class. The Map is composed of Tiles.
# these Tiles are NOT the same as the Grid Tiles, as what they keep track of is different.
# The Grid is used for the Agent to interact with the environment. It is the world.
# The Map is what the Agent uses to do reasoning and make decisions.


# helper functions for binary strings

# returns a binary string of unsigned integer n
def bstring(n):
	return str(bin(n))[2:]

# checks if bits indicated by indices from bstr is an element of generated
def entail(bstr, generated, indices):
	bits = ""
	for i in indices:
		bits += bstr[i]
	return bits in generated

# removes indicated bit from bstr
def remove(bstr, i):
	x = list(bstr)
	x.remove(x[i])
	return "".join(x)

# returns index list of elements in list x, given list y
# assumes y is a subset of x
def get_indices(x, y):
	l = [x.index(item) for item in y]
	return l

# generates possibile bits given the indices, the percept it is affecting, and the state of that percept
def generate_bits(indices, p_index, p_state):
	n = len(indices)
	r = {"".zfill(n)}
	#if (not p_state):
		#return r

	# if pit, then its all but all false
	g = []
	if (p_index <= state_index.PIT):
		g = [bstring(i).zfill(n) for i in range(1, 1<<n)]
	else:
	# otherwise only powers of 2
		g = [bstring((1<<i)).zfill(n) for i in range(n)]
	return g

# generates possible worlds the generated bits adhere to, given a length, generated bits, and indices
def generate_worlds(n, generated, indices, p_index):
	p = []
	# wumpus/gold only consider powers of 2
	if (p_index > state_index.PIT):
		numbers = [1<<i for i in range(n)]
	else:
		numbers = range(1<<n)
	for i in numbers:
		bstr = ""
		bstr = bstring(i).zfill(n)
		if (entail(bstr, generated, indices)):
			p.append(bstr)
	return p


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

		# list to hold OBSERVED Tile locations, list of 2-tuples
		self.observed = []

		# list to hold possibilities of PIT/WUMPUS/GOLD
		self.worlds = [[] for i in range(percept_index.BUMP)]

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
			s += str(i) + ": [" + str(self.observed[i]) + "]\t"
		s += "\n"
		return s

	def _str_worlds(self):
		s = ""
		s += "Worlds:\n"
		labels = ["Pit", "Wumpus", "Gold"]
		for i in range(len(labels)):
			s += labels[i] + ": "
			for j in range(len(self.worlds[i])):
				s += self.worlds[i][j] + " "
			s += "\n"
		return s

	def __str__(self):
		string = "\nCurrent map:\n"
		string += self._str_grid()
		string += self._str_observed()
		string += self._str_worlds() # buggy
		return string

	# returns (valid) adjacent strings that are observed
	def _adjacent_observed(self, i, j):
		adj = []
		for d in range(directions.N_STATES):
			(l, m) = get_adjacent_position(i, j, d)
			if (valid_location(l, m, self.N, self.M) and self.matrix[l][m].observance == observances.OBSERVED):
				adj.append((l, m))
		return adj

	# removes indicated item (Tile) from observed and the worlds it inhabits
	def remove_tile(self, item):
		# remove from observed
		i = self.observed.index(item)
		self.observed.remove(self.observed[i])

		# remove from worlds
		for j in range(len(self.worlds)):
			new_worlds = []
			new_worlds = list({remove(bstr, i) for bstr in self.worlds[j]})
			self.worlds[j] = new_worlds

	# adds Tile to observed and updates the worlds to accommodate its possibilities
	def add_tile(self, item):
		if item in self.observed:
			return

		self.observed.append(item)

		# this code is real nasty i know.
		for i in range (len(self.worlds)):
			w = []
			if (len(self.worlds[i]) <= 0):
				w = ["0", "1"]
			else:
				w = [bstr + bstring(j) for j in range(1<<1) for bstr in self.worlds[i]]
			self.worlds[i] = w
		print("added tile! new worlds: ", self.worlds[i])

	# updates the knowledge/possible models given a percept and current location
	def update_knowledge(self, percepts, i, j):
		# index mapping
		indices = get_indices(self.observed, self._adjacent_observed(i, j))

		# intersection!!
		for k in range(len(self.worlds)):
			new_worlds = []
			b = []
			g = []
			if (percepts[k] == False):
				new_worlds = ["".zfill(len(indices))]
			else:
				b = generate_bits(indices, k, percepts[k])
				g = generate_worlds(len(self.observed), b, indices, k)
			new_worlds = list(set(self.worlds[k]) & set(g))
			self.worlds[k] = new_worlds
			print("worlds for percept ", k, ":\t", self.worlds[k])
