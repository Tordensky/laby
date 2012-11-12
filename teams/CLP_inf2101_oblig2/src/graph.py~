class Graph(object):
    """
    A simple undirected, weighted graph
    """
    def __init__(self):
        """ Initialize the graph as empty """
        self.nodes = {}
        self.edges = {}
        self.distances = {}
    
    def add_node(self, key, value):
        self.nodes[key] = [value]
    
    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)

    def _add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, [])
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


    def dijkstra(self, initial_node):
        visited = {initial_node: 0}
        current_node = initial_node
        path = {}
        
        nodes = self.nodes.keys()
        
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
    
            if min_node is None:
                break
    
            nodes.remove(min_node)
            cur_wt = visited[min_node]
            
            for edge in self.edges[min_node]:
                wt = cur_wt + self.distances[(min_node, edge)]
                if edge not in visited or wt < visited[edge]:
                    visited[edge] = wt
                    path[edge] = min_node
        
        return visited, path
    
    def shortest_path(self, initial_node, goal_node):
        distances, paths = self.dijkstra(initial_node)
        route = [goal_node]
    
        while goal_node != initial_node:
            route.append(paths[goal_node])
            goal_node = paths[goal_node]
    
        route.reverse()
        return route