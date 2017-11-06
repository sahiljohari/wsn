#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:36:49 2017
@author: Sahil Johari
"""
# import matplotlib
# matplotlib.use('TkAgg')
import numpy as np
from scipy import spatial
import networkx as nx
import matplotlib.pyplot as plt

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
import timeit
import operator
import warnings
import copy

warnings.filterwarnings("ignore")

def generate_coordinates(topology, nodes):
    if topology == 0:
        coordinates = np.random.rand(nodes, 2)
    elif topology == 1:
        theta = np.random.uniform(0, 2 * np.pi, nodes)
        radian = np.sqrt(np.random.uniform(0.0, 1.0, nodes))
        x = (radian * np.cos(theta))
        y = (radian * np.sin(theta))

        coordinates = np.vstack((x, y)).T
    else:
        print('Topology does not exists!')
        coordinates = 0

    return coordinates

def random_color():
    red = np.random.uniform(0, 1)
    green = np.random.uniform(0, 1)
    blue = np.random.uniform(0, 1)

    return red, green, blue

def smallest_last_ordering(degree, adjacency_list):
    node_stack = []
    degreeTemp = {}
    for key, val in degree.items():
        degreeTemp.setdefault(val, []).append(key)

    # 1. Loop degree and find min degree inside the loop
    # while degree:
    #     min_deg, min_node = min(degreeTemp.items(), key=operator.itemgetter(0))
    # # 2. Iterate values of node with min degree in adjacency list
    # # 3. Decrement degree of each nodes corresponding to min node
    #     popped_node = min_node.pop()
    #     for item in adjacency_list[popped_node]:
    #         if item in degree:
    #             # d = degree[item]
    #             adjacency_list[item].remove(popped_node)
    #             degree[item] -= 1
    #             degreeTemp.setdefault(min_deg-1, []).append(item)
    while adjacency_list:
        min_deg, min_nodes = min(degreeTemp.items(), key=operator.itemgetter(0))
        popped_node = min_nodes.pop()
        if not min_nodes:
            del degreeTemp[min_deg]
        for item in adjacency_list[popped_node]:
            adjacency_list[item].remove(popped_node)
            d = degree[item]
            degreeTemp[d].remove(item)

            if not degreeTemp[d]:
                del degreeTemp[d]

            degreeTemp.setdefault(d-1, []).append(item)
            degree[item] -= 1

        node_stack.append(popped_node)
        del adjacency_list[popped_node]
    return node_stack

def graph_coloring(node_stack, adjacency_list):
    color_map = {}
    clist = [random_color()]

    while node_stack:
        popped_node = node_stack.pop()
        adjacent_nodes = adjacency_list[popped_node]
        temp = []
        for node in adjacent_nodes:
            if node in color_map:
                temp.append(clist.index(color_map[node]))

        c_index = 0
        if len(temp) > 0:
            temp = sorted(set(temp))
            for i in temp:
                if i == c_index:
                    c_index += 1
                else:
                    break

        if c_index == len(clist):
            clist.append(random_color())

        color_map[popped_node] = clist[c_index]
    return color_map, clist

def plot_Graph(topology, nodes, avgDeg, coloring):
    degree = {}
    adjacency_list = {}
    # color_map = {}
    c_map = []
    max_edges = []
    min_edges = []

    start = timeit.default_timer()
    if topology == 0:
        r = np.sqrt(avgDeg / (nodes * np.pi))
    elif topology == 1:
        r = np.sqrt(avgDeg / nodes)

    coordinates = generate_coordinates(topology, nodes)

    tree = spatial.KDTree(coordinates)
    pairs = list(tree.query_pairs(r))

    for x, y in pairs:
        adjacency_list.setdefault(x, []).append(y)
        adjacency_list.setdefault(y, []).append(x)

    for edge in pairs:
        degree[edge[0]] = degree.get(edge[0], 0) + 1
        degree[edge[1]] = degree.get(edge[1], 0) + 1

    max_deg = max(degree.items(), key=operator.itemgetter(1))[1]
    if not nodes == len(adjacency_list):
        min_deg = 0
    else:
        min_deg = min(degree.items(), key=operator.itemgetter(1))[1]
    total_deg = sum(degree.values())

    observed_avg_deg = total_deg / nodes

    max_node = [k for k, v in degree.items() if v == max_deg]
    min_node = [k for k, v in degree.items() if v == min_deg]
 
    for i in pairs:
        if i[0] in max_node or i[1] in max_node:
            max_edges.append(i)
        if i[0] in min_node or i[1] in min_node:
            min_edges.append(i)

    G = nx.Graph()
    G.add_nodes_from(range(nodes))
    G.add_edges_from(list(pairs))
    pos = dict(zip(range(nodes), coordinates))

    # for node in G:
    #     if node in max_node:
    #         c_map.append('red')
    #     elif node in min_node or (min_deg == 0 and node not in min_node):   #Bug here
    #         c_map.append('blue')
    #     else:
    #         c_map.append('black')

    node_size = 40
    edge_color = '#00916a'

    adjlist_copy = copy.deepcopy(adjacency_list)
    node_stack = smallest_last_ordering(degree, adjlist_copy)
    color_map, clist = graph_coloring(node_stack, adjacency_list)

    c_map = [None] * nodes
    for i in range(nodes):
        if i in color_map:
            c_map[i] = color_map[i]
        else:
            c_map[i] = clist[0]

    print('\n-----------------------------')
    print('No. of edges: ', len(pairs))
    print('Max Degree: ', max_deg)
    print('Min Degree: ', min_deg)
    print('Average Degree: ', observed_avg_deg)
    print('-----------------------------')
    print('Elapsed time: ', timeit.default_timer() - start, 'second(s)')

    # nx.draw(G, pos, node_size=1, node_color=c_map, alpha=0.5, edge_color='#00916a')
    # nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color='red', width=1.0)
    # nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=1.0)

    # def init():
    #     return nx.draw(G, pos, node_size=1, node_color=c_map, alpha=0.5, edge_color='#00916a')
    #
    # def animate(i):
    #     if node_stack[i] in G.nodes():
    #         # print(G.nodes())
    #         plt.clf()
    #         plt.axis('equal')
    #         G.remove_node(node_stack[i])
    #     nx.draw(G, pos, node_size=1, node_color=c_map, alpha=0.5, edge_color='#00916a')
    # anim = animation.FuncAnimation(fig, animate, frames=len(node_stack), interval=1)

    nx.draw(G, pos, node_size=node_size, node_color=c_map, edge_color=edge_color, alpha=0.9)

    plt.axis('off')
    plt.axis('equal')
    plt.show()

def main():
    nodes = int(input('Enter the number of nodes: '))
    expected_avg_deg = int(input('Enter the average degree: '))
    topology = int(input('Select a topology - 0 (plane) | 1 (disk): '))
    coloring = input('Enable coloring - Y|N: ')

    plot_Graph(topology, nodes, expected_avg_deg, coloring)


if __name__ == "__main__":
    main()
