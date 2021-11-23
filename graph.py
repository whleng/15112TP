from cmu_112_graphics import *

##############################################################################
# GRAPH OBJECTS
##############################################################################

# The following concepts and structual framework was referenced from TA lecture: 
# Graph Algorithm

##############################################################################

class Graph(object):
    def __init__(self):
        self.table = dict() # dict storing the nodes and edges

    # add an edge between two nodes in the graph
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = dict()
        if nodeB not in self.table:
            self.table[nodeB] = dict()
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight

    # return weight of an edge between two nodes
    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]

    # return list of all nodes in the graph
    def getNodes(self):
        return list(self.table)

    def getNeighbours(self, node):
        return set(self.table[node])

# have yet to integrate the node as an object  
class Node(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col


##############################################################################
# DEPTH FIRST SEARCH
##############################################################################

# The following concepts and structual framework was referenced from TA lecture: 
# Graph Algorithm

##############################################################################

# main dfs function 
def dfs(graph, startNode, targetNode): # does not find shortest path
    visited = set()
    solution = dict()
    solution = solve(startNode, targetNode, graph, visited, solution)
    solution = constructPath(solution, startNode, targetNode)
    # print("sol:", solution)
    return solution # a list of coordinates

# returns a list containing (row, col) positions of path
def constructPath(solution, startNode, targetNode): 
    currNode = targetNode
    path = [currNode]
    while True:
        if currNode == startNode: break
        prevNode = solution[currNode] 
        path.append(prevNode)
        currNode = prevNode
    return path

# recursive solve function
def solve(startNode, targetNode, graph, visited, solution):
    if startNode == targetNode:
        return solution
    visited.add(startNode)
    for neighbour in graph.getNeighbours(startNode):
        if neighbour not in visited:
            solution[neighbour] = startNode
            tempsol = solve(neighbour, targetNode, graph, visited, solution)
            if tempsol != None: return tempsol
            solution[neighbour] = None
    return None

# dfs() # uncomment to test dfs


##############################################################################
# BREADTH FIRST SEARCH
##############################################################################

# The following concepts and structual framework was referenced from TA lecture: 
# Graph Algorithm
# Queue documentation was also referenced: https://docs.python.org/3/library/queue.html

##############################################################################

from queue import *

def bfs(graph, startNode, targetNode):
    visited = set()
    solution = dict()
    q = Queue() # to be visited
    q.put(startNode) 
    currNode = startNode
    while currNode != targetNode:
        # print(currNode)
        currNode = q.get()
        visited.add(currNode)
        for neighbour in graph.getNeighbours(currNode):
            if neighbour not in visited:
                solution[neighbour] = currNode
                q.put(neighbour)
                visited.add(neighbour)
    solution = constructPath(solution, startNode, targetNode)
    # print(solution)
    if solution != []: solution.pop()
    return solution

# bfs() # uncomment to test dfs


##############################################################################
# PRIM'S ALGORITHM
##############################################################################

# The following concepts and structual framework was referenced from TA lecture: 
# Graph Algorithm
# The following resources were also referenced:
# - https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
# - https://hurna.io/academy/algorithms/maze_generator/prim_s.html

##############################################################################

import random 

def prim(app):
    startNode = (0,0)
    cells = set() # set of cells
    visited = set()
    cells.add(startNode)
    graph = Graph()
    while len(cells) > 0:
        # get a random cell
        cell = random.choice(list(cells))
        cells.remove(cell)
        visited.add(cell) # mark cell as visited
        row, col = cell
        visitedNeighbours, unvisitedNeighbours = getNeighbours(app, app.rows, app.cols, row, col, visited) 
        # return visited neighbours
        if len(visitedNeighbours) > 0:
            neighbour = visitedNeighbours.pop()
            graph.addEdge(neighbour, cell) 
            # randomly connect the cell to a neighbour which has been visited
        cells = set.union(cells, unvisitedNeighbours) # add unvisited neighbour to the set
    # to create more paths, randomly add in some edges
    # for i in range(100):
    #     cell = random.randint(0, app.rows), random.randint(0, app.cols)
    #     (drow, dcol) = random.choice(app.directions)
    #     neighbour = cell[0] + drow, cell[1] + dcol
    #     graph.addEdge(neighbour, cell)
    return graph

# obtaining the 4 cells around a cell
def getNeighbours(app, rows, cols, row, col, visited):
    visitedNeighbours = set()
    unvisitedNeighbours = set()
    for dir in app.directions:
        drow, dcol = dir
        newRow, newCol = row+drow, col+dcol
        if (0 <= newRow < rows and 
            0 <= newCol < cols):
            if ((newRow,newCol) not in visited):
                unvisitedNeighbours.add( (newRow, newCol) )
            else: 
                visitedNeighbours.add( (newRow, newCol))
    return visitedNeighbours, unvisitedNeighbours

##############################################################################
# NO DEAD END MAP GENERATION
# This algorithm tries to create a maze with no dead ends through the use of DFS/recursion
# Loosely referenced from TA Lecture: Graph Algorithms (Maze Generation)
##############################################################################

# dfs until every node has been visited
# check through each node
# if a node only has one neighbour, connect it to a neighbour beside it 
# backtrack to the previous above node that has not been visited 