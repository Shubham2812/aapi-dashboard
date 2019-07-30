""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
Mostly taken from https://www.python-course.eu/graphs_python.php
"""


class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].append(vertex2)
        else:
            self.graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
    
    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex 
            in graph """
        if path == None:
            path = []
        graph = self.graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, end_vertex, path)
                if extended_path: 
                    return extended_path
        return None
    
    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths
    
    def find_all_dependent_paths(self, end_vertex, path=[]):
        """find all paths dependent on a vertex"""
        graph = self.graph_dict
        dependent_paths = []
        for vertex in list(self.graph_dict.keys()):
            dependent_paths = dependent_paths + self.find_all_paths(vertex,
                                                               end_vertex,
                                                               path=[])
        return dependent_paths
    
    def find_all_dependency_paths(self, start_vertex, path=[]):
        """find all paths from a vertex to its dependencies"""
        graph = self.graph_dict
        dependency_paths = []
        for vertex in graph[start_vertex]:
            dependency_paths = dependency_paths + self.find_all_paths(start_vertex,
                                                                 vertex,
                                                                 path=[])
        return dependency_paths
    
    def vertex_degree(self, vertex):
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. Loops are counted 
            double, i.e. every occurence of vertex in the list 
            of adjacent vertices. """ 
        adj_vertices =  self.graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree
    
    def find_vertices_with_no_outbound_edges(self):
        """ returns a list of modules with 0 outbound edges. """
        graph = self.graph_dict
        vertices_with_no_outbound_edges = set()
        for vertex in graph:
            if not graph[vertex]:
                vertices_with_no_outbound_edges.add(vertex)
        return vertices_with_no_outbound_edges
    
    def find_vertices_with_no_inbound_edges(self):
        """ returns a list of modules with 0 inbound edges. """
        graph = self.graph_dict
        all_vertices = set(graph.keys())
        list_vetrices_with_inbound_edges = graph.values()
        set_of_vertices_with_inbound_edges = set()
        for list_of_vertices in list_vetrices_with_inbound_edges:
            for vertex in list_of_vertices:
                set_of_vertices_with_inbound_edges.add(vertex)
        return all_vertices.difference(set_of_vertices_with_inbound_edges)
        
    def find_isolated_vertices(self):
        graph = self.graph_dict
        return self.find_vertices_with_no_inbound_edges().intersection(self.find_vertices_with_no_outbound_edges())

    def delta(self):
        """ the minimum degree of the vertices """
        min = 100000000
        for vertex in self.graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min
        
    def Delta(self):
        """ the maximum degree of the vertices """
        max = 0
        for vertex in self.graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree > max:
                max = vertex_degree
        return max
    
    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for vertex in self.graph_dict:
            seq.append(self.vertex_degree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)

    def density(self):
        """ method to calculate the density of a graph """
        g = self.graph_dict
        V = len(g.keys())
        E = len(self.edges())
        return 2.0 * E / (V *(V - 1))

    def diameter(self):
        """ calculates the diameter of the graph """
        
        v = self.vertices() 
        pairs = [ (v[i],v[j]) for i in range(len(v)) for j in range(i+1, len(v)-1)]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_paths(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        # longest path is at the end of list, 
        # i.e. diameter corresponds to the length of this path
        diameter = len(smallest_paths[-1]) - 1
        return diameter

    @staticmethod
    def erdoes_gallai(dsequence):
        """ Checks if the condition of the Erdoes-Gallai inequality 
            is fullfilled 
        """
        if sum(dsequence) % 2:
            # sum of sequence is odd
            return False
        if Graph.is_degree_sequence(dsequence):
            for k in range(1,len(dsequence) + 1):
                left = sum(dsequence[:k])
                right =  k * (k-1) + sum([min(x,k) for x in dsequence[k:]])
                if left > right:
                    return False
        else:
            # sequence is increasing
            return False
        return True

    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for vertex in self.graph_dict:
            seq.append(self.vertex_degree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)
