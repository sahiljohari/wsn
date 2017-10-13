#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:36:49 2017

@author: Sahil
"""
import numpy as np
from scipy import spatial
import networkx as nx
import matplotlib.pyplot as plt
import timeit
import operator

# topology = 0    # 0 for square; 1 for circle
nnodes = 8000
expected_avg_deg = 32
degree = {}
r = np.sqrt(expected_avg_deg/(nnodes*np.pi))

start = timeit.default_timer()

# positions =  np.random.rand(nnodes,2)
# else:
theta = np.random.uniform(0, 2*np.pi, nnodes)
radian = np.sqrt(np.random.uniform(0.0,1.0, nnodes))
x = (radian * np.cos(theta))
y = (radian * np.sin(theta))

positions = np.vstack((x,y)).T


kdtree = spatial.KDTree(positions)
pairs = kdtree.query_pairs(r)

for edge in list(pairs):
   degree[edge[0]] = degree.get(edge[0], 0) + 1
   degree[edge[1]] = degree.get(edge[1], 0) + 1

max_deg = max(degree.items(), key=operator.itemgetter(1))[1]
min_deg = min(degree.items(), key=operator.itemgetter(1))[1]
total_deg = sum(degree.values())

observed_avg_deg = total_deg/nnodes

G = nx.Graph()
G.add_nodes_from(range(nnodes))
G.add_edges_from(list(pairs))

pos = dict(zip(range(nnodes),positions))
print('No. of edges: ', len(pairs))
print('Max Degree: ', max_deg)
print('Min Degree: ', min_deg)
print('Average Degree: ', observed_avg_deg)

print(timeit.default_timer() - start)
nx.draw(G,pos, node_size=4, node_color='white', alpha=0.4)
plt.axis('equal')
plt.show()