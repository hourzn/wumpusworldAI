from imports import *
# important enumerations to have states/indices with meaningful names
# indices to access any particular state of a given Tile
class state_index(IntEnum):
    PIT = 0
    WUMPUS = 1
    GOLD = 2
    START = 3
    N_STATES = 4

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
