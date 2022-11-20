from imports import *
from grid import *
from states import *
from tiles import *
from  agent import *
from wumpus import *


# wumpus world class where our game is played
class wumpus_world:
    def __init__(self, N = 4, M = 4, p_pit = 0.2, n_wumpus = 1, n_gold = 1):
        self.grid = Grid(N, M, p_pit, n_wumpus, n_gold)
        self.wumpus = wumpus(self.grid)
        self.agent = agent(self.grid)
        self.game_over = False
        self.won = False

        # place the agent where there is no wumpus or pit or gold
        (i, j) = (num(1, self.grid.N), num(1, self.grid.M))
        while (self.grid.matrix[i][j].states[state_index.PIT] or self.grid.matrix[i][j].states[state_index.WUMPUS] or self.grid.matrix[i][j].states[state_index.GOLD]):
            (i, j) = (num(1, self.grid.N), num(1, self.grid.M))
        self.agent.location = (i, j)



    # print the grid
    def __str__(self):
        string = ""
        for i in range(self.grid.N):
            for j in range(self.grid.M):
                string += str(self.grid.matrix[i][j])
            string += "\n"
        return string

    # play the game
    def play(self):
        while not self.game_over:
            self.game_over = self.agent.game_over
            self.won = self.agent.won
            print(self.agent.__str__())
            print("\nWumpus location: ", self.wumpus.location)
            print("Agent location: ", self.agent.location)
            print("Agent has arrow: ", self.agent.arrow)
            print("Agent has gold: ", self.agent.gold)
            print("Wumpus is alive: ", self.wumpus.alive)
            print(self)
            # display agent actions from agent class
            self.agent.display_actions()
            # if agent is in the same location as the wumpus, the game is over
            if self.agent.location == self.wumpus.location:
                self.game_over = True
                self.won = False
                print("You have been eaten by the wumpus!")


if __name__ == "__main__":
    game = wumpus_world()
    game.play()
    