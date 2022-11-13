from imports import *
from states import *

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
