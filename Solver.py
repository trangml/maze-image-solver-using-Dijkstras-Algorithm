import os
import sys
import argparse
import numpy as np
import time
import cv2 as cv
import matplotlib.pyplot as plt

from Maze import Maze
from Dijkstra import Dijkstra

def solver(image_folder, image_name, method, show_maze=True):
    print("Image name: ", image_name)
    print("Method: ", method)
    maze = Maze(image_folder+ image_name)
    #maze.saveOutputMaze(image_folder+"input_"+image_name)
    #maze.printOutput()
    di = Dijkstra(maze)
    start1=time.perf_counter()
    if method == "Recursive":
        shortest = di.solveRecursion()
    if method == "TDDP":
        shortest = di.solveDPTopDown()
    if method == "BUDP":
        shortest = di.solveDPBottomUp()
    end1=time.perf_counter()
    runtime=end1-start1
    print(f"Time: {runtime:0.8f} s")
    if shortest is not None:
        path_length = len(shortest)
        maze.drawPath(path=shortest)
        maze.saveOutputMaze(image_folder+"output_"+image_name)
        if show_maze:
            maze.printOutput()
    else:
        path_length = float('inf')
    print(f"Path Length: {path_length}")
    return (path_length,runtime)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, default='TDDP', help='which form of algorithm to run, TDDP, BUDP, or Recursive. Pass Benchmark to run benchmark test, or Difficulty to test difficulty', choices=['TDDP', 'BUDP', 'Recursive', 'Benchmark', 'Difficulty'])
    # Get the file
    parser.add_argument('--maze_file', type=str, default='maze_10x10.png', help='the file of the maze')
    args = parser.parse_args()

    image_folder="assets/"
    method = args.method
    image_name = args.maze_file

    if method == "Benchmark":
        ns = [3, 5, 7, 10, 15, 25, 30]
        bench_images = ["maze_3x3.png", "maze_5x5_med.png", "maze_7x7_hard.png","maze_10x10.png",  "maze_15x15.png", "maze_25x25_hard.png", "maze_30x30.png"]
        methods = ['TDDP', 'BUDP', 'Recursive']
        times = [[], [], []]
        lengths = [[], [], []]
        for image, n in zip(bench_images, ns):
            print("---------New Image----------")
            # time_per_image = []
            # time_per_image.append(n)
            # lengths_pi = []
            for m, time_per_image, lengths_pi in zip(methods, times, lengths):
                path_len, runtime = solver(image_folder, image, m, show_maze=False)
                print("")
                time_per_image.append(runtime)
                lengths_pi.append(path_len)
        print("---------Plotting Results----------")
        print(times)
        print(lengths)
        print("Benchmark complete")
        plt.plot(ns, times[0], label='TDDP', marker='o')
        plt.plot(ns, times[1], label='BUDP', marker='<')
        plt.plot(ns, times[2], label='Recursive', marker='s')
        plt.yscale('log')
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('seconds')
        plt.legend()
        plt.show()
    elif method == "Difficulty":
        ns = [5, 7, 25, 40, 50]
        bench_images = ["maze_7x7_easy.png", "maze_7x7_med.png", "maze_7x7_hard.png"]
        methods = ['TDDP', 'BUDP', 'Recursive']
        times = [[], [], []]
        lengths = []
        for image in bench_images:
            print("---------New Image----------")
            for m, time_per_image in zip(methods, times):
                path_len, runtime = solver(image_folder, image, m, show_maze=False)
                print("")
                time_per_image.append(runtime)
                lengths.append(path_len)
        print("---------Plotting Results----------")
        print(times)
        print(lengths)

        print("Benchmark complete")
        x = [1,2,3]
        labels = ['Easy', 'Medium', 'Hard']
        plt.plot(x, times[0], label='TDDP', marker='o')
        plt.plot(x, times[1], label='BUDP', marker='<')
        plt.plot(x, times[2], label='Recursive', marker='s')
        plt.xticks(x, labels)
        #plt.yscale('log')
        plt.grid(True)
        plt.xlabel('difficulty')
        plt.ylabel('seconds')
        plt.legend()
        plt.show()
    else:
        solver(image_folder, image_name, method)


if __name__ == "__main__":
    main()
