from imports import *
from tiles import *
from states import *
from grid import *

class agent:
    # put agent in a random location on the edge of the grid where there is no pit and no gold
    def __init__(self, grid):
        self.matrix = grid.matrix
        self.N = grid.N
        self.M = grid.M
        self.location = (1, 1)
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
        string += "Agent's percepts: " + str(self.percepts) + "\n"
        string += "Wumpus killed: " + str(self.wumpus_killed) + "\n"
        string += "------------------------------------------------------------"
        return string

    # turn the agent 90 degrees to the left
    def turn_left(self):
        self.facing = (self.facing - 1) % directions.N_STATES
        self.moves += 1
        print("Agent has turned left!")
    # turn the agent 90 degrees to the right
    def turn_right(self):
        self.facing = (self.facing + 1) % directions.N_STATES
        self.moves += 1
        print("Agent has turned right!")

    # move the agent forward
    def move_forward(self):
        (i, j) = self.location
        if self.facing == directions.RIGHT:
            if j == self.M:
                self.percepts[percept_index.BUMP] = True
                print("\nYou bumped into a wall!")
            else:
                self.location = (i, j + 1)
                self.moves += 1
                print("\nAgent has moved forward!")

        elif self.facing == directions.DOWN:
            if i == self.N:
                self.percepts[percept_index.BUMP] = True
                print("\nYou bumped into a wall!")
            else:
                self.location = (i + 1, j)
                self.moves += 1
                print("\nAgent has moved forward!")

        elif self.facing == directions.LEFT:
            if j == 1:
                self.percepts[percept_index.BUMP] = True
                print("\nYou bumped into a wall!")
            else:
                self.location = (i, j - 1)
                self.moves += 1
                print("\nAgent has moved forward!")

        elif self.facing == directions.UP:
            if i == 1:
                self.percepts[percept_index.BUMP] = True
                print("\nYou bumped into a wall!")
            else:
                self.location = (i - 1, j)
                self.moves += 1
                print("\nAgent has moved forward!")
        

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



    # check if agent has arrow
    def has_arrow(self):
        if self.arrow:
            self.arrow = False
            return True
        return False
    
    # check if agent has gold
    def has_gold(self):
        if self.gold:
            self.gold = False
            return True
        return False

    # grab gold if possible
    # if the agent grabs gold in the tile with gold display a message
    def grab(self):
        if self.matrix[self.location[0]][self.location[1]].states[state_index.GOLD]:
            self.gold = True
            self.score += 1000
            print("You got the gold!")
        else:
            print("There is no gold to grab!")
        self.moves += 1

    # shoot the arrow
    def shoot(self):
        if self.arrow:
            self.arrow = False
            self.moves += 1
            # if the agent shoots the arrow in the tile with the wumpus display a message
            if self.matrix[self.location[0]][self.location[1]].states[state_index.WUMPUS]:
                self.wumpus_killed = True
                self.score += 1000
                print("You killed the wumpus!")
            else:
                print("You missed the wumpus!")
        else:
            print("You don't have an arrow!")
            
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

    # get the agent's state
    def get_state(self):
        return (self.location, self.facing)

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
    
    # get the percept index
    def get_percept_index(self):
        index = 0
        for i in range(percept_index.N_STATES):
            if self.percepts[i]:
                index += 2 ** i
        return index

    # get the state index
    def get_state_index(self):
        (i, j) = self.location
        index = 0
        for k in range(state_index.N_STATES):
            if self.matrix[i][j].states[k]:
                index += 2 ** k
        return index

