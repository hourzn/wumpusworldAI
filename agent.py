from imports import *
from tiles import *
from states import *
from grid import *
from map import *


# helper functions
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

class agent:
<<<<<<< HEAD
	# put agent in a random location on the edge of the grid where there is no pit and no gold
	def __init__(self, grid):
		self.map = Map(grid)
		self.location = set_start_position(self.map.N)
		self.map.matrix[self.location[0]][self.location[1]].has_agent = True
		self.map.matrix[self.location[0]][self.location[1]].observance = observances.VISITED
		self.facing = directions.RIGHT
		self.score = 0
		self.moves = 0
		self.percepts = [False for i in range(percept_index.N_STATES)]
		self.arrow = True
		self.gold = False
		self.wumpus_killed = False
		self.game_over = False
		self.won = False
		self.act = [self.turn_left, self.turn_right, self.move_forward, self.grab, self.release, self.shoot, self.climb]
		self.act_names = ["turn_left", "turn_right", "move_forward", "grab", "release", "shoot", "climb"]

	# display the agent's state and percepts on the console window
	def __str__(self):
		string = "------------------------------------------------------------\n"
		string += "Agent's location: " + str(self.location) + "\n"
		string += "Agent's facing direction: " + str(self.facing) + "\n"
		string += "Agent's score: " + str(self.score) + "\n"
		string += "Agent's moves: " + str(self.moves) + "\n"
		string += "Agent's percepts: " + str(self.percepts) + "\n"
		string += "Wumpus killed: " + str(self.wumpus_killed) + "\n"
		string += "------------------------------------------------------------"
		string += str(self.map)
		string += "------------------------------------------------------------"
		return string

    # turn the agent 90 degrees to the left
	def turn_left(self):
		self.facing = self.facing - 1
		if (self.facing < directions.RIGHT):
			self.facing = directions.UP
		self.moves += 1
		print("Agent has turned left!")

	# turn the agent 90 degrees to the right
	def turn_right(self):
		self.facing = self.facing + 1
		if (self.facing > directions.UP):
			self.facing = directions.RIGHT
		self.moves += 1
		print("Agent has turned right!")

	# move the agent forward
	def move_forward(self, grid):
		(i, j) = get_adjacent_position(self.location[0], self.location[1], self.facing)
		if (not valid_location(i, j, self.map.N, self.map.M)):
			#self.map.matrix.percepts[percept_index.BUMP] = True
			print("\nYou bumped into a wall!")
		else:
			print("\nAgent has moved forward!")

			# update has_agent
			self.map.matrix[self.location[0]][self.location[1]].has_agent = False
			self.map.matrix[i][j].has_agent = True

			# update state to VISITED if OBSERVED
			if (self.map.matrix[i][j].observance == observances.OBSERVED):
				self.map.matrix[i][j].observance = observances.VISITED
			## remove from Observed list

			self.location = (i, j)
			self.moves += 1
			self.update_percepts(grid)

	# display actions agent can take
	def display_actions(self, grid):
		print("Actions:")
		for i in range(len(self.act)):
			print(str(i) + ": " + self.act_names[i])
		# get user input
		action = int(input("Enter action: "))
		if action == 0:
			self.turn_left()
		elif action == 1:
			self.turn_right()
		elif action == 2:
			self.move_forward(grid)
		elif action == 3:
			self.grab(grid)
		elif action == 4:
			self.release(grid)
		elif action == 5:
			self.shoot(grid)
		elif action == 6:
			self.climb(grid)
		else:
			print("Invalid action!")

	# grab gold if possible
	# if the agent grabs gold in the tile with gold display a message
	def grab(self, grid):
		if grid.matrix[self.location[0]][self.location[1]].states[state_index.GOLD]:
			grid.matrix[self.location[0]][self.location[1]].states[state_index.GOLD] = False
			self.gold = True
			#self.score += 1000 leaving cave with gold does score.
			print("You got the gold!")
		else:
			print("There is no gold to grab!")
		self.moves += 1

	def release(self, grid):
		if self.gold:
			grid.matrix[self.location[0]][self.location[1]].states[state_index.GOLD] = True
			self.gold = False
			print("You released the gold from your grasp.")
		else:
			print("You have no gold to release!")
		self.moves += 1

	# shoot the arrow
	def shoot(self, grid):
		if not self.arrow:
			print("You don't have any more arrows left!\n")
			return
		self.arrow = False
		self.moves += 1

		# if the agent shoots the arrow in the tile with the wumpus display a message
		arrow_position = self.location
		while (valid_location(arrow_position[0], arrow_position[1], self.map.N, self.map.M)):
			if grid.matrix[arrow_position[0]][arrow_position[1]].states[state_index.WUMPUS]:
				self.wumpus_killed = True
				self.score += 1000
				print("You killed the wumpus!")
				## make the scream percept audible
			arrow_position = get_adjacent_position(arrow_position[0], arrow_position[1], self.facing)
		if (not valid_location(arrow_position[0], arrow_position[1],self.map.N, self.map.M)):
			print("The arrow hit a wall...\n")
	# exit the cave
	def climb(self, grid):
		if self.gold:
			self.score += 1000
		# if agent is at start location and has gold, then agent wins the game after climbing
		if self.location == grid.START_POSITION:
			self.won = True
			self.game_over = True
			print('Agent has exited the cave successfully!')
