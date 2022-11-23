from imports import *
from tiles import *
from states import *
from grid import *

class agent:
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
    

