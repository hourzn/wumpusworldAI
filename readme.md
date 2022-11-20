Going through the slides and textbook for information about the wumpus world, and trying to figure classes for implementation of the environment and the agent through classes.

ENVIRONMENT:

The wumpus is described as a series of caves, and each cave can have any of the following:

A pit
The wumpus
The gold
None of the above (Safe)

From this moment on, I’m going to call caves ‘Tiles’.

Though there are some caveats:
A pit and a wumpus can be in the same tile. The wumpus is too big to be affected by the pit.
The gold and a pit cannot be in the same tile, otherwise the agent would always die.
The wumpus can be in the same tile as the gold. This means that in order to step there safely, the wumpus must be dead.

Just like in the book/slides, the probability for a pit is the same for any tile other than the starting tile. That is a probability of 0.2.
This means there is no fixed amount of pits per matrix/grid of tiles.

P(pit) = 0.2

Also like the book, there will be only 1 Wumpus and 1 Gold. The probability of any of those is uniform based on the number of tiles in the grid/matrix.

P(wumpus) == P(gold) =1/((NxM) - 1) for a grid with N rows and M columns.

I was thinking of having a boolean list to hold these states for each tile, and those being integer enumerated for easier indexing.
(with Python, using IntEnum provides similar functionality to C/C++ enums, basically named constants. The same can be achieved really with constant variables).

I was thinking of the following names:
SAFE = 0
PIT = 1
WUMPUS = 2
GOLD = 3
N_STATES = 4

Based on the caveats discussed above, there are some states that are not possible for a single tile:

SAFE is true and any of the following states are also true.
PIT is true and GOLD is true.
PIT, WUMPUS, GOLD are true at once.

I was also considering of having a separate integer value for observance states:
VISITED = 0
OBSERVED = 1
UNKNOWN = 2
N_STATES = 3

VISITED means that the agent has been to that tile.
OBSERVED means that the agent has observed that tile and has an idea of what it may contain, though has not yet been to it.
UNKNOWN means that the agent does not know/have an inkling of an idea of what lies there and has not yet visited it.

Pseudocode of class implementation I had in mind: (this is not proper code, but it gets the idea across)
Class Tile:
Attributes:
Boolean list of Tile states
Integer value indicating observance state
Constructor: - set all boolean states to false
Set observance state to UNKNOWN

I plan to have its attributes public, because I had in mind to make it a component of the Grid class.

THE GRID:
The wumpus world consists of an NxM grid of caves. So I was planning to make a Grid class that encompasses that. In the textbook, it gives an example of a 4x4 environment, though that should not be a strict requirement.

In other words I plan to have a list of list of Tiles as a component of the Grid class. I plan to have it so that the Agent interacts with this Grid.

Grid Limits:
Based on the values passed into the constructor, the size of the Grid can change. These numbers of rows and columns will also be attributes of the class.

Knowing what is out of bounds is important for figuring out where the ‘walls’ are.

What makes a position invalid?
For any position i (row index), j (column index)

Position (i, j) is invalid if…
If i is nonpositive (< 0)
If i >= N (number of rows)
If j is nonpositive (< 0)
If j >= M (number of columns)

If any of these criteria are true, then the whole position is invalid.

I feel like implementing this as a (simple) function that is private to the Grid class.
def \_\_valid_tile(t): # t is a list of 2 elements. T[0] is the row, t[1] is the column
return (t[0] < 0 or t[0] >= self.N or t[1] < 0 or t[1] >= self.M)

This is what I had in mind for the implementation of the Grid (this is pseudocode):

Other important values:

1. wumpus probability
2. pit probability
3. gold probability

Class Grid:
Attributes:

-   N, for number of rows
-   M, for number of columns
-   Tile matrix (list of list of Tiles)
    Constructor(self, N, M, … maybe other values not sure yet…)
    Set self.N
    Set self.M
    Construct matrix based on N and M (initialize Tiles)
    Populate the matrix
    Place the pits based on probability
    Place the wumpus
    Place the gold

THE AGENT:
Both Tile and the Grid are rather simple classes, the Agent will be the object that will be interacting with it.

From the textbook:
The agent is placed in the bottom left corner (row N - 1, column 0) and faces to the right.

Because of this, there should be a constant/tuple to indicate START_POSITION.
There should also be an enumeration for the agent’s facing direction:

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
N_DIRECTIONS = 4

