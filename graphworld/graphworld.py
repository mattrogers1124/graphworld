from dataclasses import dataclass
from random import sample
from scipy.spatial import ConvexHull
from .fibonacci import fibonacci_sphere


@dataclass
class GraphWorld:
    vertices: list
    edges: set
    neighbors: dict

    @staticmethod
    def generate_blank(n, alpha=1):
        vnew = sample(fibonacci_sphere(round(n*alpha)), n)
        enew = set()
        nnew = {i: set() for i in range(len(vnew))}
        return GraphWorld(vnew, enew, nnew)

    @staticmethod
    def generate_triangulated(n, alpha=1):
        g = GraphWorld.generate_blank(n, alpha)
        for s in ConvexHull(g.vertices).simplices:
            g.add_edge(s[0], s[1])
            g.add_edge(s[0], s[2])
            g.add_edge(s[1], s[2])
        return g

    @staticmethod
    def generate_labyrinth(n, alpha=1, degree=3):
        g = GraphWorld.generate_triangulated(n, alpha)
        edges_sorted = sorted(
            list(g.edges.difference(g.mwst())),
            key=lambda e: g.weight(min(e), max(e)),
            reverse=True)
        for e in edges_sorted:
            # If both vertices have at least degree+1 neighbors,
            # then we can delete this edge
            if len(g.neighbors[min(e)]) > degree and len(g.neighbors[max(e)]) > degree:
                g.remove_edge(min(e), max(e))
        return g

    def add_edge(self, index1: int, index2: int):
        # Check values
        if index1 == index2:
            raise ValueError(f"Indices should not be equal: ({index1}, {index2})")

        if index1 < 0 or index1 >= len(self.vertices):
            raise ValueError(f"Index out of bounds: ({index1}, {index2}) ({len(self.vertices)} vertices)")

        # Add to the edge set
        self.edges.add(frozenset([index1, index2]))

        # Add to the neighbor sets
        self.neighbors[index1].add(index2)
        self.neighbors[index2].add(index1)

    def remove_edge(self, index1: int, index2: int):
        # Check values
        if index1 == index2:
            raise ValueError(f"Indices should not be equal: ({index1}, {index2})")

        if index1 < 0 or index1 >= len(self.vertices):
            raise ValueError(f"Index out of bounds: ({index1}, {index2}) ({len(self.vertices)} vertices)")

        # Remove from the edges set
        self.edges.discard(frozenset([index1, index2]))

        # Remove from the neighbor sets
        self.neighbors[index1].discard(index2)
        self.neighbors[index2].discard(index1)

    def weight(self, index1: int, index2: int):
        # Calculates the weight of the edge between two vertices
        # Check values
        if index1 == index2:
            raise ValueError(f"Indices should not be equal: ({index1}, {index2})")

        if index1 < 0 or index1 >= len(self.vertices):
            raise ValueError(f"Index out of bounds: ({index1}, {index2}) ({len(self.vertices)} vertices)")

        p1 = self.vertices[index1]
        p2 = self.vertices[index2]
        delta = (p2[i] - p1[i] for i in range(3))
        return sum((x**2 for x in delta))

    def mwst(self):
        # Returns minimum weight spanning tree as a set of edges
        # Start with an empty set for the MWST
        mwst = set()

        # Use Kruskal's algorithm. Color each vertex differently.
        coloring = {i: i for i in range(len(self.vertices))}

        # Iterate through edges from least to greatest weight
        edges_sorted = sorted(list(self.edges), key=lambda e: self.weight(min(e), max(e)))
        for edge in edges_sorted:
            if coloring[min(edge)] == coloring[max(edge)]:
                # If the vertices are already the same color, do nothing
                continue
            else:
                # If they are different colors
                # then add the edge to the MWST,
                mwst.add(edge)
                # Recolor all the vertices matching the first color
                # so that they match the second
                color_old = coloring[min(edge)]
                color_new = coloring[max(edge)]
                for i in coloring.keys():
                    if coloring[i] == color_old:
                        coloring[i] = color_new

        # Return the MWST
        return mwst