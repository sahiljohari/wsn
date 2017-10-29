#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:36:49 2017
@author: Sahil Johari
"""
import numpy as np
from scipy import spatial
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
import timeit
import operator
import warnings

warnings.filterwarnings("ignore")

degree = {}
c_map = []

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

def plot_Graph(topology, nodes, avgDeg):
    start = timeit.default_timer()
    if topology == 0:
        r = np.sqrt(avgDeg / (nodes * np.pi))
    elif topology == 1:
        r = np.sqrt(avgDeg / nodes)

    coordinates = generate_coordinates(topology, nodes)

    tree = spatial.KDTree(coordinates)
    pairs = tree.query_pairs(r)

    for edge in list(pairs):
        degree[edge[0]] = degree.get(edge[0], 0) + 1
        degree[edge[1]] = degree.get(edge[1], 0) + 1

    max_deg = max(degree.items(), key=operator.itemgetter(1))[1]
    min_deg = min(degree.items(), key=operator.itemgetter(1))[1]
    total_deg = sum(degree.values())

    observed_avg_deg = total_deg / nodes

    max_edges = []
    min_edges = []

    max_node = [k for k, v in degree.items() if v == max_deg]
    min_node = [k for k, v in degree.items() if v == min_deg]
 
    for i in list(pairs):
        if i[0] in max_node or i[1] in max_node:
            max_edges.append(i)
        if i[0] in min_node or i[1] in min_node:
            min_edges.append(i)

    G = nx.Graph()
    G.add_nodes_from(range(nodes))
    G.add_edges_from(list(pairs))

    for node in G:
        if node in max_node:
            c_map.append('red')
        elif node in min_node:
            c_map.append('blue')
        else:
            c_map.append('black')

    pos = dict(zip(range(nodes), coordinates))
    print('\n-----------------------------')
    print('No. of edges: ', len(pairs))
    print('Max Degree: ', max_deg)
    print('Min Degree: ', min_deg)
    print('Average Degree: ', observed_avg_deg)
    print('-----------------------------')
    print('Elapsed time: ', timeit.default_timer() - start, 'second(s)')


    nx.draw_networkx_nodes(G, pos, node_size=1, node_color=c_map)
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='#00916a')
    # nx.draw(G, pos, node_size=1, node_color=c_map, alpha=0.5, edge_color='#00916a')
    nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color='red', width=1.0)
    nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=1.0)

    plt.axis('off')
    plt.axis('equal')
    plt.show()

def main():
    nodes = int(input('Enter the number of nodes: '))
    expected_avg_deg = int(input('Enter the average degree: '))
    topology = int(input('Select a topology - 0 (plane) | 1 (disk): '))

    plot_Graph(topology, nodes, expected_avg_deg)


if __name__ == "__main__":
    main()
