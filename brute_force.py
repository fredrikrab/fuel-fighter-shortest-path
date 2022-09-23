"""
This script will generate all possible paths, calculate their lengths and save all paths below the given length threshold.

The first part of the script is the required code from the Jupyter notebook. The code related to brute forcing begins at line 120.

NB: This script will take a couple of minutes to complete.
"""

# IMPORT LIBRARIES
import numpy as np
import networkx as nx
from itertools import combinations, permutations

# DEFINE WAYPOINTS
# (x, y) goals
goals = {
    "start": (0,0),
    "g1": (-135, 1.50),
    "g2": (-212.00, -73.95),
    "g3": (-212.00, -198.22), 
    "g4": (-135.50, -256.00),
    "g5": (-84.5, -198.22),
    "g6": (-135.50, -128.00),
    "g7": (-135.50, -48.20),
    "g8": (44.50, -65.75),
    "g9": (0.0, -128.00),
    "g10": (44.50, -198.22),
    "g11": (0.0, -256.00)
}

# (x, y) intersections
intersections = {
    "i1": (44.50, 0.0),
    "i2": (-84.5, 0.0),
    "i3": (-212.00, 0.0),
    "i4": (-84.5, -48.20),
    "i5": (-212.00, -48.20),
    "i6": (44.50, -128),
    "i7": (-84.5, -128.00),
    "i8": (-212.00, -128.00),
    "i9": (44.50, -256),
    "i10": (-84.5, -256.00),
    "i11": (-212.00, -256.00)
}

# Make 'intersections' the common dictionary with all points of interest
intersections.update(goals)

# Specify valid travel routes
edges = {
    'i1': ['start', 'g8'],
    'i2': ['g1', 'start', 'i4'],
    'i3': ['g1', 'i5'],
    'i4': ['g7', 'i7'],
    'i5': ['g7', 'g2'],
    'i6': ['g8', 'g9', 'g10'],
    'i7': ['g9', 'g6', 'g5'],
    'i8': ['g2', 'g6', 'g3'],
    'i9': ['g10', 'g11'],
    'i10': ['g11', 'g5', 'g4'],
    'i11': ['g3', 'g4'],
}

# CREATE GRAPH
G = nx.Graph()

# Function to calculate the Manhattan distance between intersections
def m_dist(node_a, node_b):
    return abs(intersections[node_a][0] - intersections[node_b][0]) + abs(intersections[node_a][1] - intersections[node_b][1])

# Create nodes
for node in intersections:
    if node[0] in ['s', 'g']:
        G.add_node(node, type='goal')
    else:
        G.add_node(node, type='intersection')

# Attach edges to nodes, weighted by distance
for n in edges:
    for e in edges[n]:
        distance = m_dist(n, e)
        G.add_edge(n, e, weight=distance)

goal_nodes = [n for n, attribute in G.nodes(data=True) if attribute['type'] == 'goal']
intr_nodes = [n for n, attribute in G.nodes(data=True) if attribute['type'] == 'intersection']


# CREATE COMPLETE GRAPH
H = nx.Graph()

# Create 2-element tuple with all goal node combinations
goal_edges = combinations(goal_nodes, 2)

# Add all nodes and edges
H.add_nodes_from(goal_nodes)
H.add_edges_from(goal_edges)

# Calculate pairwise shortest path between all goals using Dijkstra's Algorithm
dijkstra_length = {}
for i in goal_nodes:
    for j in goal_nodes:
        length = nx.dijkstra_path_length(G, i, j)
        dijkstra_length[(i, j)] = length

# Add distance as weight to all edges
for e in H.edges():
    H[e[0]][e[1]]['weight'] = dijkstra_length[e]


# FUNCTION TO CALCULATE DISTANCE
# Lenght of shortest path that traverses the goals in the given order
def g_length(path):
    length = H.get_edge_data('start', 'g'+str(path[1]))['weight']      # length from start to first waypoint
    for k in range(1, len(path)-1):
        length += H.get_edge_data('g'+str(path[k]), 'g'+str(path[k+1]))['weight']
    return length


### CREATE PERMUTATIONS
goals = list(range(1, 12))
r = len(goals)

paths = permutations(goals, r)

### SAVE PATHS TO TEXT FILE
text_file_location = './brute_forced_paths.txt'
threshold = 1400

with open(text_file_location, 'w') as text_file:
    short_paths = []
    for entry in paths:
        path_lst = [0] + list(entry)
        length = g_length(path_lst)

        if length < threshold:
            short_paths.append((length, path_lst))
    
    short_paths.sort()
    for entry in short_paths:
        text_file.write(f"{entry[0]:.2f}\t {entry[1]}\n")
            
