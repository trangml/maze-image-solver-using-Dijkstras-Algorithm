import os
import numpy as np
import time
import cv2 as cv
import matplotlib.pyplot as plt


class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.distance = float('inf')
        self.visited = False
        # TODO: Do i need this?
        # self.parent_x = 0
        # self.parent_y = 0
        # self.processed = False
        # self.index_in_queue = None
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y


class Maze:
    def __init__(self, maze_file):
        self.filename = maze_file
        # opencv uses BGR instead of RGB, so we need to convert
        self.maze_img = cv.cvtColor(
            cv.imread(maze_file, cv.IMREAD_COLOR), cv.COLOR_BGR2RGB
        )

        self.gray_maze_img = cv.imread(maze_file, cv.IMREAD_GRAYSCALE)
        self.num_rows, self.num_cols = self.gray_maze_img.shape[:2]
        self.num_nodes = self.num_rows * self.num_cols
        self.graph = self._getGraph()
        self.start_pos = self._getStart()
        self.finish_pos = self._getFinish()
        self.start_node=self.graph[self.start_pos[0], self.start_pos[1]]
        self.finish_node=self.graph[self.finish_pos[0], self.finish_pos[1]]

    def _getGraph(self):
        graph = np.full((self.num_rows, self.num_cols), None)
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                graph[r][c]  = Node(r, c)
        return graph

    def is_all_visited(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if not self.graph[r][c].visited:
                    return False
        return True

    def _getStart(self):
        # start_pos = np.where((self.gray_maze_img >= 100) & (self.gray_maze_img <= 200))
        # if len(start_pos[0]) != 1 or len(start_pos[1]) != 1:
        #     print(
        #         "Incorrect start position found!, make sure there is only one green start position"
        #     )
        #     return None
        # RGB
        start_pos = np.where((self.maze_img[:,:,0] <= 100) & (self.maze_img[:,:,1] >= 200) & (self.maze_img[:,:,2] <= 100))
        return np.asarray((start_pos[0][-1], start_pos[1][-1]), dtype=np.int32)

    def _getFinish(self):
        # finish_pos = np.where((self.gray_maze_img >= 10) & (self.gray_maze_img <= 100))
        # if len(finish_pos[0]) != 1 or len(finish_pos[1]) != 1:
        #     print(
        #         "Incorrect finish position found!, make sure there is only one red finish position"
        #     )
        #     return None
        finish_pos = np.where((self.maze_img[:,:,0] >= 200) & (self.maze_img[:,:,1] <= 100) & (self.maze_img[:,:,2] <= 100))
        return np.asarray((finish_pos[0][0], finish_pos[1][0]), dtype=np.int32)

    def getDistance(self, u, v):
        if self.gray_maze_img[u.x, u.y] <= 25:
            return float('inf')
        if self.gray_maze_img[v.x, v.y] <= 25:
            return float('inf')
        return 0.1

    def getPathLength(self, path):
        if path is None:
            return float('inf')
        total_length = 0
        for i in range(len(path) - 1):
            total_length += self.getDistance(path[i], path[i + 1])
        return total_length

    def getNeighbors(self, current):
        neighbors = []
        if current.x - 1 >= 0:
            neighbors.append(self.graph[current.x - 1, current.y])
        if current.x + 1 < self.num_rows:
            neighbors.append(self.graph[current.x + 1, current.y])
        if current.y - 1 >= 0:
            neighbors.append(self.graph[current.x, current.y - 1])
        if current.y + 1 < self.num_cols:
            neighbors.append(self.graph[current.x, current.y + 1])
        return neighbors

    def getUnvisitedNeighbors(self, current):
        unvisited_neighbors = []
        for neighbor in self.getNeighbors(current):
            if neighbor is not None and not neighbor.visited:
                unvisited_neighbors.append(neighbor)
        return unvisited_neighbors

    def saveOutputMaze(self, output_file):
        # self.print_img = cv.resize(
        #     self.gray_maze_img, (400, 400), interpolation=cv.INTER_AREA
        # )
        # cv.imwrite(output_file, self.print_img)
        self.color_print_img = cv.cvtColor(self.maze_img, cv.COLOR_RGB2BGR)
        self.color_print_img  = cv.resize(
            self.color_print_img , (400, 400), interpolation=cv.INTER_AREA
        )
        cv.imwrite(output_file, self.color_print_img)

    def drawPath(self, path, color=(0, 0, 255)):
        # start at 1 since 0 is the start
        if len(path)<1:
            return
        x0, y0 = path[1].x, path[1].y
        for node in path[2:]:
            x1, y1 = node.x, node.y
            cv.line(
                self.maze_img, (y0, x0), (y1, x1), color, thickness=1
            )
            x0, y0 = x1, y1

    def printOutput(self):
        # cv.imshow("Maze", self.color_print_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        plt.figure(figsize=(6, 6))
        plt.imshow(self.maze_img)
        plt.show()
