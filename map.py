from queue import PriorityQueue
from imports import *
from grid import *
from states import *

import numpy as np

# this is the implementation file for the Map component class for the Agent class. The Map is composed of Tiles.
# these Tiles are NOT the same as the Grid Tiles, as what they keep track of is different.
# The Grid is used for the Agent to interact with the environment. It is the world.
# The Map is what the Agent uses to do reasoning and make decisions.


# helper functions for binary strings
# returns a binary string of unsigned integer n
def bstring(n):
    return str(bin(n))[2:]

# returns decimal form of a binary string


def dec(bstr):
    return int(bstr, 2)

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

# determines whether a given binary string is a power of 2


def is_2power(bstr):
    powers = [1 << i for i in range(len(bstr))]
    n = dec(bstr)
    return n in powers

# partitions set of binary strings, based on a given bit's state


def bool_partition(A, i):
    part = [[] for i in range(True + 1)]
    for bstr in A:
        j = True if (bstr[i] == "1") else False
        part[j].append(bstr)
    return part

# returns index list of elements in list x, given list y
# assumes y is a subset of x


def get_indices(x, y):
    l = [x.index(item) for item in y]
    return l

# generates possibile bits given the indices, the percept it is affecting, and the state of that percept


def generate_bits(indices, p_index, p_state):
    n = len(indices)
    r = {"".zfill(n)}
    if (not p_state):
        return list(r)

    # if pit, then its all but all false
    g = []
    if (p_index <= state_index.PIT):
        g = [bstring(i).zfill(n) for i in range(1, 1 << n)]
    else:
        # otherwise only powers of 2
        g = [bstring((1 << i)).zfill(n) for i in range(n)]
    return list(g)

# generates possible worlds the generated bits adhere to, given a length, generated bits, and indices


def generate_worlds(n, generated, indices, p_index):
    p = []
    # wumpus/gold only consider powers of 2
    if (p_index > state_index.PIT):
        numbers = [0] + [1 << i for i in range(n)]
    else:
        numbers = range(1 << n)
    for i in numbers:
        bstr = ""
        bstr = bstring(i).zfill(n)
        if (entail(bstr, generated, indices)):
            p.append(bstr)
    return p

# returns list of non-zero world possibilities


def get_possibilities(worlds, n):
    zero = "".zfill(n)
    w = worlds
    if w in worlds:
        w.remove(zero)
    return w

# determines if there is only 1 possibility. if there is, then the string is returned (otherwise empty string)


def one_possibility(worlds):
    bstr = ""
    if (len(worlds) == 1 and is_2power(worlds[0])):
        bstr = worlds[0]
    return bstr

# normalizes a distribution


def normalize(dist):
    n = (sum(dist))**-1
    return list(n * np.array(dist))

# gets the probability of an event, given a bit string and associated probability


def product(bstr, p):
    prod = 1
    for bit in bstr:
        f = p if (bit == "1") else (1 - p)
        prod *= f
    return prod

# gets the sum of individual events, given a set of bit strings and probability


def sum_of_product(bstrs, p):
    sum = 0
    for bstr in bstrs:
        sum += (product(bstr, p))
    return sum

# gets the normalized probability distribution of a partitioned bit string set and probability


def distribution(part, p):
    dist = [sum_of_product(bstrs, p) for bstrs in part]
    return normalize(dist)

# performs a query, given sum list of unpartitioned binary strings, an index to partition by and a probability for a boolean event


def query(A, i, p):
    return distribution(bool_partition(A, i), p)

# returns most likely index, given unpartitioned binary strings and a probability, and indices to partition by


def most_likely_index(A, p, indices):
    max_q = [1, 0]
    maxdex = -1
    ties = []
    queries = []
    for i in indices:
        q = query(A, i, p)
        queries.append([q, i])
        if (q[True] > max_q[True]):
            maxdex = i
            max_q = q
    for q in queries:
        if (q[True] == max_q[True]):
            ties.append(q)
    return maxdex if not ties else break_tie(ties)

# breaks a tie of most likely values and returns a random index from the ties list


def break_tie(ties):
    rand_q = num(0, len(ties))
    return ties[rand_q][1]


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
        (b, s, gl) = (self.percepts[percept_index.BREEZE],
                      self.percepts[percept_index.STENCH], self.percepts[percept_index.GLITTER])
        (b, s, gl) = (bool_to_intch(b), bool_to_intch(s), bool_to_intch(gl))
        (p, w, g) = (self.marks[state_index.PIT],
                     self.marks[state_index.WUMPUS], self.marks[state_index.GOLD])
        (p, w, g) = (bool_to_intch(p), bool_to_intch(w), bool_to_intch(g))
        agentch = "A" if self.has_agent else "~"
        obvs = ["V", "O", "U"]
        string = "|" + agentch + " " + \
            obvs[self.observance] + " " + b + s + gl + " " + p + w + g + "| "
        return string

    # determines if a tile is safe or not
    def is_safe(self):
        has_pit = self.percepts[percept_index.BREEZE]
        has_wumpus = self.percepts[percept_index.STENCH]
        return (has_pit == False and has_wumpus == False)


