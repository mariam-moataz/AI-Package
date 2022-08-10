from operator import attrgetter


class Node:
    id = None  # Unique value for each node.
    value = None  # name for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, id, value=None, hOfN=None):
        self.id = id
        self.value = value
        self.hOfN = hOfN


class Board:
    Board_Nodes = None
    Board_Chars = None
    Board_Heuristics = None

    def __init__(self, Mazestr, heuristicValues=None):
        self.Board_Heuristics = heuristicValues
        List = []
        Maze = (Mazestr.split(" "))
        for i in Maze:
            u = i.split(",")
            List.append(u)
        self.Board_Chars = List
        self.ROWS = len(List)
        self.COLUMNS = len(List[0])
        self.intialize()

    def intialize(self):

        u = 0
        List = []
        for i in range(self.ROWS):
            suplist = []
            for j in range(self.COLUMNS):
                if self.Board_Heuristics is None:
                    N = Node(u, self.Board_Chars[i][j])
                else:
                    N = Node(u, self.Board_Chars[i][j], self.Board_Heuristics[u])
                suplist.append(N)
                u += 1
            List.append(suplist)
        self.Board_Nodes = List

        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                self.Set_neighbours(self.Board_Nodes[i][j])

    def in_bounds(self, row, col):
        if row < 0 or col < 0:
            return False
        if row > len(self.Board_Chars) - 1 or col > len(self.Board_Chars[0]) - 1:
            return False
        if self.Board_Chars[row][col] == "#":
            return False
        return True

    def to_1d(self, row, col):
        return (row * self.COLUMNS) + col

    def to_2d(self, id):
        row = id // self.COLUMNS
        column = id % self.COLUMNS
        return row, column

    def Set_neighbours(self, node):

        row, column = self.to_2d(node.id)
        if self.in_bounds(row - 1, column) == 1:
            node.up = self.Board_Nodes[row - 1][column]
        if self.in_bounds(row + 1, column) == 1:
            node.down = self.Board_Nodes[row + 1][column]
        if self.in_bounds(row, column - 1) == 1:
            node.left = self.Board_Nodes[row][column - 1]
        if self.in_bounds(row, column + 1) == 1:
            node.right = self.Board_Nodes[row][column + 1]

    def Get_successors(self, node):

        neighbours = []
        if node.up is not None:
            neighbours.append(node.up)
        if node.down is not None:
            neighbours.append(node.down)
        if node.left is not None:
            neighbours.append(node.left)
        if node.right is not None:
            neighbours.append(node.right)
        return neighbours

    def Get_Start_Node(self):
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if self.Board_Nodes[i][j].value == "S":
                    m = self.Board_Nodes[i][j]
                    return m

    def Get_End_Node(self):
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if self.Board_Nodes[i][j].value == "E":
                    m = self.Board_Nodes[i][j]
                    return m


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''

    limit = None  # dls
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    vis_path = []  # dls
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)

    def __init__(self, mazeStr, heristicValue=None):

        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.mazeStr = mazeStr
        if heristicValue is None:
            self.h = Board(mazeStr)
        else:
            self.h = Board(mazeStr, heristicValue)
        self.Start_Node = self.h.Get_Start_Node()
        self.Goal_Node = self.h.Get_End_Node()
        self.path.clear()
        self.fullPath.clear()
        self.vis_path.clear()

    def return_path1(self, node):
        while node is not None:
            self.path.append(node.id)
            node = node.previousNode
        self.path.reverse()

    def return_path(self, node=Node(0)):
        path_list = []
        while node is not None:
            path_list.append(node.id)
            node = node.previousNode
        return path_list

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.Recursive_DLS(self.Start_Node, self.h.Board_Nodes, 50)
        return self.path, self.fullPath

    def Recursive_DLS(self, node, problem, limit):

        cutoff = True
        failure = True
        self.fullPath.append(node.id)

        if node.value == self.Goal_Node.value:
            #self.Goal_Node.previousNode = node
            self.return_path1(node)
            return node
        elif limit == 0:
            return cutoff
        else:
            cutoff = False
            child = self.h.Get_successors(node)
            for i in child:
                if i.id not in self.vis_path:
                    i.previousNode = node
                    self.vis_path.append(node.id)
                    result = self.Recursive_DLS(i, problem, limit - 1)
                    self.vis_path.pop(len(self.vis_path) - 1)
                    if result == cutoff:
                        cutoff = True
                    elif result != failure:
                        return result
            if cutoff:
                return cutoff
            return failure

    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes

        f_queue = []
        b_queue = []

        f_queue.append(self.Start_Node)
        b_queue.append(self.Goal_Node)

        forward_vis = []  # bds
        backward_vis = []  # bds

        limit = self.h.ROWS * self.h.COLUMNS
        for i in range(limit):
            forward_vis.append(0)
            backward_vis.append(0)

        while f_queue.__len__() > 0 and b_queue.__len__() > 0:

            cur_Fnode = f_queue[0]
            self.fullPath.append(cur_Fnode.id)
            f_queue.pop(0)

            cur_Bnode = b_queue[0]
            self.fullPath.append(cur_Bnode.id)
            b_queue.pop(0)

            forward_vis[cur_Fnode.id] = 1
            backward_vis[cur_Bnode.id] = 1

            fchildren = self.h.Get_successors(cur_Fnode)
            for child in fchildren:
                if forward_vis[child.id] != 0:
                    continue

                if backward_vis[child.id] == 1:
                    if child.id not in self.fullPath:
                        self.fullPath.append(child.id)
                    list1 = self.return_path(cur_Fnode)
                    list1.reverse()
                    list2 = self.return_path(child)
                    self.path = list1 + list2
                    return self.path, self.fullPath

                child.previousNode = cur_Fnode
                forward_vis[child.id] = 1
                f_queue.append(child)

            bchildren = self.h.Get_successors(cur_Bnode)
            for child2 in bchildren:
                if backward_vis[child2.id] != 0:
                    continue

                if forward_vis[child2.id] == 1:
                    if child2.id not in self.fullPath:
                        self.fullPath.append(child2.id)
                    list1 = self.return_path(child2)
                    list1.reverse()
                    list2 = self.return_path(cur_Bnode)
                    self.path = list1 + list2

                    return self.path, self.fullPath

                child2.previousNode = cur_Bnode
                backward_vis[child2.id] = 1
                b_queue.append(child2)

        return self.path, self.fullPath

    def contains_id(self, container, id):
        for i in range(len(container)):
            if container[i].id == id:
                return True
        return False

    def BFS_path(self, node):
        if node.previousNode is None:
            self.path.append(node.id)
        else:
            self.BFS_path(node.previousNode)
            self.path.append(node.id)

    def BFS_full_path(self, closed):
        for i in closed:
            self.fullPath.append(i.id)
        self.fullPath.append(self.Goal_Node.id)

    def BFS_cost(self, node):
        if node.previousNode.id == self.Start_Node.id:
            self.totalCost = node.hOfN
        else:
            self.BFS_cost(node.previousNode)

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes

        open = [self.Start_Node]
        closed = []

        counter = 0

        while True:

            Current_Node = min(open, key=attrgetter('hOfN'))

            if Current_Node.value is self.Goal_Node.value:
                self.BFS_path(Current_Node)
                self.BFS_full_path(closed)
                self.BFS_cost(Current_Node)
                return self.path, self.fullPath, self.totalCost

            Successors = self.h.Get_successors(Current_Node)

            for i in Successors:
                if self.contains_id(open, i.id) or self.contains_id(closed, i.id):
                    continue
                i.previousNode = Current_Node
                open.append(i)

            for i in range(len(open)):
                if open[i].id == Current_Node.id:
                    open.pop(i)
                    break

            closed.append(Current_Node)


def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('DFS\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms('.,.,.,.,E,#,.,. .,.,#,#,#,.,#,. .,#,#,.,.,#,#,. .,#,#,.,.,.,.,. .,.,.,.,.,.,.,S')
    path, fullPath = searchAlgo.BDS()
    print('BFS\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print(' UCS \nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
    #######################################################################################


main()
