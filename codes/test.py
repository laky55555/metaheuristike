import collections
import itertools


def neighbours_of(i, j):
    """Positions of neighbours (includes out of bounds but excludes cell itself)."""
    neighbours = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    neighbours.remove((i, j))
    return neighbours


def find_surrounded(grid):
    """List of x,y positions in grid where the cell is surrounded by 1s."""
    votes = collections.defaultdict(int)
    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            # we don't get to vote if not ...
            print ("i, j "   + str(i) + "  " + str(j))
            if y == 0:
                continue
            # vote for everyone in the 3x3 square around us
            for a, b in neighbours_of(i, j):
                #print ("Iz (i,j) => a, b" + str(i) + "  " + str(j) + " "  + str(a) + "  " + str(b))
                votes[(a, b)] += 1
    print(votes)
    # now the things we want to change are those that got 8 votes
    surrounded_positions = [pos for pos, count in votes.items() if count == 8]
    return surrounded_positions

def change_when_cell_type_surrounded(grid, cell_type):
    """Update grid inline to flip bits of cells of cell_type that are surrounded."""
    # we'll flip to the opposite of what we're looking for
    change_to = 1 - cell_type
    surrounded = find_surrounded(grid)
    for i, j in surrounded:
        if grid[i][j] == cell_type:
            grid[i][j] = change_to


grid = [[0,0,0,0,0],
        [0,1,1,1,0],
        [0,1,1,1,1],
        [0,1,1,1,0],
        [0,0,1,0,0]]

change_when_cell_type_surrounded(grid, 1)
change_when_cell_type_surrounded(grid, 0)