=======
    def __init__(self, grid):
        self.matrix = grid.matrix
        self.N = grid.N
        self.M = grid.M
        self.location = (0,0)
        self.facing = directions.RIGHT
        self.score = 0
        self.moves = 0
        self.percepts = [False for i in range(percept_index.N_STATES)]
        self.arrow = True
        self.gold = False
        self.wumpus_killed = False
        self.game_over = False
        self.won = False
        self.act = [self.turn_left, self.turn_right, self.move_forward, self.grab, self.shoot, self.climb]
        self.act_names = ["turn_left", "turn_right", "move_forward", "grab", "shoot", "climb"]

    # display the agent's state and percepts on the console window
    def __str__(self):
        string = "------------------------------------------------------------\n"
        string += "Agent's location: " + str(self.location) + "\n"
        string += "Agent's facing direction: " + str(self.facing) + "\n"
        string += "Agent's score: " + str(self.score) + "\n"
        string += "Agent's moves: " + str(self.moves) + "\n"
        string += "                  breeze, stench, glitter, bump, scream\n"
        string += "Agent's percepts: " + str(self.percepts) + "\n"
        string += "Wumpus killed: " + str(self.wumpus_killed) + "\n"
        string += "------------------------------------------------------------"
        return string

    # turn the agent 90 degrees to the left
    def turn_left(self):
        if self.facing == directions.RIGHT:
            self.facing = directions.UP
        elif self.facing == directions.DOWN:
            self.facing = directions.RIGHT
        elif self.facing == directions.LEFT:
            self.facing = directions.DOWN
        elif self.facing == directions.UP:
            self.facing = directions.LEFT
        self.moves += 1
        print("\nAgent has turned left!")

    # turn the agent 90 degrees to the right
    def turn_right(self):
        if self.facing == directions.RIGHT:
            self.facing = directions.DOWN
        elif self.facing == directions.DOWN:
            self.facing = directions.LEFT
        elif self.facing == directions.LEFT:
            self.facing = directions.UP
        elif self.facing == directions.UP:
            self.facing = directions.RIGHT
        self.moves += 1
        print("\nAgent has turned right!")

    # move the agent forward
    # check if valid position based on facing direction, if position is invalid, then agent hits bumps percept
    def move_forward(self):
        # set the agent's previous location to visited
        (i, j) = self.location
        self.matrix[i][j].states[observances.VISITED] = True
        if self.facing == directions.RIGHT:
            if j + 1 < self.M:
                self.location = (i, j + 1)
                print("\nAgent has moved forward!")
            else:
                self.percepts[percept_index.BUMP] = True
                print("Agent has hit a wall!")
        elif self.facing == directions.DOWN:
            if i + 1 < self.N:
                self.location = (i + 1, j)
                print("\nAgent has moved forward!")
            else:
                self.percepts[percept_index.BUMP] = True
                print("Agent has hit a wall!")
        elif self.facing == directions.LEFT:
            if j - 1 >= 0:
                self.location = (i, j - 1)
                print("\nAgent has moved forward!")
            else:
                self.percepts[percept_index.BUMP] = True
                print("Agent has hit a wall!")
        elif self.facing == directions.UP:
            if i - 1 >= 0:
                self.location = (i - 1, j)
                print("\nAgent has moved forward!")
            else:
                self.percepts[percept_index.BUMP] = True
                print("Agent has hit a wall!")
        self.moves += 1
        # update the agent's percepts
        self.update_percepts()

  
    # check ig agent is on a tile with a pit
    def check_pit(self):
        (i, j) = self.location
        if self.matrix[i][j].states[state_index.PIT]:
            print("Agent has fallen into a pit!")
            self.game_over = True
            exit("Game over!")

        
    # display actions agent can take
    def display_actions(self):
        print("Actions:")
        for i in range(len(self.act)):
            print(str(i) + ": " + self.act_names[i])
        # get user input
        action = int(input("Enter action: "))
        if action == 0:
            self.turn_left()
        elif action == 1:
            self.turn_right()
        elif action == 2:
            self.move_forward()
        elif action == 3:
            self.grab()
        elif action == 4:
            self.shoot()
        elif action == 5:
            self.climb()
        else:
            print("Invalid action!")

    # grab gold if agent is on a tile with glitter percept
    def grab(self):
        (i, j) = self.location

        # check if agent is on a tile with glitter percept
        if self.matrix[i][j].states[percept_index.GLITTER]:
            self.gold = True
            self.score += 1
            self.moves += 1
            print("Agent has grabbed the gold!")
        else:
            print("There is no gold here!")

    # shoot the arrow
    # arrow flys until hits a wall or kills wumpus
    def shoot(self):
        (i, j) = self.location
        if self.arrow:
            # shoot the arrow until it hits a wall or kills the wumpus
            while True:
                # move the arrow forward
                if self.facing == directions.RIGHT:
                    if j + 1 < self.M:
                        self.location = (i, j + 1)
                    else:
                        print("Arrow has hit a wall!")
                        break
                elif self.facing == directions.DOWN:
                    if i + 1 < self.N:
                        self.location = (i + 1, j)
                    else:
                        print("Arrow has hit a wall!")
                        break
                elif self.facing == directions.LEFT:
                    if j - 1 >= 0:
                        self.location = (i, j - 1)
                    else:
                        print("Arrow has hit a wall!")
                        break
                elif self.facing == directions.UP:
                    if i - 1 >= 0:
                        self.location = (i - 1, j)
                    else:
                        print("Arrow has hit a wall!")
                        break
                # check if arrow has killed the wumpus
                (i, j) = self.location
                if self.matrix[i][j].states[state_index.WUMPUS]:
                    print("Arrow has killed the wumpus!")
                    self.wumpus_killed = True
                    break
            self.arrow = False
            self.moves += 1
        else:
            print("Agent has no more arrows!")

    # exit the cave
    def climb(self):
        (i, j) = self.location
        if self.matrix[i][j].states[state_index.START]:
            self.score -= 1
        self.moves += 1
        # if agent is at start location and has gold, then agent wins the game after climbing
        if self.matrix[i][j].states[state_index.START] and self.gold:
            self.won = True
        self.game_over = True
        print('Agent has exited the cave successfully!')
