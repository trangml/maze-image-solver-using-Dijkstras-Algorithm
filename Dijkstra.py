class Dijkstra:
    def __init__(self, maze):
        self.maze = maze
        self.graph = maze.graph
        self.source = maze.start_node
        self.finish = maze.finish_node

    def solveDPTDRecur(self, current, end):
        current.visited = True
        if current == end:
            return [current.parent]
        neighbors = self.maze.getUnvisitedNeighbors(current)
        if len(neighbors) == 0:
            return
        for neighbor in self.maze.getUnvisitedNeighbors(current):
            dist = self.maze.getDistance(current, neighbor)
            alt = current.distance + dist
            if( alt < neighbor.distance):
                neighbor.distance = alt
                neighbor.parent = current
        x = self.getMinDistance()
        if x is None:
            print("No path found")
            return
        self.solveDPTDRecur(x, end)
        return

    def solveDPTopDown(self):
        """Solve the maze using Dijkstra's algorithm and Top-Down Dynamic Programming"""
        self.source.distance = 0
        self.solveDPTDRecur(self.source, self.finish)
        if self.finish.parent is not None:
            path = [self.finish.parent]
            while path[0].parent is not None:
                path.insert(0, path[0].parent)
        return path

    def solveDPBottomUp(self):
        """Solve the maze using Dijkstra's algorithm and Bottom-Up Dynamic Programming"""
        path = []
        self.source.distance = 0
        # while graph is not all visited
        for count in range(self.maze.num_nodes):
            x = self.getMinDistance()
            if x is None:
                print("No path found")
                return []
            x.visited = True
            if x == self.finish:
                break
            for neighbor in self.maze.getUnvisitedNeighbors(x):
                dist = self.maze.getDistance(x, neighbor)
                if dist >= float('inf'):
                    neighbor.visited = True
                else:
                    alt = x.distance + dist
                    if( alt < neighbor.distance):
                        neighbor.distance = alt
                        neighbor.parent = x
        if self.finish.parent is not None:
            path = [self.finish.parent]
            while path[0].parent is not None:
                path.insert(0, path[0].parent)
        return path

    def getMinDistance(self):
        """Find the node with the minimum distance from the source node"""
        min_dist = float('inf')
        min_node = None
        for r in range(self.maze.num_rows):
            for c in range(self.maze.num_cols):
                node=self.maze.graph[r][c]
                if node.distance < min_dist and not node.visited:
                    min_dist = node.distance
                    min_node = node
        return min_node

    def findShortestPathRecursive(self, current, end, path):
        """Find the shortest path through a graph using Dijkstra's algorithm and recursion"""
        # if there are no new neighbors to explore, return None
        neighbors = self.maze.getUnvisitedNeighbors(current)
        if len(neighbors) == 0:
            return None

        # else, if we have reached the end, return path
        if current == end:
            return path
        path = path + [current]
        shortest_path = None
        # else, explore neighbors
        for neighbor in neighbors:
            dist = self.maze.getDistance(current, neighbor)
            if dist < float('inf'):
                if neighbor not in path:
                    new_path = self.findShortestPathRecursive(
                        neighbor, end, path
                    )
                    new_length = self.maze.getPathLength(new_path)
                    curr_length = self.maze.getPathLength(shortest_path)
                    if new_length < curr_length:
                        shortest_path = new_path
        #current.visited = True
        return shortest_path

    def solveRecursion(self):
        """Solve the maze using Dijkstra's algorithm and Dynamic Programming"""
        path = []
        path= self.findShortestPathRecursive(self.source, self.finish, path)
        return path