class Map:
    def __init__(self, grid):
        # making map
        self.N = grid.N
        self.M = grid.M
        self.matrix = [[MTile(i, j) for j in range(self.M)]
                       for i in range(self.N)]

        # list to hold OBSERVED Tile locations, list of 2-tuples
        self.observed = []

        # list to hold possibilities of PIT/WUMPUS/GOLD
        self.worlds = [[] for i in range(percept_index.BUMP)]

        # list to hold SAFE Tiles
        self.safe_tiles = []

        self.probs = [0 for i in range(state_index.N_STATES)]
        self.probs[state_index.PIT] = grid.p_pit
        self.probs[state_index.WUMPUS] = grid.p_wumpus
        self.probs[state_index.GOLD] = grid.p_gold

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

    def _str_safe(self):
        s = "Safe tiles: "
        # remove all duplicates in safe_tiles
        self.safe_tiles = list(set(self.safe_tiles))

        for tile in self.safe_tiles:
            s += str(tile) + " "
        s += "\n"
        return s

    def __str__(self):
        string = "\nCurrent map:\n"
        string += self._str_grid()
        string += self._str_observed()
        string += self._str_worlds()
        string += self._str_safe()
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
        for i in range(len(self.worlds)):
            w = []
            if (len(self.worlds[i]) <= 0):
                w = ["0", "1"]
            else:
                w = [bstr + bstring(j) for j in range(1 << 1)
                     for bstr in self.worlds[i]]
            self.worlds[i] = w

    # update_knowledge: gets new models and performs the reasoning
    def update_knowledge(self, percepts, i, j):
        adj = self._adjacent_observed(i, j)
        indices = get_indices(self.observed, adj)
        self._get_knowledge(percepts, indices)

        # make inferences
        self._infer(adj, indices)

    # gets the possible models given a percept and adjacent indices
    def _get_knowledge(self, percepts, indices):

        # intersection!!
        for k in range(len(self.worlds)):
            new_worlds = []
            b = []
            g = []
            b = generate_bits(indices, k, percepts[k])
            g = generate_worlds(len(self.observed), b, indices, k)
            new_worlds = list(set(self.worlds[k]) & set(g))
            self.worlds[k] = new_worlds

    # given a tile location and its contents state, marks Tile according to that state
    def _mark_tile(self, l, m, state, adj):
        self.matrix[l][m].marks[state] = True

        # remaining adjacent tiles that are not that location are considered SAFE
        for (i, j) in adj:
            if ((i, j) != (l, m) and self.matrix[i][j].safe == False):
                self.matrix[i][j].safe = True
                self.safe_tiles.append((i, j))

    # performs logical inference
    def _logic_infer(self, bstr):
        k = bstr.index('1')
        (l, m) = self.observed[k]
        return (l, m)

    # removes contradictory possibilities
    def _remove_contradictions(self, state, indices, mli):
        # removing bstrs where the mli is off
        exclude = set()
        for i in indices:
            for bstr in self.worlds[state]:
                b = {bstr}
                if (i == mli and bstr[i] == "0"):
                    exclude |= b
                elif (state > state_index.PIT and bstr[i] == "1"):
                    exclude |= b
        self.worlds[state] = list(set(self.worlds[state]) - exclude)

    # performs probabilistic inference
    def _prob_infer(self, state, indices):
        mli = most_likely_index(self.worlds[state], self.probs[state], indices)
        (l, m) = self.observed[mli]
        return (l, m)

    # makes inferences about the possible true state
    def _infer(self, adj, indices):
        zero = "".zfill(len(self.observed))
        z = [zero]
        (l, m) = (0, 0)
        for i in range(len(self.worlds)):
            possibilities = get_possibilities(
                self.worlds[i], len(self.observed))
            if (not possibilities or possibilities == z):
                continue  # do not perform queries on Tiles that don't have anything

            if (not (bstr := one_possibility(self.worlds[i]))):
                # probabilistic query to get the most likely Tile
                (l, m) = self._prob_infer(i, indices)
            else:
                # otherwise get tile location according to logical reasoning
                (l, m) = self._logic_infer(bstr)
            self._mark_tile(l, m, i, adj)
            self._remove_contradictions(
                i, indices, self.observed.index((l, m)))
            if (not self.worlds[i]):
                self.worlds[i].append(zero)

    # return the current state of the map
    def get_state(self):
        return self.matrix
