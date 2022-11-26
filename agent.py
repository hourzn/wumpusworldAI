from imports import *
from tiles import *
from states import *
from grid import *
from map import *


class agent:
	# put agent in a random location on the edge of the grid where there is no pit and no gold
	def __init__(self, grid):
		self.map = Map(grid)
		self.location = set_start_position(self.map.N)
		self.start_position = self.location
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
		self.visited = [(3,0)]
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
			# self.map.matrix.percepts[percept_index.BUMP] = True
			print("\nYou bumped into a wall!")
		else:
			print("\nAgent has moved forward!")

			# update has_agent
			self.map.matrix[self.location[0]][self.location[1]].has_agent = False
			self.map.matrix[i][j].has_agent = True

			# update state to VISITED if OBSERVED
			if (self.map.matrix[i][j].observance == observances.OBSERVED):
				self.map.matrix[i][j].observance = observances.VISITED
				self.map.remove_tile((i, j))

			self.location = (i, j)
			self.moves += 1
			self.update_percepts(grid)
			self.map.update_knowledge(self.percepts, self.location[0], self.location[1])
			self.visited.append(self.location)

	# grab gold if possible
	# if the agent grabs gold in the tile with gold display a message
	def grab(self, grid):
		if grid.matrix[self.location[0]][self.location[1]].states[state_index.GOLD]:
			grid.matrix[self.location[0]][self.location[1]].states[state_index.GOLD] = False
			self.gold = True
			# self.score += 1000 leaving cave with gold does score.
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
		if (not valid_location(arrow_position[0], arrow_position[1], self.map.N, self.map.M)):
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

	# get the agent's state
	def get_state(self):
		return (self.location, self.facing)

	# update the agent's percepts
	def update_percepts(self, grid):
		(i, j) = self.location
		self.percepts = [False for i in range(percept_index.N_STATES)]
		for direction in range(directions.N_STATES):
			# check if Tile in that location is valid
			(adj_i, adj_j) = get_adjacent_position(i, j, direction)
			if (not valid_location(adj_i, adj_j, self.map.N, self.map.M)):
				continue
			# check contents of Tile
			if (grid.matrix[adj_i][adj_j].states[state_index.PIT]):
				self.map.matrix[i][j].percepts[percept_index.BREEZE] = True
				self.percepts[percept_index.BREEZE] = True
			if (grid.matrix[adj_i][adj_j].states[state_index.WUMPUS]):
				self.map.matrix[i][j].percepts[percept_index.STENCH] = True
				self.percepts[percept_index.STENCH] = True
			# if (grid.matrix[adj_i][adj_j].states[state_index.GOLD]):
			# 	self.map.matrix[i][j].percepts[percept_index.GLITTER] = True
			# 	self.percepts[percept_index.GLITTER] = True
			if (grid.matrix[i][j].states[state_index.GOLD]):
				self.map.matrix[i][j].percepts[percept_index.GLITTER] = True
				self.percepts[percept_index.GLITTER] = True

			# is it safe?
			if (self.map.matrix[i][j].is_safe()):
				self.map.matrix[adj_i][adj_j].safe = True
				self.map.safe_tiles.append((adj_i, adj_j))

			# update obsevance state
			if self.map.matrix[adj_i][adj_j].observance == observances.UNKNOWN:
				self.map.matrix[adj_i][adj_j].observance = observances.OBSERVED
				self.map.add_tile((adj_i, adj_j))

	# get the agent's best action based on the current state
	def get_action(self, grid):
		# check if agent has the gold
		if self.gold:
			# if agent is at start location with the gold, climb out of the cave
			if self.location == self.start_position:
				print("Agent is at start location with the gold, climbing out of the cave...")
				return self.climb(grid)
			# if agent is not at start location with the gold, move towards the start location using the map
			else:
				print(
					"Agent has the gold and is not at start location with the gold, moving towards the start location...")
				# move towards the start location
				last_location = self.location
				while (self.location != self.start_position):
					# print the adjacent tiles to the agent
					print("Adjacent tiles to the agent:")

					# get the adjacent tiles to the agent
					adjacent_tiles = self.get_adjacent_tiles(last_location)
					# print the adjacent tiles to the agent
					for tile in adjacent_tiles:
						if tile.location not in self.visited:
							print(tile.location)
						else:
							self.visited.pop()
							# turn towards the tile
							self.turn_towards_tile(tile)

							# move foward
							self.move_forward(grid)
							self.visited.pop()


					last_location = self.location
		# else if our agent does not have gold, use the map to find the gold by moving towards safe tiles
		else:
			last_location = self.location

			# move towards the safe tiles
			while (not self.gold):
				# gold percept
				if self.percepts[percept_index.GLITTER]:
					return self.grab(grid)
				# if agent does not have gold, move towards safe tiles
				if self.percepts[percept_index.STENCH]:
					self.shoot(grid)

				# print the adjacent tiles to the agent
				print("Adjacent tiles to the agent:")
				# get the adjacent tiles to the agent
				adjacent_tiles = self.get_adjacent_tiles(last_location)
				# print the adjacent tiles to the agent
				for tile in adjacent_tiles:
					print(tile.location)
					if tile.observance == observances.OBSERVED and tile.safe:
						# turn towards the tile if we are not facing it
						self.turn_towards_tile(tile)
						self.move_forward(grid)
						break
					# backtracking
					else:
						if tile.location not in self.visited:
							# turn towards the tile
							self.turn_towards_tile(tile)
							# move foward
							self.move_forward(grid)
							break



				last_location = self.location

	# get the adjacent tiles to the agent
	def get_adjacent_tiles(self, location):
		adjacent_tiles = []
		# get the adjacent tiles to the agent
		for i in range(-1, 2):
			for j in range(-1, 2):
				# check if adjacent tile is valid
				if (not valid_location(location[0] + i, location[1] + j, self.map.N, self.map.M)):
					continue
				# check if adjacent tile is diagonal
				if (i != 0 and j != 0):
					continue
				# check if adjacent tile is the agent's current location
				if (i == 0 and j == 0):
					continue
				# add adjacent tile to the list
				adjacent_tiles.append(self.map.matrix[location[0] + i][location[1] + j])
		return adjacent_tiles

	def turn_towards_tile(self, tile):
		# get the direction to the tile
		direction = self.get_direction_to_tile(tile)
		# while the agent is not facing the tile, turn left
		while (self.facing != direction):
			self.turn_left()

	def get_direction_to_tile(self, tile):
		# get the direction to the tile
		if (self.location[0] == tile.location[0]):
			if (self.location[1] < tile.location[1]):
				return directions.RIGHT
			else:
				return directions.LEFT
		else:
			if (self.location[0] < tile.location[0]):
				return directions.DOWN
			else:
				return directions.UP