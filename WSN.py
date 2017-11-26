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
import matplotlib.animation as animation

import timeit
import operator
import warnings
import copy
import itertools
from itertools import chain

warnings.filterwarnings("ignore")


def connected_components(neighbors):
    seen = set()

    def component(node):
        nodes = set([node])
        while nodes:
            node = nodes.pop()
            seen.add(node)
            nodes |= neighbors[node] - seen
            yield node

    for node in neighbors:
        if node not in seen:
            yield component(node)


def largest_component(old_graph):
    new_graph = {node: set(edge for edge in edges)
                 for node, edges in old_graph.items()}
    components = []
    for component in connected_components(new_graph):
        c = set(component)
        components.append([edges for edges in old_graph.values()
                           if c.intersection(edges)])
    return components

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
    degreeBucket = {}
    terminal_size = 0

    for key, val in degree.items():
        degreeBucket.setdefault(val, []).append(key)

    while adjacency_list:
        min_deg, min_nodes = min(degreeBucket.items(), key=operator.itemgetter(0))
        popped_node = min_nodes.pop()
        if not min_nodes:
            del degreeBucket[min_deg]

        counter = 0
        for item in adjacency_list[popped_node]:
            adjacency_list[item].remove(popped_node)
            d = degree[item]
            degreeBucket[d].remove(item)

            if not degreeBucket[d]:
                del degreeBucket[d]

            degreeBucket.setdefault(d-1, []).append(item)
            degree[item] -= 1
            counter += 1
        node_stack.append(popped_node)

        if len(adjacency_list)-1 == counter and terminal_size == 0:
            terminal_size = counter + 1
        del adjacency_list[popped_node]

    return node_stack, terminal_size

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

