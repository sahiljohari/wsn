#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:36:49 2017

@author: Sahil
"""
import numpy as np
from scipy import spatial
import networkx as nx
import mpl_toolkits.mplot3d.axes3d as axes
import matplotlib.pyplot as plt
import timeit
import operator

fig = plt.figure()
ax = axes.Axes3D(fig)

nnodes = 8000
expected_avg_deg = 32
degree = {}
r = np.sqrt(expected_avg_deg/(nnodes*np.pi))

start = timeit.default_timer()

phi = np.random.uniform(0,2*np.pi, nnodes)
costheta = np.random.uniform(-1,1, nnodes)
u = np.random.uniform(0,1, nnodes)

theta = np.arccos( costheta )
radian = np.cbrt(u)

# theta = np.random.uniform(0, 2*np.pi, nnodes)
# radian = np.sqrt(np.random.uniform(0.0,1.0, nnodes))
x = (radian * np.sin(theta) * np.cos(phi))
y = (radian * np.sin(theta) * np.sin(phi))
z= (radian * np.cos(theta))

positions = np.vstack((x,y,z)).T


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
# nx.draw(G,pos, node_size=4, node_color='red', alpha=0.4)
ax.plot_wireframe(x,y,z)
plt.axis('equal')
plt.show()