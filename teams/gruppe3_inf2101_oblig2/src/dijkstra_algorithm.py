#!/usr/bin/env python
"""Implementation of Dijkstra algorithm found on www.wikipedia.org
and http://www.cs.berkeley.edu/~kamil/teaching/sp03/041403.pdf.
Recipy at: http://code.activestate.com/recipes/119466/
used as referance.
Author Adnan Begovic <abe065@post.uit.no>.
"""

from heapq import *
from adj_list_dict_of_dict import Graph

INFINITY = 99999999
class Shortest_path(object):
    """Find the shortest path between two nodes in the given graph. Use dictionaries
    to track distances of vertices and heap queue."""
    def dijkstra(self, graph, source, destination=None):
        dist = {}
        edges = {}
        Q = []
        for v in graph.graph:
            dist[v] = INFINITY
            heappush(Q, (dist[v], v))
            
        dist[source] = 0
        heapreplace(Q, (dist[source], source))
        
        while Q:
            u = heappop(Q)[1]
            if dist[u] == INFINITY:
                break
                
            for z in graph.neighbors(u):
                if dist[u] + graph.graph[u][z] < dist[z]:
                    dist[z] = dist[u] + graph.graph[u][z]
                    edges[z] = u
                    if z in Q:
                        heapreplace(Q, (dist[z], z))
                    else:
                        heappush(Q, (dist[z], z))

        return edges

    def shortestPath(self, graph, source, destination):
        edge = self.dijkstra(graph, source, destination)
        Path = []
        while 1:
            Path.append(destination)
            if destination == source:
                break
            destination = edge[destination]
        Path.reverse()
        return Path
        
