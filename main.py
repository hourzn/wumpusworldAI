from imports import *
from grid import *
from states import *
from tiles import *
from agent import *
from wumpus import *


# wumpus world class where our game is played
class wumpus_world:
    def __init__(self, N=4, M=4, p_pit=0.2, n_wumpus=1, n_gold=1):
        self.grid = Grid(N, M, p_pit, n_wumpus, n_gold)
        self.wumpus = wumpus(self.grid)
        self.agent = agent(self.grid)
        self.game_over = False
        self.won = False
        self.agent.update_percepts(self.grid)

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
            # update the agent's percepts
            self.agent.update_percepts(self.grid)
            self.game_over = self.agent.game_over
            self.won = self.agent.won
            print(self.agent.__str__())
            print("\nWumpus location: ", self.wumpus.location)
            print("Agent location: ", self.agent.location)
            # print("Agent has arrow: ", self.agent.arrow)
            # print("Agent has gold: ", self.agent.gold)
            # print("Wumpus is alive: ", self.wumpus.alive)
            print(self)
            print(self.grid.matrix[self.agent.location[0]]
                  [self.agent.location[1]])
            # display agent actions from agent class
            self.agent.display_actions(self.grid)
            if (self.agent.game_over or self.agent.won):
                break
            # if agent is in the same location as the wumpus, the game is over
            if (self.agent.location == self.wumpus.location and not self.agent.wumpus_killed):
                self.game_over = True
                self.won = False
                print("You have been eaten by the wumpus!")
            if (self.grid.matrix[self.agent.location[0]][self.agent.location[1]].states[state_index.PIT]):
                self.game_over = True
                self.won = False
                print("You have fallen into a pit!")


if __name__ == "__main__":
    game = wumpus_world()
    game.play()