def plot_Graph(topology, nodes, avgDeg, display_mode):
    degree = {}
    adjacency_list = {}
    color_data = {}  # contains collection of nodes for each distinct color
    c_map = []  # contains all the colors generated
    max_edges = []
    min_edges = []
    bipartite_nodes = []
    # bipartite_color = []

    start = timeit.default_timer()
    if topology == 0:
        r = np.sqrt(avgDeg / (nodes * np.pi))
    elif topology == 1:
        r = np.sqrt(avgDeg / nodes)
    else:
        r = 0

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
    if display_mode in (0, 1, 3):
        G.add_edges_from(list(pairs))
    pos = dict(zip(range(nodes), coordinates))

    if display_mode == 0:
        for node in G:
            if node in max_node:
                c_map.append('red')
            elif node in min_node:
                c_map.append('blue')
            else:
                c_map.append('black')

    if display_mode in (1, 2, 3):
        adjlist_copy = copy.deepcopy(adjacency_list)
        node_stack, terminal_size = smallest_last_ordering(degree, adjlist_copy)
        if display_mode in (2, 3):
            node_stack_copy = copy.deepcopy(node_stack)
            color_map, clist = graph_coloring(node_stack_copy,
                                              adjacency_list)  #color_map->c_map ; clist contains list of distinct colors
            c_map = [None] * nodes
            for i in range(nodes):
                if i in color_map:
                    c_map[i] = color_map[i]
                else:
                    c_map[i] = clist[0]

            for k,v in color_map.items():
                color_data.setdefault(v, []).append(k)

            color_count_data = {k: len(color_data[k]) for k in color_data.keys()}  # contains node count for each color
            max_color = max(color_count_data.items(), key=operator.itemgetter(1))[1]

            if display_mode == 3:
                # Bipartite calculation
                largest_colors = sorted(color_count_data, key=color_count_data.get, reverse=True)[:4]
                largest_colors_combinations = list(itertools.combinations(largest_colors, 2))
                for c_pair in largest_colors_combinations:
                    bipartite_nodes.append((color_data[c_pair[0]], color_data[c_pair[1]]))

                unique_bipartites = []
                max_backbone = []

                for node_pair in bipartite_nodes:
                    bipartite_adj = {}
                    for node in node_pair[0]:
                        bipartite_adj[node] = list(set(adjacency_list[node]) & set(node_pair[1]))
                    for node in node_pair[1]:
                        bipartite_adj[node] = list(set(adjacency_list[node]) & set(node_pair[0]))
                    unique_bipartites.append(copy.deepcopy(bipartite_adj))

                for collection in unique_bipartites:
                    bipartite_nodelist = []
                    bipartite_nodelist.extend(max(largest_component(collection), key=len))
                    max_backbone.append(list(np.unique(list(chain.from_iterable(bipartite_nodelist)))))

                bipartite_backbone = sorted(max_backbone, key=len, reverse=True)[:2]
                bipartite_nodeColors_1 = []
                bipartite_nodeColors_2 = []
                for node in bipartite_backbone[0]:
                    bipartite_nodeColors_1.append([k for k, v in color_data.items() if node in v])
                for node in bipartite_backbone[1]:
                    bipartite_nodeColors_2.append([k for k, v in color_data.items() if node in v])

                bipartite_nodeColors_1 = list(chain.from_iterable(bipartite_nodeColors_1))
                bipartite_nodeColors_2 = list(chain.from_iterable(bipartite_nodeColors_2))

    print('\n-----------------------------')
    print('Number of edges: ', len(G.edges()))
    print('Max Degree: ', max_deg)
    print('Min Degree: ', min_deg)
    print('Average Degree: ', observed_avg_deg)
    if display_mode == 1:
        print('Terminal Clique Size: ', terminal_size)
    if display_mode == 2:
        print('Number of Colors used: ', len(clist))
        print('Maximum Color Size: ', max_color)
    print('-----------------------------\n')
    print('Elapsed time: ', timeit.default_timer() - start, 'second(s)')

    if display_mode == 0:
        nx.draw(G, pos, node_size=2, node_color=c_map, alpha=0.5, edge_color='#00916a')
        nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color='red', width=1.0)
        nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=1.0)
    elif display_mode == 1:
        fig = plt.figure()
        def animate(i):
            if node_stack[i] in G.nodes():
                plt.clf()
                plt.axis('equal')
                G.remove_node(node_stack[i])
                nx.draw(G, pos, node_size=20, alpha=0.9, edge_color='#000000')

        anim = animation.FuncAnimation(fig, animate, frames=len(node_stack), interval=500)
    elif display_mode == 2:
        nx.draw(G, pos, node_size=5, node_color=c_map, edge_color='#000000')
    elif display_mode == 3:
        G1 = copy.deepcopy(G)
        G2 = copy.deepcopy(G)
        for node in G.nodes():
            if node not in bipartite_backbone[0]:
                G1.remove_node(node)
            if node not in bipartite_backbone[1]:
                G2.remove_node(node)
        plt.figure(1)
        plt.axis('off')
        plt.axis('equal')
        nx.draw(G1, pos, node_size=10, node_color=bipartite_nodeColors_1, edge_color='#000000')

        plt.figure(2)
        plt.axis('off')
        plt.axis('equal')
        nx.draw(G2, pos, node_size=10, node_color=bipartite_nodeColors_2, edge_color='#000000')

    plt.axis('off')
    plt.axis('equal')
    plt.show()

def main():
    nodes = int(input('Enter the number of nodes: '))
    expected_avg_deg = int(input('Enter the average degree: '))
    topology = int(input('Select a topology - \n0 (Plane) \n1 (Disk): '))
    display_mode = int(input(
        'Select display - \n''0'' (RGG plot) \n''1'' (Smallest last Ordering) \n''2'' (Coloring) \n''3'' (Backbone): '))

    if display_mode in (0, 1, 2, 3):
        plot_Graph(topology, nodes, expected_avg_deg, display_mode)
    else:
        print('Invalid input! Try again..')


if __name__ == "__main__":
    main()