>>>>>>> f661f3397a837a16c9522c704adbb8c9d74093fe

	# get the agent's state
	def get_state(self):
		return (self.location, self.facing)

<<<<<<< HEAD
	# update the agent's percepts
	def update_percepts(self, grid):
		(i, j) = self.location
		for direction in range(directions.N_STATES):
			# check if Tile in that location is valid
			(adj_i, adj_j) = get_adjacent_position(i, j, direction)
			if (not valid_location(adj_i, adj_j, self.map.N, self.map.M)):
				continue
			# check contents of Tile
			if (grid.matrix[adj_i][adj_j].states[state_index.PIT]):
				self.map.matrix[i][j].percepts[percept_index.BREEZE] = True
			if (grid.matrix[adj_i][adj_j].states[state_index.WUMPUS]):
				self.map.matrix[i][j].percepts[percept_index.STENCH] = True
			if (grid.matrix[adj_i][adj_j].states[state_index.GOLD]):
				self.map.matrix[i][j].percepts[percept_index.GLITTER] = True

			# update obsevance state
			if self.map.matrix[adj_i][adj_j].observance == observances.UNKNOWN:
				self.map.matrix[adj_i][adj_j].observance = observances.OBSERVED
				# add to Observed

	# get the percept index
	def get_percept_index(self):
		index = 0
		for i in range(percept_index.N_STATES):
			if self.percepts[i]:
				index += 2 << i
		return index

	# get the state index
	def get_state_index(self):
		(i, j) = self.location
		index = 0
		for k in range(state_index.N_STATES):
			if self.map.matrix[i][j].states[k]:
				index += 2 << k
		return index
=======
    # update the agent's percepts
    def update_percepts(self):
        (i, j) = self.location
        self.percepts = [False for i in range(percept_index.N_STATES)]
        if self.matrix[i][j].states[state_index.WUMPUS]:
            self.percepts[percept_index.STENCH] = True
        if self.matrix[i][j].states[state_index.PIT]:
            self.percepts[percept_index.BREEZE] = True
        if self.matrix[i][j].states[state_index.GOLD]:
            self.percepts[percept_index.GLITTER] = True
        if self.matrix[i][j].states[state_index.START]:
            self.percepts[percept_index.BUMP] = True
    
>>>>>>> f661f3397a837a16c9522c704adbb8c9d74093fe

