"""
----------------------------------------------------
Smart Angkor Tourist Guide
Graph
----------------------------------------------------
This file creates the graph and performs
BFS, DFS and Dijkstra.

Ported from the original console-app graph.py, kept
functionally identical -- only used here as a library
that the Django views call into.
----------------------------------------------------
"""

import heapq


class Graph:

    # Create an empty graph
    def __init__(self):
        self.graph = {}

    # Add Edge
    def add_edge(self, source, destination, distance):

        if source not in self.graph:
            self.graph[source] = []

        if destination not in self.graph:
            self.graph[destination] = []

        self.graph[source].append((destination, distance))
        self.graph[destination].append((source, distance))

    # Breadth First Search (BFS)
    def bfs(self, start):

        visited = []
        queue = []
        queue.append(start)
        visited.append(start)

        while len(queue) > 0:
            current = queue.pop(0)

            for neighbor, distance in self.graph[current]:

                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)

        return visited

    # Depth First Search (DFS)
    def dfs(self, start):

        visited = []
        stack = []
        stack.append(start)

        while len(stack) > 0:
            current = stack.pop()

            if current not in visited:
                visited.append(current)

                for neighbor, distance in self.graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)

        return visited

    # Dijkstra Algorithm
    def dijkstra(self, start, destination):

        distances = {}
        previous = {}

        for temple in self.graph:
            distances[temple] = float("inf")
            previous[temple] = None

        distances[start] = 0

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))

        while priority_queue:
            current_distance, current = heapq.heappop(priority_queue)

            if current == destination:
                break

            for neighbor, weight in self.graph[current]:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        if distances[destination] == float("inf"):
            return [], float("inf")

        path = []
        current = destination

        while current is not None:
            path.insert(0, current)
            current = previous[current]

        return path, distances[destination]
