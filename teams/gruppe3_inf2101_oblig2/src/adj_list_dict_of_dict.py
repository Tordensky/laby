#!/usr/bin/env python
""" Source code for the first lecture in INF-2101, fall 2012.
	Author John Marcus Bjoerndalen.
	Revized by Adnan Begovic, September 3rd 2012.
	Latest revision done by Adnan Begovic, September 30th 2012.
	Following methods are revised: removeEdge and hasEdge.
	Following methods are added: addVertice, removeVertice and
	neighbors. Latest revision removes pygraphviz module.
"""
import cProfile

class Graph(object):
    def __init__(self, vertices = None, edges = None):
        """Vertices is a list of the vertex ids or numbers.
        Edges is a list of (vertex, vertex) tuples.
        If both are None (or empty lists), the graph is empty.
        """
        self.graph = {}
        self.vertices = vertices
        self.edges = edges
        if self.vertices:
            for v in self.vertices:
                self.graph[v] = {}
        if self.edges:
            for e in self.edges:
                self.addEdge(e)
                
    def _addEdgeOneDir(self, v0, v1):
        """just add the edge in one direction"""
        if v0 not in self.graph:
            self.graph[v0] = {}
            self.graph[v0][v1] = 3
        else:
            if v1 not in self.graph[v0]:
                self.graph[v0][v1] = 3

    def addVertice(self, vertice):
        """Add a vertice in the graph as a key with
        empty dictionary as value."""
        if vertice not in self.graph:
            self.graph[vertice] = {}
        
    def addEdge(self, edge):
        """Add an edge such that we can easily check for
        both (v0,v1) and (v1,v0).
        Will also add vertices if necessary."""
        v0 = edge[0]
        v1 = edge[1]
        # Undirected graph, just make sure it shows both
        # directions.
        self._addEdgeOneDir(v0, v1)
        self._addEdgeOneDir(v1, v0)

    def removeEdge(self, edge):
        v0 = edge[0]
        v1 = edge[1]
        # Checking if the edge is existing
        try:
            if v1 in self.graph[v0]:
                del self.graph[v0][v1]
        except KeyError:
            print 'Oooops! Vertice ' + str(v0) + ' does not exsist in the graph!'

        try:
            if v0 in self.graph[v1]:
                del self.graph[v1][v0]
        except KeyError:
            print 'Oooops! Vertice ' + str(v1) + ' does not exsist in the graph!'

    def removeVertice(self, vertice):
        """Remove the vertice from graph and remove also all
        edges the vertice has with the neighbouring vertices."""
        # Checking if the vertice is existing in the graph
        try:
            if vertice in self.graph:
                # Deleting first all edges from neighbours to the vertice...
                for neighbour in self.graph[vertice]:
                    del self.graph[neighbour][vertice]
                # ... and at the end all edges from vertice to its neighbours
                del self.graph[vertice]
        except KeyError:
            print 'Oooops! ' + str(vertice) + ' does not exsist in the graph!'

    def hasVertice(self, vertice):
        """Returns true if there is vertice in the graph. """
        try:
            return vertice in self.graph
        except KeyError:
            print 'Cannot find vertice ' + str(vertice) + ' in the graph!'
            return False
    
    def hasEdge(self, v0, v1):
        """returns true if there is an edge between v0 and v1"""
        try:
            return v1 in self.graph[v0]
        except KeyError:
            print 'Oooops! Vertice ' + str(v0) + ' does not exsist in the graph!'
    
    def neighbors(self, vertice):
        """Returns list of all neighbors to the vertice"""
        nb = []
        for v in self.graph[vertice]:
            nb.append(v)
        return nb

    def show(self, image = 'graph.png'):
        # Later, we will use graphviz to visualize graphs.
        print "Graph"
        print " Vertices", sorted(self.graph.keys())
        print " Edges"
        for v0 in sorted(self.graph.keys()):
            print " ", v0, "->", \
            ", ".join([repr(x) for x in \
                        sorted(self.graph[v0])])
        # Using pygraphviz to visualize graph
        #G = pgv.AGraph(self.graph)
        #G.draw(image, prog="dot")

