#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:36:49 2017
@author: Sahil Johari
"""
import copy
import itertools
import operator
import timeit
import warnings
from itertools import chain

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy import spatial

warnings.filterwarnings("ignore")


# Private functions
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


# -----------

# Functions to implement the algorithms
def smallest_last_ordering(degree, adjacency_list):
    node_stack = []
    degreeBucket = {}
    deleted_node_degree = {}
    terminal_size = 0
    # Create a degree bucket
    for key, val in degree.items():
        degreeBucket.setdefault(val, []).append(key)
    # Delete the smallest nodes recursively
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

            degreeBucket.setdefault(d - 1, []).append(item)
            degree[item] -= 1
            counter += 1
        # Add the deleted node to the SLO stack
        node_stack.append(popped_node)
        deleted_node_degree[popped_node] = min_deg
        # Calculate terminal clique size
        if len(adjacency_list) - 1 == counter and terminal_size == 0:
            terminal_size = counter + 1
        del adjacency_list[popped_node]

    return node_stack, terminal_size, max(deleted_node_degree.values())


def graph_coloring(node_stack, adjacency_list):
    color_map = {}
    clist = [random_color()]
    # Iterate the SLO stack and assign colors to the nodes
    while node_stack:
        popped_node = node_stack.pop()
        # Fetch adjacent nodes for each node and check for their colors
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


def backbone_selection(G, color_data, color_count_data, adjacency_list):
    bipartite_nodes = []
    unique_bipartites = []
    max_backbone = []
    bipartite_nodeColors = []
    coverage_list = {}
    # Fetch the largest color classes and create their combinations
    largest_colors = sorted(color_count_data, key=color_count_data.get, reverse=True)[:4]
    largest_colors_combinations = list(itertools.combinations(largest_colors, 2))
    # Get nodes for each color combination
    for c_pair in largest_colors_combinations:
        bipartite_nodes.append((color_data[c_pair[0]], color_data[c_pair[1]]))
    # Remove duplicate nodes to create bipartite node list with unique nodes
    for node_pair in bipartite_nodes:
        bipartite_adj = {}
        for node in node_pair[0]:
            bipartite_adj[node] = list(set(adjacency_list[node]) & set(node_pair[1]))
        for node in node_pair[1]:
            bipartite_adj[node] = list(set(adjacency_list[node]) & set(node_pair[0]))
        unique_bipartites.append(copy.deepcopy(bipartite_adj))
    # Find the largest component backbones from the collection of bipartite node lists
    for collection in unique_bipartites:
        bipartite_nodelist = []
        bipartite_nodelist.extend(max(largest_component(collection), key=len))
        max_backbone.append(list(np.unique(list(chain.from_iterable(bipartite_nodelist)))))

    bipartite_backbone = sorted(max_backbone, key=len, reverse=True)[:6]
    # Calculate the coverage of each backbone and select the largest 2 of them
    subgraphs = [copy.deepcopy(G) for x in range(6)]
    coverage_set = [set() for x in range(6)]

    for node in G.nodes():
        for i in range(6):
            if node not in bipartite_backbone[i]:
                subgraphs[i].remove_node(node)

    for i in range(len(bipartite_backbone)):
        while True:
            flag = True
            Graph = copy.deepcopy(subgraphs[i])
            bipartite_degree_list = [Graph.degree(node) for node in
                                     Graph.nodes() if
                                     Graph.degree(node) > 1]
            for n in subgraphs[i].nodes():
                if Graph.degree(n) not in bipartite_degree_list:
                    try:
                        Graph.remove_node(n)
                        flag = False
                    except Exception:
                        pass
            subgraphs[i] = Graph
            if flag:
                break

    for i in range(6):
        for node in subgraphs[i].nodes():
            for n in adjacency_list[node]:
                coverage_set[i].add(n)
            coverage_set[i].add(node)
        coverage_list[subgraphs[i]] = len(coverage_set[i])

    largest_backbone_coverage = sorted(coverage_list, key=coverage_list.get, reverse=True)[:2]
    # Determine the node colors for the largest backbones obtained
    for i in range(2):
        temp_colors = []
        for node in largest_backbone_coverage[i].nodes():
            for key in color_data.keys():
                if node in color_data[key]:
                    temp_colors.append(key)
        bipartite_nodeColors.append(temp_colors)

    return sorted(coverage_list, key=coverage_list.get, reverse=True)[:2], bipartite_nodeColors, coverage_list


# ------------

def plot_Graph(topology, nodes, avgDeg, display_mode):
    degree = {}
    adjacency_list = {}
    color_data = {}  # contains collection of nodes for each distinct color
    c_map = []  # contains all the colors generated
    max_edges = []
    min_edges = []

    start = timeit.default_timer()
    if topology == 0:
        r = np.sqrt(avgDeg / (nodes * np.pi))
    elif topology == 1:
        r = np.sqrt(avgDeg / nodes)
    else:
        r = 0
    # RGG generation
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
        node_stack, terminal_size, max_degree_del = smallest_last_ordering(degree, adjlist_copy)
        if display_mode in (2, 3):
            node_stack_copy = copy.deepcopy(node_stack)
            color_map, clist = graph_coloring(node_stack_copy,
                                              adjacency_list)  # color_map->c_map ; clist contains list of distinct colors
            c_map = [None] * nodes
            for i in range(nodes):
                if i in color_map:
                    c_map[i] = color_map[i]
                else:
                    c_map[i] = clist[0]

            for k, v in color_map.items():
                color_data.setdefault(v, []).append(k)

            color_count_data = {k: len(color_data[k]) for k in color_data.keys()}  # contains node count for each color
            max_color = max(color_count_data.items(), key=operator.itemgetter(1))[1]

            if display_mode == 3:
                largest_backbone_coverage, bipartite_nodeColors, coverage_list = backbone_selection(G, color_data,
                                                                                                    color_count_data,
                                                                                                    adjacency_list)

    print('\n-----------------------------')
    if display_mode in (0, 1, 2):
        print('Number of edges: ', len(pairs))
        print('Max Degree: ', max_deg)
        print('Min Degree: ', min_deg)
        print('Average Degree: ', observed_avg_deg)
        if display_mode == 1:
            print('Terminal Clique Size: ', terminal_size)
            print('Maximum degree when deleted: ', max_degree_del)
        if display_mode == 2:
            print('Number of Colors used: ', len(clist))
            print('Maximum Color Size: ', max_color)
    if display_mode == 3:
        print('Backbone 1 vertices: ', len(largest_backbone_coverage[0].nodes()))
        print('Backbone 1 edges: ', len(largest_backbone_coverage[0].edges()))
        print('Backbone 1 coverage: ',
              format((coverage_list[largest_backbone_coverage[0]] / float(nodes)) * 100, '.2f'), '%')
        print('Backbone 2 vertices: ', len(largest_backbone_coverage[1].nodes()))
        print('Backbone 2 edges: ', len(largest_backbone_coverage[1].edges()))
        print('Backbone 2 coverage: ',
              format((coverage_list[largest_backbone_coverage[1]] / float(nodes)) * 100, '.2f'), '%')

    print('-----------------------------\n')
    print('Elapsed time: ', timeit.default_timer() - start, 'second(s)')

    if display_mode == 0:
        # Part I
        nx.draw(G, pos, node_size=2, node_color=c_map, alpha=0.5, edge_color='#00916a')
        nx.draw_networkx_edges(G, pos, edgelist=max_edges, edge_color='red', width=1.0)
        nx.draw_networkx_edges(G, pos, edgelist=min_edges, edge_color='blue', width=1.0)
    elif display_mode == 1:
        # Part II - Smallest last ordering
        fig = plt.figure()

        def animate(i):
            if node_stack[i] in G.nodes():
                plt.clf()
                plt.axis('equal')
                G.remove_node(node_stack[i])
                nx.draw(G, pos, node_size=20, alpha=0.9, edge_color='#000000')
                plt.autoscale(False)

        anim = animation.FuncAnimation(fig, animate, frames=len(node_stack), interval=50)
    elif display_mode == 2:
        # Part II - Graph coloring
        nx.draw(G, pos, node_size=5, node_color=c_map, edge_color='#000000')
    elif display_mode == 3:
        # Part III - Bipartite Backbone Selection
        plt.figure(1)
        plt.axis('equal')
        nx.draw(largest_backbone_coverage[0], pos, node_size=10, node_color=bipartite_nodeColors[0],
                edge_color='#000000')

        plt.figure(2)
        plt.axis('equal')
        nx.draw(largest_backbone_coverage[1], pos, node_size=10, node_color=bipartite_nodeColors[1],
                edge_color='#000000')

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