Actions:
Based on the slides, the Agent can do the following actions:

    Forward:
    	Given the current facing direction, go to the next square according to that direction.
    So a new position based on the facing direction.
    If the resulting position is invalid, then the Agent does not move and instead a Bump is audible (perceived)

For current position i, j:
RIGHT: i, j + 1 (column++)
DOWN: i - 1, j (row - -)
LEFT: i, j - 1 (column - -)
UP: i + 1, j (row++)

TurnLeft:
Turns agent to the left by 90 degrees:

ex)
TurnLeft(LEFT) gives a new facing direction of DOWN
TurnLeft(DOWN) gives a new facing direction of RIGHT
TurnLeft(RIGHT) gives a new facing direction of UP
TurnLeft(UP) gives a new facing direction of LEFT
TurnRight:
Turns agent to the right by 90 degrees.

ex)
TurnRight(LEFT) gives a new facing direction of UP
TurnRight(UP) gives a new facing direction of RIGHT
TurnRight(RIGHT) gives a new facing direction of DOWN
TurnRight(DOWN) gives a new facing direction of of LEFT

For both of these functions, I found it best to implement them similarly with the enumeration.
TurnRight increments facing direction by 1
TurnLeft decrements facing direction by 1
If the facing direction is nonpositive, then set the facing direction to UP
If the facing direction is greater than or equal to the number of directions, then set the facing direction to RIGHT

Grab:
If the agent is in the same tile as a tile that contains the Gold, then the Agent can grab it and hold on to it, removing the gold from the Tile.

    In this case, it is best for the Agent to have an has_gold attribute that is a boolean value, and that it needs to interact with the grid through the agent’s current position.

    In pseudocode:
    self.has_gold = true
    Grid.matrix[self.pos.x][self.pos.y].states[GOLD] = false

Release:
If the agent is currently holding the gold, then it can be released at the current tile the Agent lies. The Agent will no longer hold the Gold, and the Tile will now have the Gold.

    In Pseudocode:
    self.has_gold = false
    Grid.matrix[self.pos.x][self.pos.y].states[GOLD] = true

Shoot:
If there is still an arrow in use, then the Agent can shoot an arrow in the facing direction.
The arrow will fly through the Tiles until:
It hits a wall (position becomes invalid)
It hits the wumpus (lies at that position)

    If the arrow hits the wumpus, then the wumpus dies. Once the wumpus dies, its scream can be heard everywhere until the Agent takes another step.
    After being shot, there are no other arrows.

I think that there should be a boolean attribute of has_arrow, that is by default set to true since the arrow can only be used once. Once used, this attribute is set to false.

There should also be maybe a status for the wumpus. That might mean that a Wumpus class to be implemented, with one of the attributes being whether it is alive or not.

Climb:
Agent is able to exit the cave if its position is also the START_POSITION

PERCEPTS:
The agent will be able to perceive at any (valid) adjacent tiles by looking around (iterating through directions enumeration).
There will be percepts for each Tile. It is a list of boolean values:
BREEZE = 0
STENCH = 1
GLITTER = 2
BUMP = 3
SCREAM = 4
N_PERCEPTS = 5
By default they are set to false.

I am not sure of how to really implement this, whether to have it be part of the grid itself, or for the Agent to have its own grid to do its reasoning.

There are 5 percepts:

Breeze:
Any valid adjacent tile contains a PIT state set to true
Stench:
A valid adjacent tile contains a WUMPUS state set to true
Glitter:
A valid adjacent tile contains a GOLD state set to true.
Bump:
Agent attempts to move forward to an invalid position.
Scream:
The shot arrow hits the wumpus.

Possible class pseudocode for the Agent:

Class Agent:
Attributes:
2 element list for position
Current facing direction(integer)
has_arrow (boolean)
has_gold (boolean)
(MAYBE) copy of Grid for reasoning, like a map!
Constructor: - set position to START_POSITION

-   set facing direction to RIGHT
-   set has_arrow to true
-   set has_gold to false
-   (MAYBE) construct map
    Methods:
    Forward(Grid)
    TurnLeft()
    TurnRight()
    Grab(Grid)
    Release(Grid)
    Shoot(Grid)
    Climb()

Other helpful functions maybe:

look_around(Grid):
Goes through the directions in a loop to get percepts checking the Grid states from valid tiles.
