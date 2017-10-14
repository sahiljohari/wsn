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
import timeit
import operator
import warnings

warnings.filterwarnings("ignore")

degree = {}
c_map = []


def plot_Square(nodes, avgDeg):
    start = timeit.default_timer()
    r = np.sqrt(avgDeg / (nodes * np.pi))

    coordinates = np.random.rand(nodes, 2)
    tree = spatial.KDTree(coordinates)
    pairs = tree.query_pairs(r)

    for edge in list(pairs):
        degree[edge[0]] = degree.get(edge[0], 0) + 1
        degree[edge[1]] = degree.get(edge[1], 0) + 1

    max_deg = max(degree.items(), key=operator.itemgetter(1))[1]
    min_deg = min(degree.items(), key=operator.itemgetter(1))[1]
    total_deg = sum(degree.values())

    observed_avg_deg = total_deg / nodes

    G = nx.Graph()
    G.add_nodes_from(range(nodes))
    G.add_edges_from(list(pairs))

    pos = dict(zip(range(nodes), coordinates))
    print('\n-----------------------------')
    print('No. of edges: ', len(pairs))
    print('Max Degree: ', max_deg)
    print('Min Degree: ', min_deg)
    print('Average Degree: ', observed_avg_deg)
    print('-----------------------------')
    print('Elapsed time: ', timeit.default_timer() - start, 'second(s)')

    max_edges = []
    min_edges = []
    max_node = max(degree.items(), key=operator.itemgetter(1))[0]
    min_node = min(degree.items(), key=operator.itemgetter(1))[0]

    for i in list(pairs):
        if i[0] == max_node or i[1] == max_node:
            max_edges.append(i)
        if i[0] == min_node or i[1] == min_node:
            min_edges.append(i)

    for node in G:
        if node == max_node:
            c_map.append('red')
        elif node == min_node:
            c_map.append('blue')
        else:
            c_map.append('black')

    nx.draw(G, pos, node_size=4, node_color=c_map, alpha=0.4, edge_color = '#00916a')
    nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color = 'red', width = 2.0)
    nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=2.0)
    plt.axis('equal')
    plt.show()


def plot_Disk(nodes, avgDeg):
    start = timeit.default_timer()
    r = np.sqrt(avgDeg / nodes)

    theta = np.random.uniform(0, 2 * np.pi, nodes)
    radian = np.sqrt(np.random.uniform(0.0, 1.0, nodes))
    x = (radian * np.cos(theta))
    y = (radian * np.sin(theta))

    coordinates = np.vstack((x, y)).T

    tree = spatial.KDTree(coordinates)
    pairs = tree.query_pairs(r)

    for edge in list(pairs):
        degree[edge[0]] = degree.get(edge[0], 0) + 1
        degree[edge[1]] = degree.get(edge[1], 0) + 1

    max_deg = max(degree.items(), key=operator.itemgetter(1))[1]
    min_deg = min(degree.items(), key=operator.itemgetter(1))[1]
    total_deg = sum(degree.values())

    observed_avg_deg = total_deg / nodes

    G = nx.Graph()
    G.add_nodes_from(range(nodes))
    G.add_edges_from(list(pairs))

    pos = dict(zip(range(nodes), coordinates))
    print('\n-----------------------------')
    print('No. of edges: ', len(pairs))
    print('Max Degree: ', max_deg)
    print('Min Degree: ', min_deg)
    print('Average Degree: ', observed_avg_deg)
    print('-----------------------------')
    print('Elapsed time: ', timeit.default_timer() - start)

    max_edges = []
    min_edges = []
    max_node = max(degree.items(), key=operator.itemgetter(1))[0]
    min_node = min(degree.items(), key=operator.itemgetter(1))[0]

    for i in list(pairs):
        if i[0] == max_node or i[1] == max_node:
            max_edges.append(i)
        if i[0] == min_node or i[1] == min_node:
            min_edges.append(i)

    for node in G:
        if node == max_node:
            c_map.append('red')
        elif node == min_node:
            c_map.append('blue')
        else:
            c_map.append('black')

    nx.draw(G, pos, node_size=4, node_color=c_map, alpha=0.4, edge_color='#00916a')
    nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color='red', width=2.0)
    nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=2.0)
    plt.axis('equal')
    plt.show()


def main():
    nodes = int(input('Enter the number of nodes: '))
    expected_avg_deg = int(input('Enter the average degree expected: '))
    topology = int(input('Choose a topology - 0(square) | 1(disk): '))

    if topology == 0:
        plot_Square(nodes, expected_avg_deg)
    elif topology == 1:
        plot_Disk(nodes, expected_avg_deg)
    else:
        print('Invalid choice!')


if __name__ == "__main__":
    main()
